---
name: security-audit
description: Multi-agent security audit of a built feature before ship (Phase 3.5) — scoped to the feature's files, findings verified independently, gate report for /ship
argument-hint: <feature-name|design-file> [--profile quick|standard|deep] [--budget N] [--full] [--output <dir>]
---

# Security Audit Command

> Source-first security audit of a built feature (Phase 3.5). An auditor, not a fixer.

## Usage

```bash
/workflow:security-audit <feature-name|design-file> [--profile quick|standard|deep] [--budget N] [--full] [--output <dir>]
```

## Examples

```bash
/workflow:security-audit USER_AUTH
/workflow:security-audit .claude/sdd/features/DESIGN_DATA_EXPORT.md --profile quick
/workflow:security-audit USER_AUTH --profile deep --budget 40
/workflow:security-audit --full                      # whole repository, not one feature
```

---

## Overview

Runs between Build and Ship:

```text
Phase 3:   /build                    → Code + .claude/sdd/reports/BUILD_REPORT_{FEATURE}.md
Phase 3.5: /workflow:security-audit  → .claude/sdd/reports/SECURITY_AUDIT_{FEATURE}.md (THIS COMMAND)
Phase 4:   /ship                     → .claude/sdd/archive/{FEATURE}/SHIPPED_{DATE}.md
```

Optional, but when its report exists `/ship` honors it: a `BLOCKED` verdict stops the ship.

---

## What Happens

1. **Load the skill** — read `${CLAUDE_PLUGIN_ROOT}/skills/sdd-security-audit/SKILL.md`; it owns the full methodology. Run it in this session: the audit coordinates parallel subagents, and a subagent cannot spawn its own.
2. **Resolve scope** — the feature's DESIGN manifest, board touched files, and branch diff (`--full` drops scoping). Record profile, budget, and scope in `run-metadata.json` in the external run directory (default `~/security-audit-skill/<repo>/run-<N>`, or `--output`, which must be outside the repo or git-ignored).
3. **Six phases** — reconnaissance → coverage-led hunting waves → independent candidate validation → validated `findings.json` → fresh-eyes record verification → target-neutral reports.
4. **Write the SDD report** — `.claude/sdd/reports/SECURITY_AUDIT_{FEATURE}.md` from `SECURITY_AUDIT_TEMPLATE.md`: verdict, counts, one row per record, coverage statement, run directory. No reproduction detail.
5. **Hand off** — `/ship` unless `BLOCKED`; otherwise route each fix to `/build` or `/iterate`. Never edit code, phase documents, or board tasks.

---

## References

- Skill: `${CLAUDE_PLUGIN_ROOT}/skills/sdd-security-audit/SKILL.md`
- Template: `${CLAUDE_PLUGIN_ROOT}/sdd/templates/SECURITY_AUDIT_TEMPLATE.md`
- Contracts: `${CLAUDE_PLUGIN_ROOT}/sdd/architecture/WORKFLOW_CONTRACTS.yaml`
- Previous Phase: `${CLAUDE_PLUGIN_ROOT}/commands/workflow/build.md`
- Next Phase: `${CLAUDE_PLUGIN_ROOT}/commands/workflow/ship.md`
- Lighter alternative: `appsec-review` skill (standards-mapped single-agent review)
