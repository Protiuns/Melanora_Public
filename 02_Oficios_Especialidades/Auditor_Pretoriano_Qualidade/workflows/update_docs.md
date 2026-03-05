---
description: Updates ALL generated documentation (Skills + Automations) to ensure the Knowledge Base is fresh.
---

# Update Documentation System

This workflow triggers all documentation generators.

1. Update Skill Catalog
// turbo
```bash
python .agent/scripts/update_skill_catalog.py
```

2. Update Automation Catalog
// turbo
```bash
python .agent/scripts/update_automation_catalog.py
```
