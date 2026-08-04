# GitHub Profile README (Deep-Sea Shark Identity) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the three deliverables that make `github.com/jerungpyro/jerungpyro` render a deep-sea shark identity on the GitHub profile page — `README.md`, a hand-authored animated `assets/banner.svg`, and one `.github/workflows/snake.yml`.

**Architecture:** Three static artifacts plus one scheduled Action. The banner is self-contained SVG (own dark background, SMIL animation only — no CSS, no external fonts, no scripts) so it renders identically under GitHub's light and dark themes with no `<picture>` switching. Every hosted widget is themed by explicit hex params drawn from the same six-token palette, so third-party cards read as part of one designed surface. Verification is a zero-dependency Python script written **before** the artifacts, so each task has a real red→green cycle instead of eyeballing.

**Tech Stack:** Markdown + sanitizer-safe inline HTML, SVG 1.1 with SMIL, GitHub Actions YAML, Python 3 stdlib (verification only).

## Global Constraints

- Repo must be named **exactly** `jerungpyro`, be **public**, and have `README.md` at the root. Any other name renders nowhere.
- Default branch is **`main`**. The repo currently has zero commits on `master`; rename before the first commit.
- Palette — these six hexes are the only colours permitted anywhere:
  | Token | Hex | Role |
  |---|---|---|
  | abyss | `#0B1D2A` | banner background, widget backgrounds |
  | deep | `#123047` | depth band |
  | current | `#1E5F74` | mid-water band, widget borders |
  | foam | `#A8DADC` | wordmark, secondary text, wave lines |
  | ember | `#FF6B35` | primary accent — shark eye, section markers, headings |
  | ash | `#FFD166` | sparing highlight |
- Role line is exactly `Software Engineer`. **No employer is ever named** — this is deliberate so the README never goes stale on a job change.
- **Nothing student-framed.** The strings `student`, `Final-year`, `Netcentric`, `coursework`, `academic` must not appear in `README.md`.
- **Banned repos** — these were deliberately dropped and must not reappear in any form: `OOP-ASSIGNMENTS`, `CPP-ASSIGNMENTS`, `ICPROM-25`, `tictactoe`.
- Exactly **one** GitHub Action in `.github/workflows/`. WakaTime and blog-embed were rejected as YAGNI.
- Every image carries meaningful `alt` text. The banner's alt conveys the wordmark and role, never the word "banner".
- Content is never conveyed by colour alone — the `▸` / `▾` section markers are literal characters.
- No placeholder badges and no dead links. Only the real URLs below.
- Banner must degrade to a correct static image if SMIL is ever stripped — no layout depends on animation.

### Confirmed answers to the handover's open questions

1. **Stack** — add React, TypeScript, Python, FastAPI **and Capacitor** to the existing list.
2. **Taglines** — keep the drafted wording: `Software Engineer` / `mobile · backend · security` / `I ship things that people actually use`.
3. **Featured three** — confirmed as designed. Featured: CampusResQ, FoodTruck Finder, Task Manager. Collapsed: Task Manager API, Crypto Value Tracker, EV Charger Finder, Dividend Calculator, Personal Website.

### Canonical facts (copy verbatim; do not retype from memory)

| Field | Value |
|---|---|
| GitHub user | `jerungpyro` |
| Wordmark | `JERUNGPYRO` |
| Real name | Badrul Akasyah |
| Role line | `Software Engineer` |
| LinkedIn | `https://www.linkedin.com/in/badrulakasyah` |
| Instagram | `https://www.instagram.com/badrul_38` |
| Email | `mailto:bakasyah@gmail.com` |

| Project | URL |
|---|---|
| CampusResQ | `https://github.com/jerungpyro/RESQ` |
| FoodTruck Finder | `https://github.com/jerungpyro/foodtruck_finder` |
| Task Manager | `https://github.com/jerungpyro/Task-Manager-Dart-Laravel` |
| Task Manager API | `https://github.com/jerungpyro/task-manager-api-latest` |
| Crypto Value Tracker | `https://github.com/jerungpyro/crypto_value_tracker` |
| EV Charger Finder | `https://github.com/jerungpyro/ev_charger_finder` |
| Dividend Calculator | `https://github.com/jerungpyro/Dividend-Calc-App` |
| Personal Website | `https://github.com/jerungpyro/jerungpyro.github.io` |

### Deliberate deviation from the design's repo layout

`docs/DESIGN.md` lists only `README.md`, `assets/`, `.github/`. This plan adds `tools/check_profile.py` — dev-only verification tooling, never rendered on the profile. It is the mechanism that makes every task testable. If the owner wants a spotless tree, delete `tools/` in a final commit; nothing else depends on it.

---

### Task 1: Verification harness and repo skeleton

Written first so every later task has a failing check to turn green. Zero third-party dependencies — Python 3 stdlib only.

