# SECURITY AUDIT: {Feature Name}

> Target-neutral summary of the Phase 3.5 security audit. Reproduction detail stays in the external run directory — never copy execution, inputs, or traces here.

## Metadata

| Attribute | Value |
|-----------|-------|
| **Feature** | {FEATURE_NAME} |
| **Date** | {YYYY-MM-DD} |
| **Status** | {BLOCKED / PASS WITH FINDINGS / CLEAR / INCOMPLETE} |
| **Next Step** | {/ship, or the routed fix command} |
| **Profile** | {quick / standard / deep} |
| **Scope** | {scoped: N paths from DESIGN manifest + board + diff / full repository} |
| **Source ref** | {commit SHA}{, dirty worktree} |
| **Budget** | {N agent invocations / none} — used {M} |
| **Run directory** | {absolute path, e.g. ~/security-audit-skill/<repo>/run-<N>} |
| **Run status** | {complete / incomplete: <incomplete_reason>} |

---

## Verdict

**{BLOCKED / PASS WITH FINDINGS / CLEAR / INCOMPLETE}** — {one sentence: why}

| Verdict | Count |
|---------|-------|
| confirmed — critical | {n} |
| confirmed — high | {n} |
| confirmed — medium | {n} |
| confirmed — low / informational | {n} |
| needs_validation | {n} |
| rejected | {n} |

---

## Records

One row per `confirmed` and `needs_validation` record, ordered by severity then fingerprint. Rejected records stay in `findings.json` only.

| Fingerprint | Verdict | Severity | Title | Location | Route |
|-------------|---------|----------|-------|----------|-------|
| {fp} | confirmed | {high} | {short title} | `{repo/relative/path}` | {/build · /iterate DESIGN_X.md · owner} |
| {fp} | needs_validation | — | {short title} | `{repo/relative/path}` | {owner who can resolve the blocker} |

### Fix first

1. {fingerprint} — {the invariant to enforce, one line}
2. {...}

---

## Coverage

- **Covered units:** {n} of {total} ledger units
- **Out of scope / deferred / blocked:** {n} / {n} / {n} — {one line on the largest gap}
- **Prior runs used:** {paths, or "none — first audit of this feature"}
- **Execution:** {sandboxed local checks / source-only: <missing control>}
- **Statement:** {e.g. "Scoped standard run over the feature's 14 files; no confirmed findings in the audited scope. Not a claim about the rest of the repository."}

---

## Revision History

| Date | Run | Change |
|------|-----|--------|
| {YYYY-MM-DD} | run-{N} | {Initial audit / re-audit after fixes} |
