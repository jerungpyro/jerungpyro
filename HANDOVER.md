# START HERE

This folder will become **`github.com/jerungpyro/jerungpyro`** — the special repo whose
`README.md` renders on the GitHub profile page. It is not related to any other project.

## State: design approved, nothing built yet

- `docs/DESIGN.md` — the full approved spec. **Read this first.**
- `docs/old-readme-source.md` — the previous plain README. Source of project
  descriptions and links only; its framing is outdated (see below).
- `assets/` and `.github/workflows/` — created empty, ready for `banner.svg` and
  `snake.yml`.

## Next step

Create the implementation plan from `docs/DESIGN.md` (superpowers `writing-plans`),
then build the three deliverables:

1. `README.md`
2. `assets/banner.svg` — hand-authored animated SVG
3. `.github/workflows/snake.yml` — the single GitHub Action

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
