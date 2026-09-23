# SOCIAL PLATFORM UNLOCK — GitHub ki madad se kya khul sakta hai? (2026-09-23)

> Sawaal: *"GitHub ki madad se Instagram, Reddit, Twitter/X, Facebook, Pinterest aur baaki social platforms unlock kar sakte ho ya nahi?"*
> Method: 20+ live probes (evidence: `probes/phase_social_probe.txt`) + GitHub se official SDKs + API policies ka fact-check.
> **Boundary (pehle se tay):** legitimate routes hi — login-wall/anti-bot bypass nahi. Jo tool bypass karta hai wo out of scope.

---

## 1. Seedha jawab: 3 categories me

| Category | Matlab | Platforms |
|---|---|---|
| **A. Bina kisi credential ke ABHI khul gaye** ✅ | aaj hi, is sandbox se verified | **Reddit (RSS), Telegram (public channels), Bluesky, Mastodon (fediverse), TikTok (public metadata), YouTube (yt-dlp se), X (third-party bridge — sirf public data)** |
| **B. User ke apne credentials/API key se khulenge** ⚠️ | GitHub par official SDKs ready hain; account/approval user ke haath me | Reddit full API, X (paid), Instagram/Facebook (Meta app), Pinterest, Discord, WhatsApp Business, Telegram Bot |
| **C. Legitimate route nahi mila** ❌ | na koi public API, na API key ka rasta bina app-review ke | Instagram **personal** scraping-free access, Facebook personal, Quora, aur X reads bina paise ke |

**Ek line:** GitHub se **official client libraries aur tools** milte hain (jo legit hain), lekin "login-wall todne wala" unlock GitHub par bhi nahi hota — aur wo hamare rules me bhi nahi hai (§25).

---

## 2. LIVE VERIFIED MATRIX (aaj ka test)

| Platform | Route | Result | Evidence |
|---|---|---|---|
| **Reddit** | Public RSS `.rss` | ✅ 200 — 24,685 B, titles aaye | `r/programming` feed |
| **Reddit** | OAuth API (praw) | ⚠️ 2026 me self-service app **band** — manual approval ticket lagta hai; free tier = 100 QPM non-commercial | fact-check §4 |
| **Telegram** | Public channel preview (`t.me/s/<channel>`) | ✅ 200 — 127,691 B, messages parse hue | `t.me/s/telegram` |
| **Telegram** | Bot API | ⚠️ BotFather token chahiye (user ka 2-min kaam) | — |
| **Bluesky** | Public AT-Protocol API (`public.api.bsky.app`) | ✅ 200 — actor search chal gaya; **koi key nahi** | 1,289 B; saath me `atproto` SDK se bhi actors mile |
| **Mastodon (fediverse)** | Instance public timelines | ✅ fosstodon.org 6,808 B · mastodon.world 7,358 B (instance par depend karta hai; mastodon.social/Infosec ne auth maanga) | — |
| **TikTok** | Public oEmbed | ✅ 200 — video title/author mile **bina kisi key** | 1,522 B |
| **YouTube** | yt-dlp se channel/video metadata | ✅ channel ki latest videos list hui | Fireship channel titles |
| **YouTube** | Official RSS feeds | ❌ 404/500 (is environment se block) | 2 IDs test kiye |
| **X (Twitter)** | Third-party bridge (fxtwitter) | ✅ 200 — public profile JSON (jack: 12.27M followers) — **sirf public data, third-party, GitHub se nahi** | 682 B |
| **X (Twitter)** | Nitter mirrors | ❌ sab dead (000/403) | 3 instances |
| **X (Twitter)** | Official API | ❌ 2026 me **pay-per-use**: $0.005/post read, $0.010/user profile; naya free tier khatam | fact-check §4 |
| **Instagram** | Anonymous API | ❌ homepage 200 (login page), `web_profile_info` 400 — **login ke bina data nahi** | — |
| **Instagram** | Graph API | ⚠️ sirf **business accounts** + Meta app review | — |
| **Facebook** | Anonymous / Graph API bina app | ❌ homepage 400; Graph API 403 "Provide valid app ID" | — |
| **Facebook** | Graph API (app token ke saath) | ⚠️ Meta app + permissions review | — |
| **Pinterest** | Anonymous resource API | ❌ homepage 200 par resource call 403 | — |
| **Pinterest** | API v5 | ⚠️ App + OAuth token chahiye | — |
| **RSSHub (public instance)** | GitHub-backed RSS bridge | ❌ 403 (public instance Cloudflare se blocked) — **self-host** karna padega | 2 routes test |
| **Quora** | koi route | ❌ (pehle bhi verify hua) | — |