**Files:**
- Create: `tools/check_profile.py`
- Modify: branch rename `master` → `main`

**Interfaces:**
- Consumes: nothing.
- Produces: `python tools/check_profile.py` — offline structural checks, exit 0 on pass, exit 1 with a `FAIL:` line per problem. `python tools/check_profile.py --links` additionally HTTP-checks every URL found in `README.md`.

- [ ] **Step 1: Rename the branch (zero commits exist, so this is free)**

```bash
git branch -m master main
git rev-parse --abbrev-ref HEAD   # expect: main
```

- [ ] **Step 2: Write the verification script**

Create `tools/check_profile.py`:

```python
#!/usr/bin/env python3
"""Structural checks for the jerungpyro profile README, banner and workflow.

Offline by default. Pass --links to also HTTP-check every URL in README.md.
Stdlib only, so it runs anywhere Python 3 does.
"""
import re
import sys
import pathlib
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
SVG = "{http://www.w3.org/2000/svg}"

PALETTE = ["#0B1D2A", "#123047", "#1E5F74", "#A8DADC", "#FF6B35", "#FFD166"]

BANNED_FRAMING = ["student", "final-year", "netcentric", "coursework", "academic"]
BANNED_REPOS = ["OOP-ASSIGNMENTS", "CPP-ASSIGNMENTS", "ICPROM-25", "tictactoe"]

REQUIRED_LINKS = [
    "https://www.linkedin.com/in/badrulakasyah",
    "https://www.instagram.com/badrul_38",
    "mailto:bakasyah@gmail.com",
    "https://github.com/jerungpyro/RESQ",
    "https://github.com/jerungpyro/foodtruck_finder",
    "https://github.com/jerungpyro/Task-Manager-Dart-Laravel",
    "https://github.com/jerungpyro/task-manager-api-latest",
    "https://github.com/jerungpyro/crypto_value_tracker",
    "https://github.com/jerungpyro/ev_charger_finder",
    "https://github.com/jerungpyro/Dividend-Calc-App",
    "https://github.com/jerungpyro/jerungpyro.github.io",
]

failures = []


def fail(msg):
    failures.append(msg)


def check_banner():
    path = ROOT / "assets" / "banner.svg"
    if not path.exists():
        return fail("assets/banner.svg is missing")
    raw = path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        return fail(f"assets/banner.svg is not well-formed XML: {exc}")

    if root.tag != f"{SVG}svg":
        fail("assets/banner.svg root element is not <svg>")
    if root.get("viewBox") != "0 0 1200 300":
        fail(f'banner viewBox is {root.get("viewBox")!r}, expected "0 0 1200 300"')
    if root.get("width") != "100%":
        fail('banner must set width="100%" so it scales to the column')

    # Self-contained: no scripts, no external references, no CSS blocks.
    if root.iter(f"{SVG}script") and list(root.iter(f"{SVG}script")):
        fail("banner contains <script>; GitHub strips it and it is not needed")
    if list(root.iter(f"{SVG}style")):
        fail("banner contains <style>; use presentation attributes instead")
    if list(root.iter(f"{SVG}image")):
        fail("banner embeds <image>; the banner must be pure vector")
    if "http://" in raw or "https://" in raw.replace(
        "http://www.w3.org/2000/svg", ""
    ).replace("http://www.w3.org/1999/xlink", ""):
        fail("banner references an external URL; it must be self-contained")

    # Accessibility + identity.
    titles = [t.text or "" for t in root.iter(f"{SVG}title")]
    if not any("JERUNGPYRO" in t for t in titles):
        fail("banner <title> must name the JERUNGPYRO wordmark")
    if not list(root.iter(f"{SVG}desc")):
        fail("banner is missing a <desc>")

    texts = "".join((t.text or "") for t in root.iter(f"{SVG}text"))
    if "JERUNGPYRO" not in texts:
        fail("banner is missing the JERUNGPYRO wordmark text")
    if "Software Engineer" not in texts:
        fail("banner is missing the 'Software Engineer' role line")

    # Motion: three staggered wave drifts plus the shark drift.
    xforms = list(root.iter(f"{SVG}animateTransform"))
    if len(xforms) < 4:
        fail(f"banner has {len(xforms)} animateTransform elements, expected >= 4")
    durs = {x.get("dur") for x in xforms}
    for expected in ("8s", "11s", "14s"):
        if expected not in durs:
            fail(f"banner is missing the {expected} wave drift (durations found: {sorted(durs)})")

    # Palette discipline.
    used = set(m.upper() for m in re.findall(r"#[0-9A-Fa-f]{6}", raw))
    stray = used - set(PALETTE)
    if stray:
        fail(f"banner uses off-palette colours: {sorted(stray)}")
    for token in ("#0B1D2A", "#A8DADC", "#FF6B35"):
        if token not in used:
            fail(f"banner never uses {token}")


def check_readme():
    path = ROOT / "README.md"
    if not path.exists():
        return fail("README.md is missing")
    raw = path.read_text(encoding="utf-8")
    low = raw.lower()

    for word in BANNED_FRAMING:
        if word in low:
            fail(f"README.md contains outdated framing: {word!r}")
    for repo in BANNED_REPOS:
        if repo.lower() in low:
            fail(f"README.md resurrects a dropped repo: {repo}")
    for link in REQUIRED_LINKS:
        if link not in raw:
            fail(f"README.md is missing required link: {link}")

    if 'src="assets/banner.svg"' not in raw:
        fail("README.md does not reference assets/banner.svg")
    if "/jerungpyro/jerungpyro/output/snake.svg" not in raw:
        fail("README.md does not reference the snake output from the output branch")
    if "<details>" not in raw or "Deeper waters" not in raw:
        fail("README.md is missing the collapsed 'Deeper waters' section")
    if "SURFACING NOW" not in raw:
        fail("README.md is missing the 'SURFACING NOW' featured section")
    if "Software Engineer" not in raw:
        fail("README.md is missing the 'Software Engineer' role line")

    # Every <img> needs meaningful alt text.
    for tag in re.findall(r"<img\b[^>]*>", raw):
        alt = re.search(r'alt="([^"]*)"', tag)
        if not alt or not alt.group(1).strip():
            fail(f"<img> without alt text: {tag[:80]}")
        elif alt.group(1).strip().lower() in {"banner", "image", "img", "logo"}:
            fail(f"<img> alt text is not meaningful: {alt.group(1)!r}")

    # Markdown-image syntax must also carry alt text.
    for alt in re.findall(r"!\[([^\]]*)\]\(", raw):
        if not alt.strip():
            fail("markdown image with empty alt text")


def check_workflow():
    wf_dir = ROOT / ".github" / "workflows"
    files = sorted(p.name for p in wf_dir.glob("*.yml")) if wf_dir.exists() else []
    files += sorted(p.name for p in wf_dir.glob("*.yaml")) if wf_dir.exists() else []
    if files != ["snake.yml"]:
        return fail(f"expected exactly one workflow named snake.yml, found {files}")

    raw = (wf_dir / "snake.yml").read_text(encoding="utf-8")
    for needle, why in [
        ("Platane/snk@", "must pin the snk action"),
        ("target_branch: output", "must publish to the output branch"),
        ("workflow_dispatch", "must be manually runnable"),
        ("schedule", "must run on a cron schedule"),
        ("contents: write", "needs write permission to push the output branch"),
        ("color_snake=%23FF6B35", "snake must be ember-coloured"),
    ]:
        if needle not in raw:
            fail(f"snake.yml {why} (missing {needle!r})")

    # Tabs are illegal in YAML indentation.
    for i, line in enumerate(raw.splitlines(), 1):
        if line.startswith("\t"):
            fail(f"snake.yml line {i} is indented with a tab")


def check_links():
    import urllib.request
    import urllib.error

    raw = (ROOT / "README.md").read_text(encoding="utf-8")
    urls = sorted(set(re.findall(r"https://[^\s\"')<>]+", raw)))
    for url in urls:
        # The snake output branch does not exist until the Action first runs.
        if "output/snake.svg" in url:
            print(f"SKIP {url} (populated by the first Action run)")
            continue
        req = urllib.request.Request(url, headers={"User-Agent": "profile-check"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                code = resp.status
        except urllib.error.HTTPError as exc:
            code = exc.code
        except Exception as exc:  # noqa: BLE001 - report and continue
            fail(f"{url} -> {type(exc).__name__}: {exc}")
            continue
        if code >= 400:
            fail(f"{url} -> HTTP {code}")
        else:
            print(f"OK   {url} -> HTTP {code}")


def main():
    check_banner()
    check_readme()
    check_workflow()
    if "--links" in sys.argv:
        check_links()

    if failures:
        for f in failures:
            print(f"FAIL: {f}")
        print(f"\n{len(failures)} check(s) failed.")
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Run it and confirm it fails loudly**

Run: `python tools/check_profile.py`
Expected: exit 1, with `FAIL: assets/banner.svg is missing`, `FAIL: README.md is missing`, and a workflow failure line. This is the red state every later task turns green.

- [ ] **Step 4: Commit**

```bash
git add tools/check_profile.py HANDOVER.md docs/
git commit -m "chore: add profile verification harness and design docs"
```

---

### Task 2: The animated banner

**Files:**
- Create: `assets/banner.svg`

**Interfaces:**
- Consumes: the palette from Global Constraints.
- Produces: `assets/banner.svg` — `viewBox="0 0 1200 300"`, `width="100%"`. Referenced by Task 3 as `<img src="assets/banner.svg">`.

**Constraints specific to this file:** SMIL only (`<animate>`, `<animateTransform>`). No `<style>`, no `<script>`, no `@font-face`, no external hrefs — GitHub sanitizes or blocks all of them. Fonts must be a system-font stack, and both text elements use `textLength` + `lengthAdjust="spacing"` so the wordmark occupies the same box no matter which fallback font resolves on the viewer's machine. That is also what produces the wide letter-spacing.

- [ ] **Step 1: Write the banner**

Create `assets/banner.svg` with exactly this content:

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 300" width="100%"
     preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="bt bd">
  <title id="bt">JERUNGPYRO — Software Engineer</title>
  <desc id="bd">A geometric shark with a glowing ember eye glides through deep ocean water beside the JERUNGPYRO wordmark and the role line Software Engineer.</desc>

  <defs>
    <linearGradient id="water" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#1E5F74"/>
      <stop offset="0.42" stop-color="#123047"/>
      <stop offset="1" stop-color="#0B1D2A"/>
    </linearGradient>
    <linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#A8DADC" stop-opacity="0.13"/>
      <stop offset="1" stop-color="#A8DADC" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="glow">
      <stop offset="0" stop-color="#FF6B35" stop-opacity="0.6"/>
      <stop offset="1" stop-color="#FF6B35" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- water column: own background, so light/dark GitHub themes render identically -->
  <rect width="1200" height="300" fill="#0B1D2A"/>
  <rect width="1200" height="300" fill="url(#water)"/>
  <rect y="96" width="1200" height="2" fill="#1E5F74" opacity="0.35"/>
  <rect y="188" width="1200" height="2" fill="#1E5F74" opacity="0.22"/>

  <!-- light shafts -->
  <g>
    <polygon points="180,-20 250,-20 150,320 60,320" fill="url(#shaft)"/>
    <polygon points="640,-20 690,-20 600,320 540,320" fill="url(#shaft)"/>
    <polygon points="980,-20 1060,-20 940,320 850,320" fill="url(#shaft)"/>
    <animate attributeName="opacity" values="0.7;1;0.7" dur="9s" repeatCount="indefinite"/>
  </g>

  <!-- marine snow -->
  <g fill="#A8DADC" opacity="0.28">
    <circle cx="212" cy="0" r="2">
      <animate attributeName="cy" values="-10;310" dur="17s" repeatCount="indefinite"/>
    </circle>
    <circle cx="498" cy="0" r="1.5">
      <animate attributeName="cy" values="-10;310" dur="13s" begin="-4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="742" cy="0" r="2.5">
      <animate attributeName="cy" values="-10;310" dur="21s" begin="-9s" repeatCount="indefinite"/>
    </circle>
    <circle cx="1032" cy="0" r="1.5">
      <animate attributeName="cy" values="-10;310" dur="15s" begin="-2s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- shark: jerung -->
  <g>
    <animateTransform attributeName="transform" type="translate"
                      values="0 -7; 0 7; 0 -7" keyTimes="0;0.5;1"
                      calcMode="spline" keySplines="0.45 0 0.55 1; 0.45 0 0.55 1"
                      dur="7.5s" repeatCount="indefinite"/>
    <path fill="#A8DADC" d="M 432 150
      C 400 127 350 115 298 113
      L 268 72 L 250 115
      C 212 119 178 129 154 141
      L 90 92 L 128 150 L 98 206 L 154 159
      C 186 175 236 186 286 187
      C 344 188 404 172 432 150 Z"/>
    <path fill="#A8DADC" d="M 352 178 L 312 228 L 368 188 Z"/>
    <path fill="#A8DADC" d="M 250 186 L 228 214 L 264 190 Z"/>
    <g stroke="#0B1D2A" stroke-width="3" stroke-linecap="round" opacity="0.55">
      <path d="M 396 128 L 388 156"/>
      <path d="M 386 126 L 378 156"/>
      <path d="M 376 125 L 368 155"/>
      <path d="M 366 124 L 358 154"/>
    </g>
    <path d="M 430 155 C 416 170 402 175 386 176" fill="none" stroke="#0B1D2A"
          stroke-width="3" stroke-linecap="round" opacity="0.5"/>
    <circle cx="406" cy="139" r="26" fill="url(#glow)">
      <animate attributeName="opacity" values="0.55;1;0.55" dur="3.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="406" cy="139" r="5.5" fill="#FF6B35"/>
  </g>

  <!-- embers in the wake: pyro -->
  <g fill="#FF6B35">
    <circle cx="124" cy="196" r="2.5">
      <animate attributeName="cy" values="200;62" dur="4.6s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.95;0" dur="4.6s" repeatCount="indefinite"/>
    </circle>
    <circle cx="158" cy="196" r="2">
      <animate attributeName="cy" values="204;70" dur="5.8s" begin="-1.8s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.85;0" dur="5.8s" begin="-1.8s" repeatCount="indefinite"/>
    </circle>
    <circle cx="98" cy="196" r="1.8" fill="#FFD166">
      <animate attributeName="cy" values="196;58" dur="6.7s" begin="-3.4s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;0.8;0" dur="6.7s" begin="-3.4s" repeatCount="indefinite"/>
    </circle>
  </g>

  <!-- wordmark -->
  <text x="560" y="142" fill="#A8DADC" font-size="60" font-weight="700"
        textLength="580" lengthAdjust="spacing"
        font-family="'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif">JERUNGPYRO</text>
  <rect x="560" y="166" width="110" height="4" fill="#FF6B35"/>
  <rect x="682" y="167.5" width="458" height="1" fill="#A8DADC" opacity="0.25"/>
  <text x="560" y="206" fill="#A8DADC" opacity="0.78" font-size="22"
        textLength="268" lengthAdjust="spacing"
        font-family="'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif">Software Engineer</text>

  <!-- drifting waves: 400px period, translated by exactly one period so the loop is seamless -->
  <g fill="none" stroke="#A8DADC" stroke-width="2">
    <g opacity="0.18">
      <path d="M -400 234 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0"/>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-400 0" dur="14s" repeatCount="indefinite"/>
    </g>
    <g opacity="0.28">
      <path d="M -400 256 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0"/>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-400 0" dur="11s" repeatCount="indefinite"/>
    </g>
    <g opacity="0.4">
      <path d="M -400 276 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0 c 50 -14 150 -14 200 0 c 50 14 150 14 200 0"/>
      <animateTransform attributeName="transform" type="translate" from="0 0" to="-400 0" dur="8s" repeatCount="indefinite"/>
    </g>
  </g>
</svg>
```

