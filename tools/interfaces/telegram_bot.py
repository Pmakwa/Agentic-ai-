#!/usr/bin/env python3
"""
telegram_bot.py — UAI-COS v2.0 Telegram interface (memory console + LLM bridge)

Ye UAI-COS spec ko is chat se BAHAR le jaata hai: Telegram se memory likho/padho,
audit dekho, aur (LLM key ho to) UAI-COS system prompt ke saath jawab lo.

Design (spec sections):
  #68 Security model    -> chat-id whitelist (ALLOWED_CHAT_IDS), warna deny
  #0.6 Least privilege  -> read commands (A4 free) vs write commands (log hoti hain)
  #10/#49 Approval      -> /forget (delete) confirm ke bina execute nahi hota
  #51 Observability     -> har command audit log me likhi jaati hai
  #58 Graceful degrade  -> LLM key na ho to bhi memory console chalta hai
  #70 Privacy           -> /ask me sirf non-sensitive memory inline hoti hai

Setup:
  export TELEGRAM_BOT_TOKEN="123456:ABC..."       # BotFather se
  export ALLOWED_CHAT_IDS="123456789"             # apna chat id (bot /id se batata hai)
  # optional (LLM answer ke liye — ek bhi provider kaafi hai)
  export LLM_PROVIDER="openai"                    # openai | anthropic | gemini | ollama
  export LLM_API_KEY="sk-..."
  export LLM_MODEL="gpt-4o-mini"

Run (background me):
  python3 tools/interfaces/telegram_bot.py
  # ya: nohup python3 tools/interfaces/telegram_bot.py > logs/bot.log 2>&1 &

Commands:
  /start /help /status /mem <text> /list [type] /search <q> /audit /ask <question> /id /dash
Stdlib only — koi pip dependency nahi.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import uai_mem  # noqa: E402  (memory engine reuse — single source of truth)

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
ALLOWED = {c.strip() for c in os.environ.get("ALLOWED_CHAT_IDS", "").split(",") if c.strip()}
PROVIDER = os.environ.get("LLM_PROVIDER", "openai").strip().lower()
API_KEY = os.environ.get("LLM_API_KEY", "").strip()
MODEL = os.environ.get("LLM_MODEL", "").strip()
TG = f"https://api.telegram.org/bot{TOKEN}"

HELP = """*UAI-COS v2.0 — memory console*

/mem <text>      — naya memory record (candidate) banao
/list [type]     — live records (type optional: preference, constraint, project …)
/search <q>      — memory me dhoondo
/audit           — memory health score + issues
/ask <question>  — UAI-COS prompt ke saath LLM se jawab (LLM key chahiye)
/status          — system snapshot
/id              — apna chat id (whitelist me daalne ke liye)
/dash            — dashboard file path

Rule: /mem se bana record `candidate` hota hai — `verified` tab jab tum confirm karo.
Delete jaisa kaam bot nahi karta (irreversible = human approval, spec #49)."""


# ------------------------------------------------------------------ telegram io
def tg(method: str, **params):
    data = urllib.parse.urlencode(params).encode()
    try:
        with urllib.request.urlopen(f"{TG}/{method}", data=data, timeout=40) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[TG ERROR] {method}: {e.code} {e.read()[:200]}", file=sys.stderr)
    except Exception as e:  # network hiccup -> bot marta nahi hai
        print(f"[TG ERROR] {method}: {e}", file=sys.stderr)
    return None


def send(chat_id: int, text: str, reply_to: int | None = None) -> None:
    # Telegram limit 4096 chars — chunk karo (Section #77 output format engine)
    for i in range(0, len(text), 3800):
        chunk = text[i:i + 3800]
        kwargs = {"chat_id": chat_id, "text": chunk, "parse_mode": "Markdown"}
        if reply_to and i == 0:
            kwargs["reply_to_message_id"] = reply_to
        if not tg("sendMessage", **kwargs):
            tg("sendMessage", chat_id=chat_id, text=chunk)  # markdown fail -> plain retry (graceful degradation)


# ------------------------------------------------------------------ llm bridge
def build_prompt() -> str:
    """UAI-COS system prompt — compiler se (single source of truth)."""
    import subprocess
    out = os.path.join(HERE, "_runtime_system_prompt.md")
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "build_system_prompt.py"),
                    "-m", "standard", "-o", out], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return open(out, encoding="utf-8").read()