---

## 3. GitHub ne isme kya diya (concrete)

| GitHub se aaya | Kya karta hai |
|---|---|
| **`atproto`** (official Bluesky SDK) | public API se actor/post search — **abhi bhi chal raha** (bina key) |
| **`praw` 8.0.3** (official Reddit SDK) | Reddit ka poora API — sirf OAuth creds daalne hain |
| **`tweepy` 4.17.0** (official X SDK) | X API calls — creds + X ka paid plan chahiye |
| **`yt-dlp`** | YouTube metadata/public media (verified) |
| **`github_unlock.py`** | in sab libs/releases ko fetch/manage karta hai |
| *(avoid)* Instaloader/jaisi scrapers | GitHub par maujood hain, lekin: ToS violation + platform anti-bot se block + legal risk → **hum use nahi karenge** |

## 4. User-action se kya-kya unlock hoga (2026 ke real rules ke saath)

| Platform | Kya chahiye | Cost / Effort | Milta kya hai |
|---|---|---|---|
| **Reddit** full API | OAuth app — **manual approval** (self-service band) | Free (non-commercial), 100 QPM — approval me hafte lag sakte hain | subreddit data, comments, search |
| **X (Twitter)** reads | Pay-per-use credits | **$0.005/post read** (~₹0.4), profile $0.010 | tweets, profiles, search |
| **Instagram** | Meta app + **business account** (Graph API) | Free par review lagta hai | apne business posts/insights |
| **Facebook** | Meta app + permissions | Free par review | Pages/comments |
| **Pinterest** | Developer app + OAuth | Free | pins/boards (apna ya public scope ke saath) |
| **Telegram** | BotFather bot token | **2 minute, free** | bot commands + channel auto-forward |
| **Discord** | Bot token | 2 minute, free | server data/announcements |
| **YouTube** | Data API key (Google Cloud) | Free (quota 10k/day) | search, metadata, comments |

## 5. Boundary — jo hum NAHI karenge (aur kyun)

1. **Login bypass / credential theft / session hijack** — koi bhi platform, kabhi bhi nahi.
2. **Anti-bot / CAPTCHA evasion** (jaise browser-fingerprint spoofing tools) — platform security ko todna = out of scope, aur bharosa kho dene wala kaam.
3. **ToS-blatant mass scraping** — technically "ho sakta hai" par ye platforms ke terms todta hai (aur accounts/IP block hote hain) — isliye nahi.
4. **Fake accounts / rate-limit bypass** — nahi.

Jo hum karenge: **official API + public endpoints + user ke apne credentials** — teen legitimate raste. Isiliye platform-wise jawab: *"kuch platforms abhi khul gaye (bina creds), kuch user ke 2-5 minute ke credential setup se khulenge, aur jo sirf bypass se khulte hain wo nahi khulenge."*

## 6. Practical: abhi kya use kar sakte hain

```bash
# Reddit (slow lane — 60s gap)
python3 -c "from tools.access_routes import rss; [print(i['title']) for i in rss('https://www.reddit.com/r/india/.rss', limit=5)]"

# Bluesky (koi key nahi)
python3 -c "from atproto import Client; c=Client(base_url='https://public.api.bsky.app'); print([a.handle for a in c.app.bsky.actor.search_actors(params={'q':'india','limit':5}).actors])"

# Mastodon
curl -s "https://mastodon.world/api/v1/timelines/public?limit=5" | head -c 300

# Telegram public channel
curl -s "https://t.me/s/telegram" | grep -o 'tgme_widget_message_text[^>]*>[^<]*' | head -3

# TikTok public metadata
curl -s "https://www.tiktok.com/oembed?url=<video-url>"

# YouTube (yt-dlp)
python3 -m yt_dlp --flat-playlist --playlist-end 5 --print "%(title)s" "https://www.youtube.com/@<channel>/videos"
```

## 7. Evidence
`probes/phase_social_probe.txt` (11 platform checks) + follow-up tests + `04_GITHUB_UNLOCK/` toolkit + installed SDKs (atproto/praw/tweepy).
