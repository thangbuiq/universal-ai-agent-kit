import json

from uak.targets import Writer, _merge_json


def make(tmp_path, **kw):
    asked = []

    def confirm(msg):
        asked.append(msg)
        return kw.pop("answer", False)

    return Writer(kw.pop("dry_run", False), kw.pop("overwrite", False), kw.pop("confirm", confirm)), asked


def skill(root, body):
    (root / "sub").mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text(body)
    (root / "sub" / "x.txt").write_text(body)
    return root


def test_new_dir_is_copied_without_asking(tmp_path):
    w, asked = make(tmp_path)
    w.copy_dir(skill(tmp_path / "src", "a"), tmp_path / "dst", "skill s")
    assert (tmp_path / "dst" / "SKILL.md").read_text() == "a"
    assert asked == []


def test_identical_dir_is_not_asked_about(tmp_path):
    w, asked = make(tmp_path)
    src = skill(tmp_path / "src", "a")
    skill(tmp_path / "dst", "a")
    w.copy_dir(src, tmp_path / "dst", "skill s")
    assert asked == []


def test_changed_dir_prompts_and_keeps_on_no(tmp_path):
    w, asked = make(tmp_path, answer=False)
    src = skill(tmp_path / "src", "new")
    skill(tmp_path / "dst", "old")
    w.copy_dir(src, tmp_path / "dst", "skill s")
    assert len(asked) == 1
    assert (tmp_path / "dst" / "SKILL.md").read_text() == "old"


def test_changed_dir_replaced_on_yes(tmp_path):
    w, _ = make(tmp_path, answer=True)
    src = skill(tmp_path / "src", "new")
    skill(tmp_path / "dst", "old")
    w.copy_dir(src, tmp_path / "dst", "skill s")
    assert (tmp_path / "dst" / "SKILL.md").read_text() == "new"


def test_overwrite_flag_skips_prompt(tmp_path):
    w, asked = make(tmp_path, overwrite=True)
    src = skill(tmp_path / "src", "new")
    skill(tmp_path / "dst", "old")
    w.copy_dir(src, tmp_path / "dst", "skill s")
    assert asked == []
    assert (tmp_path / "dst" / "SKILL.md").read_text() == "new"


def test_no_terminal_skips_conflicts(tmp_path):
    w = Writer(False, False, None)
    f = tmp_path / "AGENTS.md"
    f.write_text("mine")
    w.text(f, "kit", "instructions")
    assert f.read_text() == "mine"


def test_dry_run_never_writes(tmp_path):
    w, asked = make(tmp_path, dry_run=True)
    f = tmp_path / "c.md"
    f.write_text("old")
    src = tmp_path / "src.md"
    src.write_text("new")
    w.copy_file(src, f, "command /c")
    assert f.read_text() == "old"
    assert asked == []


def test_mcp_merge_only_asks_about_clashing_servers(tmp_path):
    path = tmp_path / "claude.json"
    path.write_text(json.dumps({"theme": "dark", "mcpServers": {"mine": {"a": 1}, "kit": {"a": 1}}}))
    w, asked = make(tmp_path, answer=False)
    _merge_json(w, path, "mcpServers", {"kit": {"a": 2}, "fresh": {"a": 3}})
    data = json.loads(path.read_text())
    assert len(asked) == 1 and "kit" in asked[0] and "fresh" not in asked[0]
    assert data["mcpServers"] == {"mine": {"a": 1}, "kit": {"a": 1}, "fresh": {"a": 3}}
    assert data["theme"] == "dark"


def test_mcp_merge_overwrites_clash_on_yes(tmp_path):
    path = tmp_path / "claude.json"
    path.write_text(json.dumps({"mcpServers": {"kit": {"a": 1}}}))
    w, _ = make(tmp_path, answer=True)
    _merge_json(w, path, "mcpServers", {"kit": {"a": 2}})
    assert json.loads(path.read_text())["mcpServers"]["kit"] == {"a": 2}
