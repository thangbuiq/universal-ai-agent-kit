---
name: refactoring
description: Safely restructure code without changing behaviour. Use for cleaning up duplication, long functions, poor naming, tangled dependencies or preparing code for a new feature.
metadata:
  source: first-party
---

# Refactoring

1. **Secure a safety net** – ensure tests cover the behaviour you will touch; add characterization tests if they don't. Run them green first.
1. **One transformation at a time**: rename, extract function/class, inline, move, replace conditionals with polymorphism/lookup, introduce parameter object, remove dead code.
1. **Run tests after every step**; commit in small steps so each is revertable.
1. **Keep behaviour and public APIs stable** unless explicitly asked; separate refactor commits from feature/fix commits.
1. Follow the codebase's conventions; don't introduce new patterns or dependencies just because.

Signals worth fixing: duplication (3+ copies), functions doing several things, deep nesting, boolean-flag parameters, primitive obsession, shotgun surgery. Stop when the code is clear enough for the task at hand; don't gold-plate.
