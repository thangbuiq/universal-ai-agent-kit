# universal-ai-agent-kit

Keep one set of **skills, slash commands, MCP servers and engineering rules**, and sync it into Claude Code, OpenCode, Codex and GitHub Copilot CLI with a single command (`uak`).

## Quick start

```bash
uv tool install -e .   # editable: kit edits apply on the next sync
uak sync -n            # dry run: see what would change
uak sync               # install into all supported CLIs
```

No install needed: `uvx --from . uak sync`. A regular (non-editable) install bundles the kit into the wheel.

## Supported CLIs

| CLI         | Skills | Commands | MCP servers | Instructions |
| ----------- | :----: | :------: | :---------: | :----------: |
| Claude Code |   ✅   |    ✅    |     ✅      |      ✅      |
| OpenCode    |   ✅   |    ✅    |     ✅      |      ✅      |
| Codex       |   ✅   |    ✅    |     ✅      |      ✅      |
| Copilot CLI |   ✅   |    –     |     ✅      |      ✅      |

<details>
<summary>Where files are written (user scope)</summary>

| CLI         | Skills                      | Commands             | MCP                          | Instructions                         |
| ----------- | --------------------------- | -------------------- | ---------------------------- | ------------------------------------ |
| Claude Code | `~/.claude/skills`          | `~/.claude/commands` | `~/.claude.json`             | `~/.claude/CLAUDE.md`                |
| OpenCode    | `~/.config/opencode/skills` | `.../commands`       | `.../opencode.json`          | `.../AGENTS.md`                      |
| Codex       | `~/.codex/skills`           | `~/.codex/prompts`   | `~/.codex/config.toml`       | `~/.codex/AGENTS.md`                 |
| Copilot CLI | `~/.copilot/skills`         | – (not supported)    | `~/.copilot/mcp-config.json` | `~/.copilot/copilot-instructions.md` |

Env overrides: `CLAUDE_CONFIG_DIR`, `OPENCODE_CONFIG_DIR`, `CODEX_HOME`, `COPILOT_HOME`.

`--scope project` writes into the current repo instead (`.claude/`, `.opencode/`, `.agents/skills`, `.github/`, `AGENTS.md`, `CLAUDE.md`, `.mcp.json`, ...).

</details>

## Usage

| Goal                      | Command                             |
| ------------------------- | ----------------------------------- |
| See what the kit contains | `uak list`                          |
| Preview without writing   | `uak sync -n`                       |
| Sync everything           | `uak sync`                          |
| Only some CLIs            | `uak sync -t claude -t codex`       |
| Only some kinds           | `uak sync --only skills --only mcp` |
| Install into this repo    | `uak sync -s project`               |
| Replace without asking    | `uak sync --overwrite`              |
| Use your own kit          | `uak --kit ~/my-kit sync`           |
| Debug logging             | `uak -v sync`                       |

Kinds are `skills`, `commands`, `mcp`, `instructions`; targets are `claude`, `opencode`, `codex`, `copilot`.

Sync is idempotent and safe to re-run:

- Anything identical to what is already installed is left alone.
- If a skill, command, MCP server or instructions file already exists and differs, `uak` asks `Overwrite? [y/N]` before replacing it. Pass `--overwrite` to replace without asking. With no terminal (CI, pipes) conflicts are skipped unless `--overwrite` is set.
- MCP servers are merged by name into existing JSON; your other entries are untouched, and only a server with the same name but a different spec triggers a prompt.
- Instructions and Codex TOML are written inside marked blocks (`uak:begin/end`), so your own content outside the block is preserved.

## What's in the kit

Third-party provenance and licenses: [NOTICE.md](NOTICE.md).

### Skills

