## Engineering principles (universal-ai-agent-kit)

- Understand before changing: read the relevant code, tests and docs first. Never guess APIs; check the source or use the `context7` MCP for library docs.
- Plan non-trivial work (`brainstorming`, `writing-plans`) and keep changes small, focused and reversible.
- Write or update tests with every behaviour change (`test-driven-development`). Run the project's test, lint and type-check commands before declaring work done.
- Verify before claiming done (`verification-before-completion`). Debug from evidence, not hunches (`systematic-debugging`). Find the root cause before fixing.
- Match the surrounding code's style, naming and comment density. Do not add unrequested features or refactors.
- Never write em dashes (U+2014) in code, comments, docs, commit messages or replies; use a hyphen (-), comma or colon instead.
- Never commit secrets. Treat all external input as untrusted.
- Use Conventional Commits and small PRs (`git-workflow`). Do not push, force-push or run destructive commands without explicit approval.
- Report outcomes honestly: if tests fail or a step was skipped, say so.

<!-- uak:ignore-begin -->

## Maintaining this repo

This section is for contributors to this repo and is **not** synced to users' CLIs.

- Read `README.md` first for context (project layout, skills/commands tables, how syncing works) before exploring or editing anything in this repo, and keep it current as you work.

- Whenever a skill or command is added, renamed, removed or its description changes, update the **Skills** / **Commands** tables in `README.md` (name linked to its file, description, source).

- Every `skills/<name>/SKILL.md` must carry a `metadata.source` frontmatter entry: the upstream URL (pinned to a commit) for imported skills, or `first-party`. Record third-party skills and their licenses in `NOTICE.md`.

- Imported skills stay unchanged from upstream apart from the `metadata.source` entry and em dashes (U+2014) replaced with a hyphen (-), and are excluded from the formatters in `prek.toml`. Add new vendored skills to that `exclude` list.

- Run `uv run prek run --all-files` before committing.

<!-- uak:ignore-end -->