- [ ] **Step 2: Run the banner checks and confirm they pass**

Run: `python tools/check_profile.py`
Expected: every `FAIL:` line mentioning `banner` is gone. `README.md is missing` and the workflow failure remain — those are Tasks 3–6.

- [ ] **Step 3: Eyeball it in a browser**

Run: `start assets/banner.svg` (PowerShell) or open the file directly.
Confirm by eye: waves drift leftward and never visibly jump; the shark rises and falls; the eye pulses; embers rise from the tail and fade; the wordmark and role line sit on the right without touching the edge.

- [ ] **Step 4: Confirm the static fallback**

Open the file and temporarily reason about it with animation disabled (`prefers-reduced-motion` in devtools, or mentally: every animated element has valid static attribute values). Nothing is positioned only by an animation, so the frozen first frame is a correct banner.

- [ ] **Step 5: Commit**

```bash
git add assets/banner.svg
git commit -m "feat: add animated deep-sea banner"
```

---

### Task 3: README — banner, badges, typing animation

**Files:**
- Create: `README.md`

**Interfaces:**
- Consumes: `assets/banner.svg` from Task 2.
- Produces: `README.md` with the centred masthead block. Tasks 4–6 append sections beneath it.

**Why these exact URL params:** `github-readme-stats`, `readme-typing-svg` and `shields.io` all accept raw hex without the `#`. Using explicit hex rather than a named preset theme is what keeps every card on the same six tokens. `komarev` renders a view counter and is display-only — it is deliberately not wrapped in a link.

