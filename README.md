# universal-ai-agent-kit

One `uv`-installable CLI (`uak`) that syncs a shared base kit of **skills, slash commands, MCP servers and engineering instructions** into every major coding CLI:

| Target      | Skills                      | Commands             | MCP                          | Instructions                         |
| ----------- | --------------------------- | -------------------- | ---------------------------- | ------------------------------------ |
| Claude Code | `~/.claude/skills`          | `~/.claude/commands` | `~/.claude.json`             | `~/.claude/CLAUDE.md`                |
| OpenCode    | `~/.config/opencode/skills` | `.../commands`       | `.../opencode.json`          | `.../AGENTS.md`                      |
| Codex       | `~/.codex/skills`           | `~/.codex/prompts`   | `~/.codex/config.toml`       | `~/.codex/AGENTS.md`                 |
| Copilot CLI | `~/.copilot/skills`         | – (not supported)    | `~/.copilot/mcp-config.json` | `~/.copilot/copilot-instructions.md` |

`--scope project` writes into the current repo instead (`.claude/`, `.opencode/`, `.agents/skills`, `.github/`, `AGENTS.md`, `CLAUDE.md`, `.mcp.json`, ...). Env overrides: `CLAUDE_CONFIG_DIR`, `OPENCODE_CONFIG_DIR`, `CODEX_HOME`, `COPILOT_HOME`.

## Install & use

```bash
uv tool install -e .          # editable: edits to the kit apply on next sync
# or without installing:  uvx --from . uak sync
# (a regular install bundles the kit into the wheel)

uak list                       # what's in the kit
uak sync -n                    # dry run
uak sync                       # sync to all CLIs (user scope)
uak sync -t claude -t codex    # only some targets
uak sync -s project            # install into the current repo
uak sync --only skills --only mcp   # only some kinds
uak --kit ~/my-kit sync        # use your own kit (same layout)
uak -v sync                    # debug logging
```

Sync is idempotent. Skills/commands owned by the kit are overwritten; MCP servers are merged by name into existing JSON (other entries untouched); instructions and Codex TOML are written inside marked blocks (`uak:begin/end`) so your own content is preserved.

## Skills & commands

> Keep these tables in sync with `skills/` and `commands/` (see `AGENTS.md`). Third-party provenance and licenses: [NOTICE.md](NOTICE.md).

### Skills

| Skill                                                                              | Description                                                                                                                                 | Source                                                                                                                                      |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [`brainstorming`](skills/brainstorming/SKILL.md)                                   | You MUST use this before any creative work - creating features, building components, adding functionality, modifying behavior, or planning… | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/brainstorming)                  |
| [`documentation`](skills/documentation/SKILL.md)                                   | Write or update READMEs, API docs, docstrings, ADRs and changelogs.                                                                         | first-party                                                                                                                                 |
| [`executing-plans`](skills/executing-plans/SKILL.md)                               | Use when executing an implementation plan in the current session as the implementer yourself — your human partner chose inline execution,…  | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/executing-plans)                |
| [`finishing-a-development-branch`](skills/finishing-a-development-branch/SKILL.md) | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work                                       | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/finishing-a-development-branch) |
| [`frontend-design`](skills/frontend-design/SKILL.md)                               | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one.                                      | [anthropics/skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/frontend-design)              |
| [`git-workflow`](skills/git-workflow/SKILL.md)                                     | Branching, Conventional Commit messages and pull request practices.                                                                         | first-party                                                                                                                                 |
| [`mcp-builder`](skills/mcp-builder/SKILL.md)                                       | Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through…           | [anthropics/skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/mcp-builder)                  |
| [`receiving-code-review`](skills/receiving-code-review/SKILL.md)                   | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable… | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/receiving-code-review)          |
| [`refactoring`](skills/refactoring/SKILL.md)                                       | Safely restructure code without changing behaviour.                                                                                         | first-party                                                                                                                                 |
| [`requesting-code-review`](skills/requesting-code-review/SKILL.md)                 | Use when completing tasks, implementing major features, or before merging to verify work meets requirements                                 | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/requesting-code-review)         |
| [`subagent-driven-development`](skills/subagent-driven-development/SKILL.md)       | Use when executing implementation plans with independent tasks in the current session                                                       | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/subagent-driven-development)    |
| [`systematic-debugging`](skills/systematic-debugging/SKILL.md)                     | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes                                                 | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging)           |
| [`test-driven-development`](skills/test-driven-development/SKILL.md)               | Use when implementing any feature or bugfix, before writing implementation code                                                             | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/test-driven-development)        |
| [`using-git-worktrees`](skills/using-git-worktrees/SKILL.md)                       | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated…  | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/using-git-worktrees)            |
| [`verification-before-completion`](skills/verification-before-completion/SKILL.md) | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands…    | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/verification-before-completion) |
| [`webapp-testing`](skills/webapp-testing/SKILL.md)                                 | Toolkit for interacting with and testing local web applications using Playwright.                                                           | [anthropics/skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/webapp-testing)               |
| [`writing-plans`](skills/writing-plans/SKILL.md)                                   | Use when you have a spec or requirements for a multi-step task, before touching code                                                        | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/writing-plans)                  |

