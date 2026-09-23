#!/usr/bin/env python3
"""
local_ai.py — UAI-COS LOCAL AI TOOLKIT (bina kisi API key)

2026-09-23 ke self-sweep me verified:
  • LLM    : Qwen2.5-0.5B-Instruct (GGUF Q4, llama.cpp, CPU) — 491 MB, load 0.6 s, ~4 s/reply
  • TTS    : edge-tts (Microsoft neural voices) — high-quality Hindi (hi-IN-SwaraNeural)
  • TTS-2  : espeak-ng fallback (fully offline, robotic)
  • STT    : faster-whisper (tiny/small; CPU; offline after first download)

Sab models /opt/uai-cache me jaate hain (persist hote hain between turns).

Usage:
    python3 tools/local_ai.py chat "Phase 2 kya tha?"            # local LLM
    python3 tools/local_ai.py say "नमस्ते दोस्तों" -o out.mp3     # Hindi TTS (natural)
    python3 tools/local_ai.py say "hello" --engine espeak         # offline fallback TTS
    python3 tools/local_ai.py transcribe audio.mp3                # STT
    python3 tools/local_ai.py status                              # kya-kya ready hai
"""
from __future__ import annotations
import argparse, os, subprocess, sys, time

CACHE = "/opt/uai-cache"
MODEL = os.path.join(CACHE, "models_qwen05b.gguf")
MODEL_URL = ("https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/"
             "qwen2.5-0.5b-instruct-q4_k_m.gguf")

SYSTEM = ("You are UAI-COS, a helpful assistant. User speaks Hindi in Roman script; "
          "reply in simple Roman Hindi + English technical terms. Be concise.")


def _ensure_model() -> str:
    if not os.path.exists(MODEL):
        os.makedirs(CACHE, exist_ok=True)
        print(f"[local_ai] model download ho raha hai: {MODEL_URL}")
        import urllib.request
        urllib.request.urlretrieve(MODEL_URL, MODEL)
        print(f"[local_ai] download done: {os.path.getsize(MODEL)/1e6:.0f} MB")
    return MODEL


def cmd_chat(args) -> int:
    from llama_cpp import Llama
    t0 = time.time()
    llm = Llama(model_path=_ensure_model(), n_ctx=args.ctx, verbose=False)
    sysmsg = SYSTEM if not args.raw else "You are a helpful assistant."
    out = llm.create_chat_completion(
        messages=[{"role": "system", "content": sysmsg},
                  {"role": "user", "content": args.prompt}],
        max_tokens=args.max_tokens, temperature=args.temp)
    print(out["choices"][0]["message"]["content"].strip())
    print(f"\n[local_ai] {time.time()-t0:.1f}s | model=Qwen2.5-0.5B-Q4 | CPU")
    return 0


def cmd_say(args) -> int:
    text, out = args.text, args.out
    if args.engine == "edge":
        try:
            import asyncio, edge_tts
            voice = args.voice
            asyncio.run(edge_tts.Communicate(text, voice).save(out))
            print(f"[local_ai] edge-tts({voice}) -> {out} ({os.path.getsize(out):,} B)")
            return 0
        except Exception as e:
            print(f"[local_ai] edge-tts fail ({e.__class__.__name__}); espeak fallback...")
            args.engine = "espeak"
    subprocess.run(["espeak-ng", "-v", args.espeak_lang, "-w", out, text], check=True)
    print(f"[local_ai] espeak-ng fallback -> {out} ({os.path.getsize(out):,} B)")
    return 0


def cmd_transcribe(args) -> int:
    from faster_whisper import WhisperModel
    t0 = time.time()
    m = WhisperModel(args.model, device="cpu", compute_type="int8")
    segs, info = m.transcribe(args.file, language=args.language or None)
    print(f"[lang={info.language} p={info.language_probability:.2f} model={args.model}]")
    for s in segs:
        print(f"  [{s.start:6.1f}s] {s.text.strip()}")
    print(f"[local_ai] {time.time()-t0:.1f}s")
    return 0


def cmd_status(_args) -> int:
    checks = [
        ("llama-cpp-python", lambda: __import__("llama_cpp").__version__),
        ("model (Qwen2.5-0.5B)", lambda: f"{os.path.getsize(MODEL)/1e6:.0f} MB" if os.path.exists(MODEL) else "not downloaded"),
        ("edge-tts", lambda: __import__("edge_tts").__version__),
        ("faster-whisper", lambda: __import__("faster_whisper").__version__),
        ("espeak-ng", lambda: subprocess.run(["espeak-ng", "--version"], capture_output=True).stdout.decode().strip()),
        ("sox", lambda: "ok" if subprocess.run(["which", "sox"], capture_output=True).returncode == 0 else "missing"),
        ("yt-dlp", lambda: "ok" if __import__("yt_dlp") else ""),
    ]
    print("UAI-COS LOCAL AI TOOLKIT — status")
    for name, fn in checks:
        try:
            print(f"  OK   {name:24} {fn()}")
        except Exception as e:
            print(f"  MISS {name:24} ({e.__class__.__name__})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="UAI-COS local AI toolkit (no keys)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("chat", help="local LLM se jawab")
    c.add_argument("prompt")
    c.add_argument("--max-tokens", type=int, default=200)
    c.add_argument("--temp", type=float, default=0.7)
    c.add_argument("--ctx", type=int, default=2048)
    c.add_argument("--raw", action="store_true", help="default system prompt hatao")

    s = sub.add_parser("say", help="text → speech")
    s.add_argument("text")
    s.add_argument("-o", "--out", default="speech.mp3")
    s.add_argument("--engine", choices=["edge", "espeak"], default="edge")
    s.add_argument("--voice", default="hi-IN-SwaraNeural")
    s.add_argument("--espeak-lang", default="hi")

    t = sub.add_parser("transcribe", help="audio → text (offline)")
    t.add_argument("file")
    t.add_argument("--model", default="tiny", help="tiny | base | small ...")
    t.add_argument("--language", default="hi")

    sub.add_parser("status", help="kya ready hai")

    args = ap.parse_args()
    return {"chat": cmd_chat, "say": cmd_say, "transcribe": cmd_transcribe, "status": cmd_status}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
