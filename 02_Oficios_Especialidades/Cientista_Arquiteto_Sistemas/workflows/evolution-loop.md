---
description: Continuous Evolution Cycle of the Agent and Skills (Evolution Loop)
---

# 🔄 Workflow: Evolution Loop (Ops Edition)

This workflow defines the Agent's self-analysis process to identify usage patterns, knowledge gaps, and technical improvement opportunities.

## 📊 1. Action Domains (Categorical Search)
When receiving a command, identify which **Domain** it belongs to:

### ⚙️ Logic & Backend
*   **Action:** API, Database, Auth, Algorithms.
*   **Skills:** `project_scope_manager`, `documentation_architect`.

### 🎨 Frontend & UI
*   **Action:** Views, Components, Styling, UX.
*   **Skills:** `project_concept_forge`.

### 🚀 DevOps & Operations
*   **Action:** CI/CD, Backup, Structure, Naming.
*   **Skills:** `project_version_control`, `project_nomenclature_guard`, `project_delivery_manager`.

## 📦 2. Reusability Management
The Agent must monitor the codebase for redundancy:
1. **Pattern Identification**: Writing the same logic for the 3rd time? Create a Module/Function.
2. **Cross-Project Refactoring**: Improvement in Project A can benefit Project B? Abstract it.

For each command received, the Agent must perform:
1. **Pattern Identification**: Is this recurrent?
2. **Skill Confrontation**: Which skill should cover this? Was it efficient?
3. **Gap Detection**: Are we improvising?

## 💡 3. Suggestion Matrix
Based on the analysis, suggest one of the following actions:

| Type | Suggested Action | Trigger |
| :--- | :--- | :--- |
| **Skill** | `Create New` | Recurrent task without dedicated skill. |
| **Skill** | `Edit/Evolve` | Current skill failed edge case or is outdated. |
| **Agent** | `Behavior Change` | Recurrent error in order interpretation. |
| **Workflow** | `New Workflow` | Multi-step process that can be automated.

## 🛡️ 4. Failure Analysis and Hardening
Whenever a task fails and is resolved via trial & error, the Agent **MUST** transform the solution into a robust pattern.

**Post-Resolution Protocol:**
1.  **Isolate Problem**: What failed?
2.  **Identify Solution**: What command worked?
3.  **Update Source**: Implant the robust solution immediately into the original Workflow or Skill.

## 🚀 5. Evolution Execution
1. Update this document or create the new skill/workflow via `write_to_file`.
2. Document the change in `README.md` if it impacts global architecture.
