"""Per-CLI adapters: where each coding CLI keeps skills, commands, MCP config and instructions."""

from __future__ import annotations

import json
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from loguru import logger

from .kit import Kit

MD_MARK = ("<!-- uak:begin -->", "<!-- uak:end -->")
TOML_MARK = ("# >>> uak managed >>>", "# <<< uak managed <<<")


class SyncError(Exception):
    pass


class Writer:
    """Filesystem access that honours --dry-run."""

    def __init__(self, dry_run: bool):
        self.dry_run = dry_run

    def text(self, path: Path, content: str, what: str) -> None:
        logger.info("{} -> {}", what, path)
        if not self.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)

    def copy_dir(self, src: Path, dst: Path, what: str) -> None:
        logger.info("{} -> {}", what, dst)
        if not self.dry_run:
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)

    def copy_file(self, src: Path, dst: Path, what: str) -> None:
        logger.info("{} -> {}", what, dst)
        if not self.dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def _block(text: str, mark: tuple[str, str], body: str) -> str:
    begin, end = mark
    new = f"{begin}\n{body}\n{end}"
    pat = re.compile(re.escape(begin) + r".*?" + re.escape(end), re.S)
    if pat.search(text):
        return pat.sub(lambda _: new, text)
    return (text.rstrip() + "\n\n" if text.strip() else "") + new + "\n"


def _read(path: Path) -> str:
    return path.read_text() if path.exists() else ""


def _merge_json(w: Writer, path: Path, key: str, servers: dict, schema: str | None = None) -> None:
    try:
        data = json.loads(_read(path) or "{}")
    except json.JSONDecodeError as e:
        raise SyncError(f"{path} is not plain JSON ({e.msg}, line {e.lineno}); remove comments and retry") from e
    if schema:
        data.setdefault("$schema", schema)
    data.setdefault(key, {}).update(servers)
    w.text(path, json.dumps(data, indent=2) + "\n", f"mcp [{', '.join(servers)}]")


def _toml(servers: dict) -> str:
    q = json.dumps  # JSON strings are valid TOML basic strings
    out: list[str] = []
    for name, s in servers.items():
        out.append(f"[mcp_servers.{q(name)}]")
        if s["transport"] == "http":
            out.append(f"url = {q(s['url'])}")
            if s.get("headers"):
                out.append(f"[mcp_servers.{q(name)}.http_headers]")
                out += [f"{k} = {q(v)}" for k, v in s["headers"].items()]
            continue
        out += [f"command = {q(s['command'])}", "args = [" + ", ".join(q(a) for a in s.get("args", [])) + "]"]
        if s.get("env"):
            out.append(f"[mcp_servers.{q(name)}.env]")
            out += [f"{k} = {q(v)}" for k, v in s["env"].items()]
    return "\n".join(out)


@dataclass(frozen=True)
class Paths:
    skills: Path
    instructions: Path
    mcp: Path | None = None
    commands: Path | None = None


class Target:
    key = ""
    label = ""

    def __init__(self, user: Paths, project: Paths):
        self._paths = {"user": user, "project": project}

    def sync(self, kit: Kit, scope: str, kinds: set[str], w: Writer) -> None:
        p = self._paths[scope]
        if "skills" in kinds:
            for s in kit.skills:
                w.copy_dir(s, p.skills / s.name, f"skill {s.name}")
        if "commands" in kinds:
            if p.commands is None:
                logger.warning("commands are not supported at {} scope; skipped", scope)
            else:
                for c in kit.commands:
                    w.copy_file(c, p.commands / c.name, f"command /{c.stem}")
        if "mcp" in kinds and kit.mcp:
            if p.mcp is None:
                logger.warning("mcp is not supported at {} scope; skipped", scope)
            else:
                self.write_mcp(w, p.mcp, kit.mcp)
        if "instructions" in kinds and kit.instructions:
            w.text(p.instructions, _block(_read(p.instructions), MD_MARK, kit.instructions), "instructions")

    def write_mcp(self, w: Writer, path: Path, servers: dict) -> None:
        raise NotImplementedError


class Claude(Target):
    key, label = "claude", "Claude Code"

    def write_mcp(self, w, path, servers):
        def spec(s):
            if s["transport"] == "stdio":
                return {"type": "stdio", "command": s["command"], "args": s.get("args", []), "env": s.get("env", {})}
            return {"type": s["transport"], "url": s["url"], "headers": s.get("headers", {})}

        _merge_json(w, path, "mcpServers", {n: spec(s) for n, s in servers.items()})


class OpenCode(Target):
    key, label = "opencode", "OpenCode"

    def write_mcp(self, w, path, servers):
        def spec(s):
            if s["transport"] == "stdio":
                return {
                    "type": "local",
                    "command": [s["command"], *s.get("args", [])],
                    "environment": s.get("env", {}),
                    "enabled": True,
                }
            return {"type": "remote", "url": s["url"], "headers": s.get("headers", {}), "enabled": True}

        _merge_json(w, path, "mcp", {n: spec(s) for n, s in servers.items()}, schema="https://opencode.ai/config.json")


class Codex(Target):
    key, label = "codex", "Codex"

    def write_mcp(self, w, path, servers):
        ok = {}
        for n, s in servers.items():
            if s["transport"] == "sse":
                logger.warning("mcp '{}': Codex does not support SSE transport; skipped", n)
            else:
                ok[n] = s
        if ok:
            w.text(path, _block(_read(path), TOML_MARK, _toml(ok)), f"mcp [{', '.join(ok)}]")


class Copilot(Target):
    key, label = "copilot", "GitHub Copilot CLI"

    def write_mcp(self, w, path, servers):
        def spec(s):
            if s["transport"] == "stdio":
                return {
                    "type": "local",
                    "command": s["command"],
                    "args": s.get("args", []),
                    "env": s.get("env", {}),
                    "tools": ["*"],
                }
            return {"type": s["transport"], "url": s["url"], "headers": s.get("headers", {}), "tools": ["*"]}

        _merge_json(w, path, "mcpServers", {n: spec(s) for n, s in servers.items()})


def build_targets(project: Path) -> dict[str, Target]:
    home, env = Path.home(), os.environ.get
    cl = Path(env("CLAUDE_CONFIG_DIR", home / ".claude"))
    oc = Path(env("OPENCODE_CONFIG_DIR", home / ".config" / "opencode"))
    cx = Path(env("CODEX_HOME", home / ".codex"))
    cp = Path(env("COPILOT_HOME", home / ".copilot"))
    targets = [
        Claude(
            Paths(cl / "skills", cl / "CLAUDE.md", home / ".claude.json", cl / "commands"),
            Paths(
                project / ".claude/skills", project / "CLAUDE.md", project / ".mcp.json", project / ".claude/commands"
            ),
        ),
        OpenCode(
            Paths(oc / "skills", oc / "AGENTS.md", oc / "opencode.json", oc / "commands"),
            Paths(
                project / ".opencode/skills",
                project / "AGENTS.md",
                project / "opencode.json",
                project / ".opencode/commands",
            ),
        ),
        Codex(
            Paths(cx / "skills", cx / "AGENTS.md", cx / "config.toml", cx / "prompts"),
            Paths(project / ".agents/skills", project / "AGENTS.md", project / ".codex/config.toml"),
        ),
        Copilot(
            Paths(cp / "skills", cp / "copilot-instructions.md", cp / "mcp-config.json"),
            Paths(project / ".github/skills", project / ".github/copilot-instructions.md"),
        ),
    ]
    return {t.key: t for t in targets}
