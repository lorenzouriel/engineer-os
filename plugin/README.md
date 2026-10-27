# engineer-os

The operating system for AI-assisted engineering, packaged as a Claude Code plugin: domain sub-agents, a spec-driven development (SDD) workflow, a data-engineering knowledge base, and diagramming, review, and authoring skills.

## Install

```bash
claude plugin marketplace add lorenzouriel/engineer-os
claude plugin install engineer-os@engineer-os
```

Every component is namespaced under the plugin, so commands run as `/engineer-os:<group>:<name>`.

## SDD workflow

```
/engineer-os:workflow:brainstorm "idea"        # Phase 0, optional
/engineer-os:workflow:define <brainstorm>      # Phase 1, Clarity Score >= 12/15
/engineer-os:workflow:design <define>          # Phase 2, architecture + agent matching
/engineer-os:workflow:build <design>           # Phase 3, delegated implementation
/engineer-os:workflow:security-audit <feature> # Phase 3.5, optional, gates ship
/engineer-os:workflow:ship <define>            # Phase 4, archive + lessons learned
```

Phase documents are written into your project under `.claude/sdd/` (`features/`, `reports/`, `board/`, `archive/`); templates and contracts ship with the plugin.

## Requirements

- Python 3.7+ for the SDD board script.
- Node.js for the security-audit validators, on Linux, macOS, or WSL.

## Source

Built from the `.claude/` tree of https://github.com/lorenzouriel/engineer-os by `scripts/build-plugin.py`. Edit the source tree, not this copy. License: MIT.