- [ ] **Step 1: Write the masthead**

Create `README.md` with this content (Tasks 4–6 append below it; do not add a trailing separator yet):

```markdown
<div align="center">

<img src="assets/banner.svg" alt="JERUNGPYRO — Software Engineer" width="100%">

<br>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0B1D2A?style=for-the-badge&logo=linkedin&logoColor=A8DADC&labelColor=123047)](https://www.linkedin.com/in/badrulakasyah)
[![Instagram](https://img.shields.io/badge/Instagram-0B1D2A?style=for-the-badge&logo=instagram&logoColor=FF6B35&labelColor=123047)](https://www.instagram.com/badrul_38)
[![Email](https://img.shields.io/badge/Email-0B1D2A?style=for-the-badge&logo=gmail&logoColor=FFD166&labelColor=123047)](mailto:bakasyah@gmail.com)
![Profile views](https://komarev.com/ghpvc/?username=jerungpyro&style=for-the-badge&color=FF6B35&label=SIGHTINGS)

<br>

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=22&duration=2600&pause=900&color=FF6B35&center=true&vCenter=true&width=620&height=52&lines=Software+Engineer;mobile+%C2%B7+backend+%C2%B7+security;I+ship+things+that+people+actually+use" alt="Software Engineer — mobile, backend, security — I ship things that people actually use">

</div>
```

