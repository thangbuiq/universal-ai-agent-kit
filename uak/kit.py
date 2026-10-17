"""Kit discovery: skills, commands, MCP servers and shared instructions."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

# MCP transport -> the field every server of that transport must define.
TRANSPORTS = {"stdio": "command", "http": "url", "sse": "url"}

# Repo-maintenance notes in AGENTS.md that must not be synced to users.
_IGNORED = re.compile(r"<!-- uak:ignore-begin -->.*?<!-- uak:ignore-end -->\s*", re.S)

_HERE = Path(__file__).parent
# Repo checkout / editable install: the repo root. Regular install: bundled uak/kit.
DEFAULT_KIT = _HERE.parent if (_HERE.parent / "skills").is_dir() else _HERE / "kit"


@dataclass(frozen=True)
class Kit:
    root: Path

    @property
    def skills(self) -> list[Path]:
        d = self.root / "skills"
        return sorted(p for p in d.iterdir() if (p / "SKILL.md").is_file()) if d.is_dir() else []

    @property
    def commands(self) -> list[Path]:
        return sorted((self.root / "commands").glob("*.md"))

    @property
    def mcp(self) -> dict[str, dict]:
        """All MCP servers from mcps/{stdio,http,sse}.json, each tagged with its transport."""
        servers: dict[str, dict] = {}
        for transport, required in TRANSPORTS.items():
            f = self.root / "mcps" / f"{transport}.json"
            if not f.is_file():
                continue
            for name, spec in json.loads(f.read_text()).items():
                if name in servers:
                    raise ValueError(f"mcp server '{name}' is defined twice (see {f.name})")
                if required not in spec:
                    raise ValueError(f"mcps/{f.name}: '{name}' needs a '{required}' field")
                servers[name] = {**spec, "transport": transport}
        return servers

    @property
    def instructions(self) -> str:
        f = self.root / "AGENTS.md"
        return _IGNORED.sub("", f.read_text()).strip() if f.is_file() else ""

    @staticmethod
    def describe(skill: Path) -> str:
        m = re.search(r"^description:\s*(.+)$", (skill / "SKILL.md").read_text(), re.M)
        return m.group(1) if m else ""