### Commands

| Command                                 | Description                                                          | Skills used               |
| --------------------------------------- | -------------------------------------------------------------------- | ------------------------- |
| [`/brainstorm`](commands/brainstorm.md) | Explore requirements and design before implementing                  | `brainstorming`           |
| [`/commit`](commands/commit.md)         | Create a Conventional Commit from current changes                    | `git-workflow`            |
| [`/debug`](commands/debug.md)           | Root-cause and fix a bug or failing test                             | `systematic-debugging`    |
| [`/docs`](commands/docs.md)             | Write or update documentation for recent changes                     | `documentation`           |
| [`/plan`](commands/plan.md)             | Write an implementation plan for a task before coding                | `writing-plans`           |
| [`/pr`](commands/pr.md)                 | Prepare a pull request title and description from the current branch | `git-workflow`            |
| [`/refactor`](commands/refactor.md)     | Refactor code safely without changing behaviour                      | `refactoring`             |
| [`/review`](commands/review.md)         | Review current changes (or a given PR/branch) for bugs and quality   | `requesting-code-review`  |
| [`/tdd`](commands/tdd.md)               | Implement a feature or fix using test-driven development             | `test-driven-development` |

## Kit layout (repo root)

```
skills/<name>/SKILL.md   # see NOTICE.md: 14 imported from obra/superpowers + anthropics/skills,
                         # plus first-party git-workflow, refactoring, documentation
commands/<name>.md       # /plan /brainstorm /review /commit /pr /tdd /debug /refactor /docs
mcps/stdio.json          # local servers: context7, fetch, playwright
mcps/http.json           # hosted (streamable HTTP) servers: atlassian
mcps/sse.json            # hosted legacy SSE servers (none by default)
AGENTS.md                # shared engineering principles
```

Add a skill by creating `skills/<name>/SKILL.md` (frontmatter `name`, `description`), a command by dropping a `.md` file in `commands/`, an MCP server in `mcps/` (see below), then run `uak sync`.

## Adding MCP servers

MCP servers are split by transport, one file each in `mcps/`. Each file maps a server name to its spec; names must be unique across files.

| File         | Transport               | Required  | Optional                     |
| ------------ | ----------------------- | --------- | ---------------------------- |
| `stdio.json` | local process           | `command` | `args`, `env`, `description` |
| `http.json`  | hosted, streamable HTTP | `url`     | `headers`, `description`     |
| `sse.json`   | hosted, legacy SSE      | `url`     | `headers`, `description`     |

Hosted example (`mcps/http.json`), e.g. Atlassian:

```json
{
  "atlassian": { "description": "Jira and Confluence", "url": "https://mcp.atlassian.com/v2/mcp" }
}
```

Local example (`mcps/stdio.json`):

```json
{ "context7": { "command": "npx", "args": ["-y", "@upstash/context7-mcp@latest"] } }
```

Then `uak sync --only mcp` (add `-n` to preview).

Per-CLI mapping: Claude/Copilot write `type: http|sse`; OpenCode writes `type: remote` for both; Codex supports `stdio` and `http` only (SSE servers are skipped with a warning).

**Authentication.** Most hosted servers (including Atlassian) use OAuth: after syncing, authenticate once inside each CLI (Claude: `/mcp`; Codex: `codex mcp login atlassian`; OpenCode: `opencode mcp auth atlassian`; Copilot: `/mcp`). Avoid putting tokens in `headers`: values are written literally into each CLI's config file, so if you must use one, keep it in a private, uncommitted custom kit (`--kit`).

## Project layout

```
skills/ commands/ mcps/ AGENTS.md   (content you edit)
uak/    cli.py (typer UI) · targets.py (per-CLI adapters) · kit.py
```

## Notes

- MCP servers need `npx` (Node) and `uvx` available. Codex: don't define the same server name outside the managed block in `config.toml` (duplicate TOML tables).
- OpenCode's `opencode.json` must be plain JSON (no comments) for merging.
- Project-scope MCP for Copilot CLI is skipped (user-level only).

## Development

Formatting and linting run through [prek](https://github.com/j178/prek) (config: `prek.toml`): ruff (lint + format), end-of-file, trailing whitespace, JSON and Markdown formatting.

```bash
uv sync                      # installs prek + ruff (dev group)
uv run prek install          # run on every commit
uv run prek run --all-files  # run manually
```