- [ ] **Step 2: Verify the four hosted URLs actually resolve**

Run:
```bash
python -c "import urllib.request as u; [print(x[:60], u.urlopen(u.Request(x, headers={'User-Agent':'c'}), timeout=20).status) for x in ['https://img.shields.io/badge/LinkedIn-0B1D2A?style=for-the-badge&logo=linkedin&logoColor=A8DADC&labelColor=123047','https://komarev.com/ghpvc/?username=jerungpyro&style=for-the-badge&color=FF6B35&label=SIGHTINGS','https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=22&duration=2600&pause=900&color=FF6B35&center=true&vCenter=true&width=620&height=52&lines=Software+Engineer']]"
```
Expected: `200` for each. If `readme-typing-svg.demolab.com` is down, the fallback host is `readme-typing-svg.herokuapp.com` with identical params — swap and re-run.

- [ ] **Step 3: Run the checker**

Run: `python tools/check_profile.py`
Expected: banner checks pass; remaining failures are the missing project links, the missing `SURFACING NOW` / `Deeper waters` sections, the missing snake reference, and the workflow. All are Tasks 4–6.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "feat: add README masthead with banner, socials and typing animation"
```

---

### Task 4: README — projects and stack

**Files:**
- Modify: `README.md` (append)

**Interfaces:**
- Consumes: the masthead from Task 3.
- Produces: the `SURFACING NOW` section, the stack section, and the collapsed `Deeper waters` `<details>` block. The design's success criterion is that the profile shows **four** projects at rest, not twelve — three featured plus the collapsed summary line.

- [ ] **Step 1: Append the projects and stack sections**

Append to `README.md`:

```markdown
---

