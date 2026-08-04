# START HERE

This folder will become **`github.com/jerungpyro/jerungpyro`** — the special repo whose
`README.md` renders on the GitHub profile page. It is not related to any other project.

## State: built (2026-08-04)

All three deliverables exist and `python tools/check_profile.py --links` passes.

- `docs/DESIGN.md` — the approved spec. **Read this first.**
- `docs/superpowers/plans/2026-08-04-github-profile-readme.md` — the implementation
  plan, amended in place with what changed during execution and why.
- `docs/old-readme-source.md` — the previous plain README. Source of project
  descriptions and links only; its framing is outdated (see below).
- `tools/check_profile.py` — dev-only verification. Run it after any edit.

The three open questions below were answered before building: stack gains React,
TypeScript, Python, FastAPI **and Capacitor**; the drafted taglines were kept; the
featured/collapsed project split was confirmed as designed.

## Known follow-up

The design's stats widgets (`github-readme-stats`, `github-profile-trophy`) are both
dead — the Vercel deployments return `DEPLOYMENT_PAUSED` and `DEPLOYMENT_DISABLED`.
They were replaced with `streak-stats.demolab.com` and
`github-readme-activity-graph`, both live and themable to the full palette. The
top-languages card and trophy row are the casualties; self-hosting either project on
a personal Vercel account brings them back with the same query params. Details in the
plan's Task 5.

The snake image 404s until the Action has run once — trigger it from the Actions tab.

## Facts the design depends on

| | |
|---|---|
| GitHub | `jerungpyro` |
| Wordmark | `JERUNGPYRO` |
| Real name | Badrul Akasyah |
| Role line | `Software Engineer` — **no employer named**, on purpose |
| LinkedIn | https://www.linkedin.com/in/badrulakasyah |
| Instagram | https://www.instagram.com/badrul_38 |
| Email | bakasyah@gmail.com |

**`jerungpyro`** = Malay *jerung* (shark) + *pyro* (fire). The whole visual direction is
built on this: ocean navy for the shark, ember orange for the fire.

## Outdated framing to avoid

`docs/old-readme-source.md` describes a "final-year Netcentric student". **That is no
longer true — he is employed as a software engineer.** Do not reuse that framing. These
repos were deliberately dropped and must not come back: OOP Assignments, CPP
Assignments, ICPROM-25, Tic Tac Toe.

## Open questions to confirm before building

1. **Stack list.** The design assumes React, TypeScript, Python and FastAPI get added
   alongside the existing Flutter / Laravel / Firebase / Dart / Kotlin. Confirm this is
   his to claim.
2. **Taglines.** The rotating lines in the typing animation are placeholder wording
   invented during design (`mobile · backend · security`, `I ship things that people
   actually use`). They should be rewritten in his own voice.
3. **Featured three.** CampusResQ, FoodTruck Finder, Task Manager are surfaced;
   Task Manager API and Crypto Value Tracker were demoted to the collapsed section.
   Confirm that split.

## Publishing

The repo must be named **exactly** `jerungpyro` (same as the username) and be **public**,
with `README.md` at the root. Any other name renders nowhere. It does not exist on
GitHub yet — it needs creating, and this folder has a fresh `git init` with no remote.
