# GitHub Profile README — Deep-Sea Shark Identity

**Date:** 2026-08-04
**Owner:** Badrul Akasyah ([@jerungpyro](https://github.com/jerungpyro))
**Status:** Design — awaiting review

> **Note:** this spec was drafted during an unrelated session in the KOWAJA working
> directory and copied here. This folder is now the home for the work. The original
> copies in `Documents/Code/KOWAJA` (`README2.md` and
> `docs/superpowers/specs/2026-08-04-github-profile-readme-design.md`) are stale and
> safe to delete.

## Goal

Replace a plain bulleted profile README with one that has a genuine visual identity.
The stated priority is visual impact, not recruiter conversion — this is built to look
good first and inform second.

## Decisions

| Question | Decision |
|---|---|
| Audience | Primarily the owner. Optimise for looking good, not for a recruiter skim. |
| Machinery budget | Full: hosted widgets + one GitHub Action + hand-authored custom art. |
| Direction | Deep-sea shark identity, built on the meaning of `jerungpyro` (Malay *jerung* = shark, + *pyro* = fire). |
| Display name | `JERUNGPYRO` as the wordmark. |
| Role line | "Software Engineer" — **no employer named**, so the README never goes stale on a job change. |
| Coursework repos | Dropped entirely (OOP Assignments, CPP Assignments, ICPROM-25, Tic Tac Toe). |
| Socials | LinkedIn, Instagram, Email. Real URLs only — no placeholder badges. |

### Standing assumption to confirm

The stack section will be updated to add **React, TypeScript, Python, FastAPI**. The
existing list (HTML/PHP/Java/Kotlin/Dart/C++, Flutter/Laravel/Firebase) predates the
owner's current professional work, which is a React + TypeScript + FastAPI + Capacitor
codebase. If that work should not be reflected, say so and this reverts.

## Visual system

Self-contained dark palette. The banner carries its own background, so it renders
identically under GitHub's light and dark themes with no `<picture>` /
`prefers-color-scheme` switching.

| Token | Hex | Role |
|---|---|---|
| abyss | `#0B1D2A` | banner background, widget backgrounds |
| deep | `#123047` | depth band |
| current | `#1E5F74` | mid-water band, widget borders |
| foam | `#A8DADC` | wordmark, secondary text, wave lines |
| ember | `#FF6B35` | primary accent — shark eye, section markers, headings |
| ash | `#FFD166` | sparing highlight |

Ocean navy carries *jerung*; ember carries *pyro*. Every widget below is themed to these
same six values so the page reads as one designed surface rather than a pile of
third-party cards.

## Anatomy

```
┌────────────────────────────────────────┐
│  animated SVG banner (assets/banner.svg)│
│   ◢◤   J E R U N G P Y R O              │
│  ◣◥◢◤  Software Engineer                │
│        ~~~~~~ drifting waves ~~~~~~     │
└────────────────────────────────────────┘
   [LinkedIn] [Instagram] [Email] [views]

   typing-SVG: rotating taglines

   ▸ SURFACING NOW — 3 featured projects

   ┌──────────────┬──────────────┐
   │  stats card  │  top langs   │
   └──────────────┴──────────────┘
   ┌──────────────────────────────┐
   │          trophies            │
   └──────────────────────────────┘

   ▾ Deeper waters  (collapsed <details>)

   ~~~~ contribution snake ~~~~
```

## Components

### 1. Banner — `assets/banner.svg`

Hand-authored animated SVG committed to the repo, referenced from the README as a
normal image.

- `viewBox="0 0 1200 300"`, `width="100%"` so it scales to any column width.
- Layered horizontal depth bands (abyss → deep → current) suggesting water column.
- Geometric shark silhouette, left third, in foam with a single ember eye.
- Wordmark `JERUNGPYRO`, wide letter-spacing, foam.
- Role line "Software Engineer" beneath in muted foam.
- Three wave paths drifting horizontally via SMIL `animateTransform`, staggered
  durations (8s / 11s / 14s) so the motion never visibly loops in sync.

**Depends on:** nothing. **Fallback:** if SMIL is ever stripped, it degrades to a
correct static banner — no broken layout.

### 2. Badge row

`shields.io` `for-the-badge` style, all tinted to the palette so they read as part of
the design rather than stock badges.

- LinkedIn → `https://www.linkedin.com/in/badrulakasyah`
- Instagram → `https://www.instagram.com/badrul_38`
- Email → `mailto:bakasyah@gmail.com`
- Profile views counter (`komarev.com/ghpvc`) — display only, not a link.

### 3. Typing animation

`readme-typing-svg` with the ember colour and a monospace face. Rotating lines, e.g.:

- `Software Engineer`
- `mobile · backend · security`
- `I ship things that people actually use`

### 4. Featured projects — "SURFACING NOW"

Three, each with an ember `▸` marker, one-line description, and tech tags:

1. **CampusResQ** — campus issue reporting; Flutter, Firebase, GPS, role-based access.
2. **FoodTruck Finder** — crowdsourced discovery with an admin web panel; Flutter, cloud.
3. **Task Manager** — full-stack; Flutter frontend, Laravel backend, web dashboard.

### 5. Stats widgets

`github-readme-stats` (stats + top languages) and `github-profile-trophy`, all themed
via explicit colour params rather than a preset theme name, so they match the banner
exactly. Stats and top-languages sit side by side in a two-column table; trophies span
full width beneath.

### 6. "Deeper waters" — collapsed

A `<details>` block holding the remaining repos, so the profile shows four things at
rest instead of twelve: Task Manager API, Crypto Value Tracker, EV Charger Finder,
Dividend Calculator, Personal Website.

### 7. Contribution snake — the only Action

`Platane/snk` on a cron schedule, writing the generated SVG to a dedicated `output`
branch and referenced from there.

This is the **only** moving part, deliberately. Rejected as YAGNI:

- **WakaTime stats** — needs a separate account and weeks of data before it says
  anything meaningful.
- **Blog-post auto-embed** — the owner does not currently blog.

One Action means exactly one thing that can ever send a failure email.

## Repository layout

A GitHub profile README only renders from a repo named **exactly** `jerungpyro/jerungpyro`,
with `README.md` at the root. The current `README2.md` in the KOWAJA working directory
renders nowhere.

```
jerungpyro/jerungpyro/
├── README.md
├── assets/
│   └── banner.svg
└── .github/
    └── workflows/
        └── snake.yml
```

## Accessibility

- Every image carries meaningful `alt` text; the banner's alt conveys the wordmark and
  role, not "banner".
- The palette's text pairs are checked against their backgrounds: foam `#A8DADC` on
  abyss `#0B1D2A` ≈ 11:1, ember `#FF6B35` on abyss ≈ 6.4:1 — both clear AA.
- Content is never conveyed by colour alone; the `▸` markers are literal characters.

## Success criteria

1. Profile renders correctly in both GitHub light and dark themes.
2. No dead links and no placeholder badges.
3. At rest the profile shows four projects, not twelve.
4. Nothing student-framed remains; the role reads "Software Engineer".
5. Exactly one GitHub Action.
6. Banner animates, and still reads correctly if animation is stripped.

## Out of scope

- Redesigning the individual project repos' READMEs.
- A personal website rebuild.
- Any change to KOWAJA.
