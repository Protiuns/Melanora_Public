---
description: Updates the Studio Skill Catalog documentation based on the current Skill Registry and Skill definitions.
---

# Update Skill Catalog

This workflow regenerates the `docs/studio_skill_catalog.md` file to reflect the latest changes in the `studio_library/_registry/skill_registry.json` and individual `SKILL.md` files.

1. Run the update script
// turbo
```bash
python .agent/scripts/update_skill_catalog.py
```
