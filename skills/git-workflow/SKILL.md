---
name: git-workflow
description: Branching, Conventional Commit messages and pull request practices. Use when committing, creating branches, writing PR descriptions, or cleaning up history.
metadata:
  source: first-party
---

# Git Workflow

**Before committing**: `git status`, `git diff`; stage only related files; ensure no secrets or build artifacts; run tests/lint.

**Branches**: never commit directly to the default branch. Name `type/short-description` (`feat/login-rate-limit`, `fix/null-user`).

**Commits** – Conventional Commits, imperative mood, subject ≤ 72 chars:

```
<type>(<scope>): <summary>

<why this change, not what; wrap at 72>

BREAKING CHANGE: <if any>
```

Types: `feat fix docs style refactor perf test build ci chore revert`. One logical change per commit.

Do not co-author commits. Use `git commit --amend --reset-author` to fix author if needed.

**Pull requests**: small and focused. Description includes *Summary* (what and why), *Changes*, *Testing* (commands run and results), *Risks/Rollout*, and linked issues. Self-review the diff first (`requesting-code-review`).

**Safety**: do not push, force-push, rewrite shared history, `reset --hard` or delete branches without explicit approval. Prefer `git revert` for published commits and `--force-with-lease` when a force push is approved. Resolve conflicts by understanding both sides, then run tests.
