# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

engineer-os is a Claude Code configuration, not an application. Everything that matters lives in `.claude/`: agents, slash commands, knowledge-base (KB) domains, skills, and the SDD (spec-driven development) workflow. There is no build, lint, or test suite for the repo as a whole. "Code" here is mostly markdown and YAML that Claude Code loads at runtime. The only executable pieces are helper scripts inside skills.

## The component model

All authoring decisions follow the four-layer model in `.claude/kb/shared/component-model.md`:

- **Agents** (`.claude/agents/<category>/*.md`) are the execution layer: identity, tool scope, model tier, stop conditions, escalation. Keep them thin; the default body is "read skill X and execute it".
- **Skills** (`.claude/skills/<name>/SKILL.md`) hold the methodology (how to do something). Detail goes in `references/`, `scripts/`, `assets/`.
- **Commands** (`.claude/commands/<group>/<name>.md`) are thin entry points, invoked as `/<group>:<name>`.
- **KB domains** (`.claude/kb/<domain>/`) hold reference truth: `index.md`, `quick-reference.md`, `concepts/`, `patterns/`.

Before adding anything, decide the layer with the `component-model` skill. Then author with `create-agent`, `create-skill`, or `/knowledge:create-kb` (`kb-build` for the source-verified variant).

## SDD workflow

Phases are wired together in `.claude/sdd/architecture/WORKFLOW_CONTRACTS.yaml`. Each phase is a `/workflow:*` command → a workflow agent (`.claude/agents/workflow/`) → an `sdd-*` skill that holds the method:

`brainstorm` (optional) → `define` (Clarity Score ≥ 12/15) → `design` → `build` → `security-audit` (optional) → `ship`, plus `iterate` for mid-stream changes. `breakdown`, `board`, `validate`, and `create-pr` support the build stage. `security-audit` has no workflow agent: it runs in the main session because it launches parallel subagents, and `/ship` blocks on its `BLOCKED` verdict when its report exists.

- Phase documents are generated from `.claude/sdd/templates/*_TEMPLATE.md` into `.claude/sdd/features/` (active). Build reports go to `.claude/sdd/reports/`, and shipped features to `.claude/sdd/archive/`.
- Design matches files to agents by globbing `.claude/agents/**`, so a new agent file is picked up without registration.
- Story state lives in a file-based kanban under `.claude/sdd/board/<FEATURE>/`, managed by a stdlib script:
  ```
  python .claude/skills/sdd-board/board.py list
  python .claude/skills/sdd-board/board.py show|next|check|html <FEATURE>
  python .claude/skills/sdd-board/board.py move <FEATURE> S01 in-progress [--note "..."]
  ```

## Contracts that other files depend on

- **Agent frontmatter is machine-read.** The `agent-router` skill (`SKILL.md` + `routing.json`) is built from every agent's `name`, `tier`, `model`, the **first line** of `description`, `kb_domains`, and the `escalation_rules` `target:` values. The parser is line-based: `kb_domains` must use inline `[a, b]` form, and every escalation `target:` must be a real agent name or `user`. Full contract: `.claude/skills/create-agent/SKILL.md`; scaffold: `.claude/agents/_template.md`.
- **The router is hand-synced here.** Its generator (`scripts/generate-agent-router.py`) is not in this repo. When you add or change an agent, update `.claude/skills/agent-router/SKILL.md` and `routing.json` by hand.
- **KB registry.** Every KB domain must be registered in `.claude/kb/_index.yaml`, and every agent `kb_domains` entry must exist there. That file is the single source of truth for KB file-size limits (quick-reference 100 lines, concept 150, pattern 200). New files start from `.claude/kb/_templates/`.
- **Skill frontmatter.** Only `name`, `description`, and optionally `license`, `allowed-tools`, `metadata`, `compatibility` are allowed. `name` must equal the folder name and be kebab-case with at least one hyphen. Write multi-line descriptions as a literal block (`|`). The description is the trigger, so there is no `triggers:` key.
- **Counts are duplicated.** Agent, command, skill, and KB counts appear in `README.md`, `.claude/agents/README.md` (hand-maintained catalog: categories, tiers, escalation map), the `agent-router` skill, and `.claude/kb/_index.yaml`. Update all of them together.

## Plugin build

The repo is also a plugin marketplace: `.claude-plugin/marketplace.json` lists one plugin, `engineer-os`, whose source is `plugin/`. `plugin/` is generated, never edited by hand:

```
python scripts/build-plugin.py          # rebuild plugin/ from .claude/
python scripts/build-plugin.py --check  # exit 1 if plugin/ is stale
```

The build copies `.claude/` and rewrites plugin-internal references (`.claude/agents|commands|skills|kb/...`, `.claude/sdd/templates|architecture/...`) to `${CLAUDE_PLUGIN_ROOT}/...` in markdown and YAML bodies. It leaves SDD workspace paths (`.claude/sdd/features|reports|board|archive`) and `.claude/storage` project-relative, and drops `settings.json`, `storage/`, the SDD workspace folders, `agents/_template.md`, and README files under `agents/` and `commands/`. After any change under `.claude/`, rebuild and commit `plugin/` in the same commit. Validate with `claude plugin validate ./plugin` and `claude plugin validate .`.

The manifest omits `version` on purpose, so installs track git commits. Never change the plugin `name` (`engineer-os`): installs are recorded by name.

## Upstream references that don't exist here

This config was extracted from the upstream `lorenzouriel/master-claude` repo, still the default source of `.claude/skills/sync-stack/scripts/sync.py`. Several skills (`create-skill`, `create-agent`) and SDD docs still describe that repo's tooling: `build-plugin.sh` (here it is `scripts/build-plugin.py`), `plugin-extras/`, `scripts/generate-agent-router.py`, `CHANGELOG.md`, and `docs/`. Apart from the build script, none of those exist in engineer-os. Skip those checklist steps rather than creating the files, unless asked.
