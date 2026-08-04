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
    if list(root.iter(f"{SVG}script")):
        fail("banner contains <script>; GitHub strips it and it is not needed")
    if list(root.iter(f"{SVG}style")):
        fail("banner contains <style>; use presentation attributes instead")
    if list(root.iter(f"{SVG}image")):
        fail("banner embeds <image>; the banner must be pure vector")
    stripped = raw.replace("http://www.w3.org/2000/svg", "").replace(
        "http://www.w3.org/1999/xlink", ""
    )
    if "http://" in stripped or "https://" in stripped:
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
            fail(
                f"banner is missing the {expected} wave drift "
                f"(durations found: {sorted(d for d in durs if d)})"
            )

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
    files = []
    if wf_dir.exists():
        files = sorted(p.name for p in wf_dir.iterdir() if p.suffix in {".yml", ".yaml"})
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
            with urllib.request.urlopen(req, timeout=30) as resp:
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
