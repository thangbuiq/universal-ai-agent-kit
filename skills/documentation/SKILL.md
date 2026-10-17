---
name: documentation
description: Write or update READMEs, API docs, docstrings, ADRs and changelogs. Use when behaviour, setup or public interfaces change, or when docs are missing or stale.
metadata:
  source: first-party
---

# Documentation

- **Find existing docs first** and update them in place; keep tone and format consistent.
- **README**: what it is, quick start (copy-pasteable, verified commands), usage examples, configuration, development/testing, contributing. Run the commands you document.
- **Code docs**: public APIs get docstrings (purpose, params, returns, raises, example). Comments explain *why*, not *what*.
- **ADRs** for significant decisions: context, decision, alternatives, consequences.
- **Changelog**: Keep a Changelog format (Added/Changed/Fixed/Removed), user-facing wording, note breaking changes and migrations.
- Prefer short sentences, concrete examples, and diagrams only when they clarify. Remove stale content rather than leaving it contradicted.
