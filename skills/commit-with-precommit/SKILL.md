---
name: commit-with-precommit
description: Commit in repos that use prek or pre-commit. Use when committing and the repo root has prek.toml, .pre-commit-config.yaml or .pre-commit-config.yml, so hooks are run on all files before the commit.
metadata:
  source: first-party
---

# Commit with pre-commit

Follow `git-workflow` for the commit itself. This skill adds one step before it.

1. **Detect** a hook config at the repo root (`git rev-parse --show-toplevel`): `prek.toml`, `.pre-commit-config.yaml` or `.pre-commit-config.yml`. If none exists, skip this skill.
1. **Pick the runner**: `prek` if available (`uv run prek`, `prek` or `uvx prek`), otherwise `pre-commit`. Prefer the project's own wrapper if documented (README, `AGENTS.md`, CI).
1. **Run all files before committing**: `prek run --all-files` (or `pre-commit run --all-files`). Not just the staged files, so CI sees the same result.
1. **Hooks that modify files** (formatters, end-of-file fixers) make the run fail. Review `git diff`, stage the fixes that belong to the change, and re-run until it passes. Never stage unrelated reformatting.
1. **Commit once green.** Do not bypass hooks (`--no-verify`, `SKIP=...`) unless the user explicitly asks, and say so if a hook failed for a reason you could not fix.