| Skill                                                                              | What it does                                                                                  | Source                                                                                                                                      |
| ---------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [`brainstorming`](skills/brainstorming/SKILL.md)                                   | Explore requirements and design before building anything new                                  | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/brainstorming)                  |
| [`commit-with-precommit`](skills/commit-with-precommit/SKILL.md)                   | Run `prek`/`pre-commit run --all-files` before committing, if the repo root has a hook config | first-party                                                                                                                                 |
| [`documentation`](skills/documentation/SKILL.md)                                   | Write or update READMEs, API docs, docstrings, ADRs, changelogs                               | first-party                                                                                                                                 |
| [`executing-plans`](skills/executing-plans/SKILL.md)                               | Carry out a written plan inline, task by task                                                 | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/executing-plans)                |
| [`finishing-a-development-branch`](skills/finishing-a-development-branch/SKILL.md) | Decide how to integrate finished work (merge, PR, cleanup)                                    | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/finishing-a-development-branch) |
| [`frontend-design`](skills/frontend-design/SKILL.md)                               | Distinctive, intentional UI design instead of templated defaults                              | [anthropics/skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/frontend-design)              |
| [`git-workflow`](skills/git-workflow/SKILL.md)                                     | Branching, Conventional Commits and pull request practices                                    | first-party                                                                                                                                 |
| [`mcp-builder`](skills/mcp-builder/SKILL.md)                                       | Build high-quality MCP servers in Python or TypeScript                                        | [anthropics/skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/mcp-builder)                  |
| [`receiving-code-review`](skills/receiving-code-review/SKILL.md)                   | Verify review feedback technically before applying it                                         | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/receiving-code-review)          |
| [`refactoring`](skills/refactoring/SKILL.md)                                       | Restructure code safely without changing behaviour                                            | first-party                                                                                                                                 |
| [`requesting-code-review`](skills/requesting-code-review/SKILL.md)                 | Review work against requirements before merging                                               | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/requesting-code-review)         |
| [`subagent-driven-development`](skills/subagent-driven-development/SKILL.md)       | Run plans with independent tasks through subagents                                            | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/subagent-driven-development)    |
| [`systematic-debugging`](skills/systematic-debugging/SKILL.md)                     | Find the root cause before proposing a fix                                                    | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/systematic-debugging)           |
| [`test-driven-development`](skills/test-driven-development/SKILL.md)               | Write the failing test first, then the code                                                   | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/test-driven-development)        |
| [`using-git-worktrees`](skills/using-git-worktrees/SKILL.md)                       | Isolate feature work in its own worktree                                                      | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/using-git-worktrees)            |
| [`verification-before-completion`](skills/verification-before-completion/SKILL.md) | Run the checks and read the output before claiming done                                       | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/verification-before-completion) |
| [`webapp-testing`](skills/webapp-testing/SKILL.md)                                 | Test local web apps with Playwright                                                           | [anthropics/skills](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/webapp-testing)               |
| [`writing-plans`](skills/writing-plans/SKILL.md)                                   | Turn a spec into a step-by-step implementation plan                                           | [obra/superpowers](https://github.com/obra/superpowers/tree/bb92a77741419a4ab5f06e711a283343f1ada0c3/skills/writing-plans)                  |

### Commands

| Command                                 | What it does                                                         | Skill used                |
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

### MCP servers

| Server       | Transport     | File              |
| ------------ | ------------- | ----------------- |
| `context7`   | local (stdio) | `mcps/stdio.json` |
| `fetch`      | local (stdio) | `mcps/stdio.json` |
| `playwright` | local (stdio) | `mcps/stdio.json` |
| `atlassian`  | hosted (HTTP) | `mcps/http.json`  |

## Customize the kit

Add something, then run `uak sync`:

| To add a... | Do this                                                                   |
| ----------- | ------------------------------------------------------------------------- |
| Skill       | Create `skills/<name>/SKILL.md` with `name` and `description` frontmatter |
| Command     | Drop a `.md` file in `commands/`                                          |
| MCP server  | Add an entry to a file in `mcps/` (below)                                 |

### MCP servers

One file per transport in `mcps/`. Each maps a server name to its spec; names must be unique across files.

| File         | Transport               | Required  | Optional                     |
| ------------ | ----------------------- | --------- | ---------------------------- |
| `stdio.json` | local process           | `command` | `args`, `env`, `description` |
| `http.json`  | hosted, streamable HTTP | `url`     | `headers`, `description`     |
| `sse.json`   | hosted, legacy SSE      | `url`     | `headers`, `description`     |

```json
{ "context7": { "command": "npx", "args": ["-y", "@upstash/context7-mcp@latest"] } }
```

```json
{ "atlassian": { "description": "Jira and Confluence", "url": "https://mcp.atlassian.com/v2/mcp" } }
```

Preview with `uak sync --only mcp -n`.

- **Per-CLI mapping:** Claude and Copilot write `type: http|sse`; OpenCode writes `type: remote` for both; Codex supports `stdio` and `http` only (SSE servers are skipped with a warning).
- **Authentication:** most hosted servers (including Atlassian) use OAuth. After syncing, authenticate once inside each CLI (Claude: `/mcp`; Codex: `codex mcp login atlassian`; OpenCode: `opencode mcp auth atlassian`; Copilot: `/mcp`). Avoid tokens in `headers`: values are written literally into each CLI's config file. If you must, keep them in a private, uncommitted custom kit (`--kit`).

## Project layout

```
.
├── .github
│   └── workflows
├── commands
│   ├── <name>.md
│   └── ...
├── mcps
│   ├── http.json
│   ├── sse.json
│   └── stdio.json
├── skills
│   ├── <name>
│   │   └── SKILL.md
│   └── ...
├── uak
│   ├── __init__.py
│   ├── cli.py
│   ├── kit.py
│   └── targets.py
├── AGENTS.md
├── NOTICE.md
├── README.md
├── prek.toml
└── pyproject.toml
```

## Notes

- MCP servers need `npx` (Node) and `uvx` available.
- Codex: don't define the same server name outside the managed block in `config.toml` (duplicate TOML tables).
- OpenCode's `opencode.json` must be plain JSON (no comments) for merging.
- Project-scope MCP for Copilot CLI is skipped (user-level only).

## Development

Formatting and linting run through [prek](https://github.com/j178/prek) (config: `prek.toml`): ruff (lint + format), end-of-file, trailing whitespace, JSON and Markdown formatting. CI runs the same check on every PR to `main` and on pushes to `main`.

```bash
uv sync                      # installs prek + ruff (dev group)
uv run prek install          # run on every commit
uv run prek run --all-files  # run manually
```