## ▸ SURFACING NOW

**[CampusResQ](https://github.com/jerungpyro/RESQ)** — campus issue reporting with photo uploads, GPS-tagged reports, role-based access and real-time status tracking.
`Flutter` `Firebase` `Google Maps`

**[FoodTruck Finder](https://github.com/jerungpyro/foodtruck_finder)** — crowdsourced food truck discovery with an admin web panel for submitting, verifying and managing locations live.
`Flutter` `Firebase` `Cloud`

**[Task Manager](https://github.com/jerungpyro/Task-Manager-Dart-Laravel)** — full-stack task management: Flutter frontend, Laravel backend, web dashboard, priorities and due dates.
`Flutter` `Laravel` `MySQL` `REST`

---

## ▸ WHAT I BUILD WITH

**Languages** — TypeScript, JavaScript, Dart, Python, PHP, Java, Kotlin, C++, HTML

**Frameworks & tools** — React, FastAPI, Flutter, Capacitor, Laravel, Firebase, MySQL, REST APIs, Google Maps Platform

**Focus** — mobile and web platforms, backend systems, application security

---

<details>
<summary><b>▾ Deeper waters</b> — five more repositories</summary>

<br>

- **[Task Manager API](https://github.com/jerungpyro/task-manager-api-latest)** — RESTful task API built around clean backend workflows.
- **[Crypto Value Tracker](https://github.com/jerungpyro/crypto_value_tracker)** — real-time prices, watchlists and market visibility across multiple assets.
- **[EV Charger Finder](https://github.com/jerungpyro/ev_charger_finder)** — location-based search for EV charging stations.
- **[Dividend Calculator](https://github.com/jerungpyro/Dividend-Calc-App)** — a small financial calculator for dividend planning.
- **[Personal Website](https://github.com/jerungpyro/jerungpyro.github.io)** — portfolio site.

</details>
```

- [ ] **Step 2: Run the checker**

Run: `python tools/check_profile.py`
Expected: all `README.md is missing required link` failures are gone, as are the `SURFACING NOW` and `Deeper waters` failures. Remaining: the snake reference (Task 6) and the workflow (Task 6).

- [ ] **Step 3: Confirm the banned-content guard is real, not vacuous**

Run:
```bash
python - <<'EOF'
import pathlib
p = pathlib.Path("README.md")
orig = p.read_text(encoding="utf-8")
p.write_text(orig + "\nFinal-year student coursework\n", encoding="utf-8")
EOF
python tools/check_profile.py
```
Expected: FAIL lines naming `'student'`, `'final-year'` and `'coursework'`. Then restore:
```bash
git checkout README.md
```
and re-run `python tools/check_profile.py` to confirm those three failures are gone again.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "feat: add featured projects, stack and collapsed deeper-waters section"
```

---

### Task 5: README — stats widgets

**Files:**
- Modify: `README.md` (append)

**Interfaces:**
- Consumes: the sections from Task 4.
- Produces: the stats block — `github-readme-stats` and top-languages side by side in a two-column table, trophies full width beneath.

**Note on the trophy widget:** `github-profile-trophy` does not accept arbitrary hex the way `github-readme-stats` does; it takes preset theme names. `theme=darkhub` with `no-frame=true` gives a dark card that reads correctly under both GitHub themes, which is what the "renders correctly in light and dark" criterion requires. Do **not** add `no-bg=true` — that makes the card transparent and its light text vanishes on GitHub's light theme.

- [ ] **Step 1: Append the stats block**

Append to `README.md`:

```markdown
---

## ▸ THE NUMBERS

<div align="center">

<table>
<tr>
<td>

<img src="https://github-readme-stats.vercel.app/api?username=jerungpyro&show_icons=true&hide_border=true&bg_color=0B1D2A&title_color=FF6B35&text_color=A8DADC&icon_color=FFD166&ring_color=FF6B35" alt="GitHub statistics for jerungpyro">

</td>
<td>

<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=jerungpyro&layout=compact&hide_border=true&langs_count=8&bg_color=0B1D2A&title_color=FF6B35&text_color=A8DADC" alt="Most-used languages for jerungpyro">

</td>
</tr>
</table>

<img src="https://github-profile-trophy.vercel.app/?username=jerungpyro&theme=darkhub&no-frame=true&column=7&margin-w=6&margin-h=6" alt="GitHub achievement trophies for jerungpyro">

</div>
```

- [ ] **Step 2: Verify the three widget URLs resolve and honour the palette**

Run:
```bash
python - <<'EOF'
import urllib.request as u
urls = [
 "https://github-readme-stats.vercel.app/api?username=jerungpyro&show_icons=true&hide_border=true&bg_color=0B1D2A&title_color=FF6B35&text_color=A8DADC&icon_color=FFD166&ring_color=FF6B35",
 "https://github-readme-stats.vercel.app/api/top-langs/?username=jerungpyro&layout=compact&hide_border=true&langs_count=8&bg_color=0B1D2A&title_color=FF6B35&text_color=A8DADC",
 "https://github-profile-trophy.vercel.app/?username=jerungpyro&theme=darkhub&no-frame=true&column=7&margin-w=6&margin-h=6",
]
for url in urls:
    body = u.urlopen(u.Request(url, headers={"User-Agent": "c"}), timeout=30).read().decode("utf-8", "replace")
    print(url.split("?")[0], len(body),
          "0B1D2A" in body.upper(), "FF6B35" in body.upper(), "A8DADC" in body.upper())
EOF
```
Expected: each returns SVG of non-trivial length. For the two `github-readme-stats` URLs all three palette flags print `True`. For the trophy URL they may print `False` — that is expected and acceptable, since it uses a preset theme; confirm only that it returned SVG. If a `github-readme-stats` flag is `False`, the param name is wrong — fix it before committing.

- [ ] **Step 3: Run the checker**

Run: `python tools/check_profile.py`
Expected: no new failures; the alt-text check passes for all three new images. Remaining: snake reference and workflow.

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "feat: add palette-themed stats, language and trophy widgets"
```

---

### Task 6: The snake Action and its README reference

**Files:**
- Create: `.github/workflows/snake.yml`
- Modify: `README.md` (append)

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces: a workflow that writes `snake.svg` to a dedicated `output` branch every 12 hours, and the README reference that reads it back from `raw.githubusercontent.com/jerungpyro/jerungpyro/output/snake.svg`.

**Why the output branch:** committing a regenerated SVG to `main` twice a day would bury real history under bot commits. `output` is an orphan-ish publishing branch that nothing else reads. `color_dots` takes five comma-separated colours for contribution levels 0–4; `%23` is a URL-encoded `#`.

- [ ] **Step 1: Write the workflow**

Create `.github/workflows/snake.yml`:

```yaml
name: generate snake

on:
  schedule:
    - cron: "0 */12 * * *"
  workflow_dispatch:
  push:
    branches:
      - main

concurrency:
  group: snake
  cancel-in-progress: true

jobs:
  generate:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    permissions:
      contents: write

    steps:
      - name: Generate the contribution snake
        uses: Platane/snk@v3
        id: snake
        with:
          github_user_name: ${{ github.repository_owner }}
          outputs: |
            dist/snake.svg?color_snake=%23FF6B35&color_dots=%230B1D2A,%23123047,%231E5F74,%23A8DADC,%23FFD166

      - name: Publish to the output branch
        uses: crazy-max/ghaction-github-pages@v4
        with:
          target_branch: output
          build_dir: dist
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

- [ ] **Step 2: Append the snake to the README**

Append to `README.md`:

```markdown
---

<div align="center">

<img src="https://raw.githubusercontent.com/jerungpyro/jerungpyro/output/snake.svg" alt="A snake eating the jerungpyro contribution graph">

<br><br>

<sub>jerung + pyro — shark and fire</sub>

</div>
```

- [ ] **Step 3: Run the full checker — it should now be green**

Run: `python tools/check_profile.py`
Expected: `All checks passed.`

- [ ] **Step 4: Confirm the YAML actually parses**

Run:
```bash
python -c "import yaml,sys; yaml.safe_load(open('.github/workflows/snake.yml',encoding='utf-8')); print('yaml ok')"
```
Expected: `yaml ok`. If `ModuleNotFoundError: yaml`, install it once (`python -m pip install pyyaml`) and re-run — this check is worth the dependency, because a malformed workflow fails silently on GitHub until the first scheduled run.

- [ ] **Step 5: Commit**

```bash
git add .github/workflows/snake.yml README.md
git commit -m "feat: add contribution snake workflow and README reference"
```

---

### Task 7: Full verification pass

**Files:** none created; this task only validates.

**Interfaces:**
- Consumes: everything from Tasks 1–6.
- Produces: evidence that each of the design's six success criteria holds.

- [ ] **Step 1: Run the offline checks plus every link**

Run: `python tools/check_profile.py --links`
Expected: `All checks passed.`, with an `OK ... HTTP 200` line for every URL and a single `SKIP` line for the snake output (that branch does not exist until the Action first runs).

- [ ] **Step 2: Walk the six success criteria explicitly**

Confirm each, in order, and write down the evidence:

1. **Renders in both themes** — the banner carries its own `#0B1D2A` background rect; every widget sets `bg_color=0B1D2A` or uses the `darkhub` preset. No `prefers-color-scheme` switching anywhere. Confirm no `<picture>` element exists: `grep -c "<picture>" README.md` → `0`.
2. **No dead links, no placeholder badges** — Step 1's `--links` output is the evidence. Every badge points at a real URL from the canonical facts table.
3. **Four projects at rest** — three under `SURFACING NOW` plus the collapsed `<details>` summary. Count: `grep -c "github.com/jerungpyro" README.md` → `8` total project links, of which 5 are inside `<details>`.
4. **Nothing student-framed** — the checker's banned-framing guard passed, and Task 4 Step 3 proved that guard is not vacuous.
5. **Exactly one Action** — `ls .github/workflows` → `snake.yml` only. The checker asserts this.
6. **Banner animates and degrades** — Task 2 Steps 3 and 4.

- [ ] **Step 3: Preview the README as GitHub will render it**

Push to a scratch branch or paste into any GitHub markdown preview and confirm: the two-column stats table does not overflow, the `<details>` block is collapsed by default, and the `▸` / `▾` markers render as literal characters.

- [ ] **Step 4: Commit any fixes**

```bash
git add -A
git commit -m "fix: verification pass corrections"
```

---

### Task 8: Publish

**Files:** none. This is the manual GitHub step, and it is the only part that cannot be done from this working directory alone.

- [ ] **Step 1: Create the repository**

It must be named **exactly** `jerungpyro` and be **public**. With `gh` installed:
```bash
gh repo create jerungpyro --public --source=. --remote=origin --push
```
Without `gh`: create `jerungpyro` on github.com as a public repo with no README/gitignore/license, then:
```bash
git remote add origin https://github.com/jerungpyro/jerungpyro.git
git push -u origin main
```

- [ ] **Step 2: Trigger the snake once by hand**

The `output` branch does not exist until the Action runs. On GitHub: **Actions → generate snake → Run workflow**. Wait for it to go green.

- [ ] **Step 3: Confirm the snake image now resolves**

Run:
```bash
python -c "import urllib.request as u; print(u.urlopen('https://raw.githubusercontent.com/jerungpyro/jerungpyro/output/snake.svg', timeout=20).status)"
```
Expected: `200`. If it is `404`, the Action did not publish — check the run log for the `Publish to the output branch` step.

- [ ] **Step 4: Look at the profile**

Open `https://github.com/jerungpyro` in both a light-theme and a dark-theme browser session. The README must render above the repository list, banner animating, snake present.

---

## Self-review

**Spec coverage** — every numbered component in `docs/DESIGN.md` maps to a task: banner §1 → Task 2; badge row §2 → Task 3; typing animation §3 → Task 3; featured projects §4 → Task 4; stats widgets §5 → Task 5; deeper waters §6 → Task 4; snake §7 → Task 6. The stack update from the "standing assumption" section → Task 4. Accessibility §Accessibility → enforced by the checker's alt-text and `<title>`/`<desc>` rules in Task 1, verified in Tasks 2–5. Success criteria → Task 7. Repo layout → Task 8.

**Deviations, stated openly** — (a) `tools/check_profile.py` is not in the design's file tree; rationale in Global Constraints. (b) The design's anatomy sketch shows no heading above the stats widgets; this plan adds `▸ THE NUMBERS` for parallelism with the other two `▸` sections. (c) The trophy widget uses a preset theme rather than explicit hex because it does not support arbitrary hex — the closest achievable match to "themed via explicit colour params", and Task 5 Step 2 verifies rather than assumes this.

**Type consistency** — the checker's constant names (`REQUIRED_LINKS`, `BANNED_REPOS`, `BANNED_FRAMING`, `PALETTE`) are defined once in Task 1 and referenced by name only thereafter. Every URL in Tasks 3–6 appears verbatim in the canonical facts table. The path `dist/snake.svg` in Task 6 Step 1 matches `build_dir: dist` in the same file and the `output/snake.svg` reference in Step 2.