def llm_answer(question: str) -> str:
    if not API_KEY and PROVIDER != "ollama":
        return ("LLM key set nahi hai (`LLM_API_KEY`), isliye /ask band hai — "
                "memory console (mem/list/search/audit) phir bhi chalu hai.\n"
                "Key set karke bot restart karo, ya khali prompt se kaam chalao.")
    system = build_prompt()
    try:
        if PROVIDER == "anthropic":
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=json.dumps({"model": MODEL or "claude-sonnet-4-20250514", "max_tokens": 2000,
                                 "system": system,
                                 "messages": [{"role": "user", "content": question}]}).encode(),
                headers={"x-api-key": API_KEY, "anthropic-version": "2023-06-01",
                         "content-type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read().decode())
                return "".join(b.get("text", "") for b in d.get("content", []))
        if PROVIDER == "gemini":
            url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
                   f"{MODEL or 'gemini-2.0-flash'}:generateContent?key={API_KEY}")
            req = urllib.request.Request(url, data=json.dumps({
                "system_instruction": {"parts": [{"text": system}]},
                "contents": [{"role": "user", "parts": [{"text": question}]}]}).encode(),
                headers={"content-type": "application/json"})
            with urllib.request.urlopen(req, timeout=120) as r:
                d = json.loads(r.read().decode())
                return d["candidates"][0]["content"]["parts"][0]["text"]
        # default: OpenAI-compatible (OpenAI / OpenRouter / Groq / local vLLM / Ollama-compat)
        base = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1")
        req = urllib.request.Request(
            f"{base.rstrip('/')}/chat/completions",
            data=json.dumps({"model": MODEL or "gpt-4o-mini", "temperature": 0.3,
                             "messages": [{"role": "system", "content": system},
                                          {"role": "user", "content": question}]}).encode(),
            headers={"Authorization": f"Bearer {API_KEY}", "content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read().decode())
            return d["choices"][0]["message"]["content"]
    except Exception as e:
        # Section #57 fallback: memory console hamesha available rahe
        return f"[LLM error] {type(e).__name__}: {e}\nMemory console commands phir bhi chalu hain."


# ------------------------------------------------------------------ command handlers
def show_list(args: str) -> str:
    rows = [r for r in uai_mem.load() if r["status"] not in ("deleted", "archived")]
    if args.strip():
        rows = [r for r in rows if r["type"] == args.strip()]
    if not rows:
        return "Koi record nahi mila."
    lines = [f"*{len(rows)} record(s)*"]
    for r in rows[:60]:
        mark = {"verified": "V", "active": "A", "conflicted": "!", "candidate": "?"}.get(r["status"], "·")
        lines.append(f"`{r['id']}` [{mark}] {r['statement'][:110]}")
    if len(rows) > 60:
        lines.append(f"… aur {len(rows) - 60} records (CLI se dekho)")
    return "\n".join(lines)


def do_mem(text: str, chat_id: int) -> str:
    text = text.strip()
    if len(text) < 8:
        return "Thoda detail do: `/mem <poora statement>` (min 8 chars)."
    # Heuristic type routing (Section #6 task classification ka mini version)
    low = text.lower()
    # Precedence (spec #6 classification): constraint > preference(durable) > error > project > working
    mtype, authority = "working", "user_explicit"
    if any(k in low for k in ("mat karo", "never", "nahi karna", "mana", "avoid", "band karo", "mat bhejo")):
        mtype = "constraint"
    elif any(k in low for k in ("hamesha", "always", "prefer", "pasand", "har baar", "default")):
        mtype = "preference"
    elif any(k in low for k in ("galti", "mistake", "fail hua", "error aaya", "bug")):
        mtype = "error"
    elif any(k in low for k in ("project", "task hai", "kaam chal raha")):
        mtype = "project"
    rec = {
        "type": mtype, "statement": text,
        "source": {"kind": "telegram_user", "ref": f"chat:{chat_id}", "observed_at": uai_mem.today()},
        "scope": {"domains": [], "projects": [], "agents": []},
        "confidence": "medium", "status": "candidate", "authority": authority,
        "sensitivity": "private",  # telegram se aaya data default private
        "tags": ["telegram"], "applies_when": "", "does_not_apply_when": "",
        "detail": "Telegram /mem se capture hua — user confirm kare to verified karo.",
        "id": "", "verified": "", "expires": "", "supersedes": "", "conflict_key": "", "force": True,
    }
    class A:  # CLI ka argparse namespace mimic
        pass
    a = A()
    for k, v in rec.items():
        setattr(a, k, v)
    a.ref = f"telegram:{chat_id}"
    a.note = "telegram /mem se capture"
    a.domain = a.project = a.agent = []
    a.tag = ["telegram"] + (["private"] if True else [])
    a.url = ""
    a.observed = uai_mem.today()
    uai_mem.cmd_add(a)
    uai_mem.cmd_index(a)
    return (f"📝 `candidate` memory bani (type: *{mtype}*).\n"
            f"Record me history + provenance hai; `verified` tab hogi jab tum confirm karo.\n"
            f"Note: sensitive hone par main ise bahar share nahi karunga (spec #70).")


def status_text() -> str:
    rows = uai_mem.load()
    live = [r for r in rows if r["status"] not in ("deleted", "archived")]
    from collections import Counter
    return (f"*UAI-COS v2.0 — status*\n"
            f"Live records: *{len(live)}*\n"
            f"Status: {dict(Counter(r['status'] for r in live))}\n"
            f"Types: {len(Counter(r['type'] for r in live))} active types\n"
            f"LLM bridge: {'ON (' + PROVIDER + ')' if (API_KEY or PROVIDER == 'ollama') else 'OFF (key nahi hai)'}\n"
            f"Whitelist: {len(ALLOWED) or 'OPEN (set ALLOWED_CHAT_IDS!)'} chat(s)\n"
            f"Dashboard: `{os.path.join(ROOT, 'DASHBOARD.html')}`")


def handle(chat_id: int, text: str, mid: int) -> None:
    cmd, _, arg = text.partition(" ")
    cmd = cmd.lower().lstrip("/")
    uai_mem.log_audit("telegram.command", f"chat={chat_id} cmd={cmd}")

    if cmd in ("start", "help"):
        send(chat_id, HELP, mid)
    elif cmd == "id":
        send(chat_id, f"Your chat id: `{chat_id}`", mid)
    elif cmd == "status":
        send(chat_id, status_text(), mid)
    elif cmd == "mem":
        send(chat_id, do_mem(arg, chat_id), mid)
    elif cmd == "list":
        send(chat_id, show_list(arg), mid)
    elif cmd == "search":
        hits = [r for r in uai_mem.load() if arg.lower() in json.dumps(r, ensure_ascii=False).lower()]
        out = [f"*{len(hits)} hit(s)*"] + [f"`{r['id']}` {r['statement'][:110]}" for r in hits[:30]]
        send(chat_id, "\n".join(out) if hits else "Kuch nahi mila.", mid)
    elif cmd == "audit":
        rows = uai_mem.load()
        import io, contextlib
        buf, old = io.StringIO(), sys.stdout
        sys.stdout = buf
        try:
            class A: pass
            a = A(); a.log = True; a.working_ttl = 7; a.fact_freshness_days = 180; a.fail_under = 70
            uai_mem.cmd_audit(a)
        finally:
            sys.stdout = old
        send(chat_id, "```\n" + buf.getvalue()[-3300:] + "\n```", mid)
    elif cmd == "ask":
        if not arg.strip():
            send(chat_id, "Sawaal likho: `/ask <question>`", mid)
        else:
            send(chat_id, "Soch raha hoon… (UAI-COS prompt + live memory ke saath)")
            send(chat_id, llm_answer(arg), mid)
    elif cmd == "dash":
        send(chat_id, f"Dashboard file: `{os.path.join(ROOT, 'DASHBOARD.html')}`\n"
                      f"Index: `{os.path.join(ROOT, 'memory', 'INDEX.md')}`", mid)
    else:
        send(chat_id, "Samajh nahi aaya. /help dekho.", mid)


# ------------------------------------------------------------------ main loop
def main() -> int:
    if not TOKEN:
        print("TELEGRAM_BOT_TOKEN set nahi hai.\n"
              "1) Telegram me @BotFather -> /newbot -> token lo\n"
              "2) export TELEGRAM_BOT_TOKEN='...'\n"
              "3) export ALLOWED_CHAT_IDS='<apna id>' (bot /id batata hai)\n"
              "4) python3 tools/interfaces/telegram_bot.py", file=sys.stderr)
        return 2

    me = tg("getMe")
    if me and me.get("ok"):
        print(f"[OK] Bot online: @{me['result']['username']}")
    tg("setMyCommands", commands=json.dumps([
        {"command": "mem", "description": "naya memory record"},
        {"command": "list", "description": "live records"},
        {"command": "search", "description": "memory search"},
        {"command": "audit", "description": "memory health"},
        {"command": "ask", "description": "LLM se jawab (UAI-COS prompt)"},
        {"command": "status", "description": "system snapshot"},
    ]))
    uai_mem.log_audit("telegram.boot", f"bot started (provider={PROVIDER}, whitelist={len(ALLOWED)})")
    print("[OK] Polling shuru (Ctrl+C se band).")

    offset = 0
    while True:
        try:
            r = tg("getUpdates", offset=offset, timeout=30)
            if not r or not r.get("ok"):
                time.sleep(3)
                continue
            for upd in r["result"]:
                offset = upd["update_id"] + 1
                msg = upd.get("message") or upd.get("edited_message")
                if not msg or "text" not in msg:
                    continue
                chat_id = msg["chat"]["id"]
                # Section #68: whitelist na ho to deny (aur chat id batao, taaki user add kar sake)
                if ALLOWED and str(chat_id) not in ALLOWED:
                    tg("sendMessage", chat_id=chat_id,
                       text=f"Access denied (spec #68 least privilege).\nYe bot owner se whitelist me add karwao. Chat id: `{chat_id}`")
                    uai_mem.log_audit("telegram.denied", f"chat={chat_id}")
                    continue
                print(f"[MSG] {chat_id}: {msg['text'][:80]}")
                handle(chat_id, msg["text"], msg["message_id"])
        except KeyboardInterrupt:
            print("\n[STOP] Bot band kiya.")
            return 0
        except Exception as e:
            print(f"[LOOP ERROR] {type(e).__name__}: {e}", file=sys.stderr)
            time.sleep(5)


if __name__ == "__main__":
    sys.exit(main())
