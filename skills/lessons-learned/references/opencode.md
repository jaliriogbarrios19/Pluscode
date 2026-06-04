# OpenCode Configuration & Skills Learnings

## Custom Provider Auth Headers

**Gotcha**: Some providers use non-standard auth headers instead of `Authorization: Bearer`.
- MiMo 2.5 Pro (Xiaomi) uses `api-key` header — requires `options.headers: { "api-key": "..." }` in provider config
- Do NOT set `options.apiKey` when using custom headers — it may cause the SDK to send both, creating conflicts
- The `@ai-sdk/openai-compatible` npm package works for any OpenAI-compatible API (most modern providers)

## Edit Tool Context Ambiguity

**Gotcha**: The `edit` tool matches the FIRST occurrence of `oldString` — if a key like `"permission"` appears both inside an agent object AND at the top level, it will match the wrong one.
- Use unique surrounding context (include the parent object key or nearby fields) to disambiguate
- After edits that touch JSON structure, always validate with `ConvertFrom-Json`

## SDD + Model Routing Integration

**Gotcha**: SDD agents and model-routing agents are orthogonal layers. Integration happens at model assignment per agent, not at permission level.
- Assign the optimal model directly to each SDD agent in `opencode.jsonc`
- Don't try to make the orchestrator delegate to model subagents — that's the wrong abstraction
- Model subagents (`@mimo-pro`, `@deepseek-pro`, `@deepseek-flash`) are for the general `build` agent, not the SDD orchestrator

## Agent Markdown Files

**Gotcha**: Agent markdown files use `---` frontmatter with `description`, `mode`, `model`, and optional `permission`. The filename becomes the agent name.
- No `name` field in frontmatter — filename is the name
- `model` uses `provider/model-id` format (e.g., `xiaomi/mimo-v2.5-pro`)
- Global agents go in `~/.config/opencode/agents/`, project agents in `.opencode/agents/`

## Skill Description Format

**Gotcha**: The `description` frontmatter field IS the trigger mechanism in opencode. Words at the START have higher matching priority than words later in the string.
- Always format as `"Trigger: {concrete words}. {capability}."` — trigger words FIRST, capability second
- Never `"{Capability}. Trigger: {words}."` — 12 of 23 skills had this inverted pattern and were corrected
- Description must be one physical line, YAML-quoted, ≤250 chars hard limit, ≤160 soft target
- State capability, not implementation: "Manage skill lifecycle with user-authorized tracking" > "Always asks authorization"

## Skill Section Order

**Gotcha**: Action skills and SDD skills follow different structural templates. Mixing them breaks the orchestrator's expectations.
- Action skills: When to Use → Critical Rules → Workflow → Pitfalls → Verification Checklist
- SDD skills: Activation Contract → What You Receive → Execution Contract → Execution Steps → Hard Rules → Decision Gates → Output Contract
- SDD skills MUST have `disable-model-invocation: true` + `user-invocable: false` in frontmatter

## Skill Cross-Referencing

**Gotcha**: Skills that depend on shared references (`_shared/`) must declare `_shared` in `metadata.related_skills`. Without this edge, moving or renaming `_shared` silently breaks dependent skills.
- All SDD skills that reference `../_shared/*.md` paths need `related_skills: [_shared]`
- Action skills cross-reference each other (e.g., branch-pr → chained-pr, work-unit-commits)

## Optional Skills Pattern

**Gotcha**: opencode scans `skills/` recursively but NOT `optional-skills/`. Skills there are invisible until explicitly copied.
- Install: copy from `optional-skills/{name}/` to `skills/{name}/`. Check for name conflicts first.
- Deactivate user-created: move back to `optional-skills/`. Deactivate agent-created: archive to `skills/.archive/`.
- No config changes needed — the directory boundary IS the activation mechanism.

## Judgment Day Protocol

**Gotcha**: After fixing confirmed issues, ALWAYS re-judge with both judges in parallel. Never assume fixes are correct.
- Round 1 fixes can introduce new issues or miss edge cases; double-blind catches them
- Only declare APPROVED when both judges return clean
- After 2 fix iterations with remaining issues, ask user whether to continue
- Confirmed = both judges agree. Suspect = one judge found it — report, don't auto-fix.

## Curator Provenance Model

**Gotcha**: The curator needs both autonomous and user-requested action modes. Initial design said "only agent-created skills" but optional skills install/deactivate requires handling user-created skills too.
- Autonomous (curator initiates): ONLY agent-created skills. Review, staleness, archiving.
- User-requested (user initiates): ALL skills. Install, deactivate, explicit patch proposals.
- Both modes require user authorization per action. Pinned skills are immune to both.

## Skill Frontmatter Conventions (OpenCode vs Hermes)

**Gotcha**: OpenCode and Hermes Agent use different frontmatter conventions. A skill loader must handle both.
- OpenCode: `metadata.version`, `metadata.tags`, `metadata.author`
- Hermes: `version` at top level, `author` at top level, `metadata.hermes.tags`, `metadata.hermes.related_skills`
- Fix: propagate top-level `version`/`author` into `metadata` dict if absent, fallback to `metadata.hermes.tags` for tags
- Hermes skills also use `platforms: [linux, macos, windows]` at top level (not in metadata)

## Agno + OpenCode MCP Integration

**Pattern**: Agno (Python agent SDK) integrates with opencode via MCP stdio server. Install `agno` + `mcp` Python packages, create a `scripts/server.py` with `from mcp.server import Server`, and register in `opencode.jsonc` as a `type: "local"` MCP with `command: ["python", "skills/.../server.py"]`. Tools without external API keys (web_search via httpx, python_exec via subprocess) work out of the box. Model-dependent tools (code_analyze via Agno Agent) require API keys in env vars. The Agno `agno[ddg]` extra requires separate install — prefer using `httpx` directly for DuckDuckGo search to avoid extra deps.

## OpenCode Config Distribution Pattern

**Pattern**: To publish an opencode config as a reusable repo, keep `opencode.jsonc` model-agnostic (no hardcoded providers or model IDs) and create a separate `opencode.json` with personal overrides. Add `opencode.json` to `.gitignore`. opencode merges both at runtime — `opencode.json` values override `opencode.jsonc`. This keeps the repo clean for any user while preserving local customization. Agent names should reflect capability (pro, fast, design), not model (deepseek-pro, mimo-pro). Long inline prompts should be extracted to `prompts/` directory and referenced via `{file:prompts/...}` syntax.

## .gitignore Self-Reference Trap

**Gotcha**: If `.gitignore` contains its own filename, it silently prevents itself from being tracked in git. The file appears in `git status` as staged but is never actually committed. Remove `.gitignore` from its own content to make it trackable. Use `git add -f .gitignore` if it was previously self-ignored.

## Hermes Agent Python Venv

**Discovery**: Hermes Agent (NousResearch) installed at `C:\Users\Usuario\AppData\Local\hermes\hermes-agent\` uses a venv without pip. The system Python 3.14 at `C:\Users\Usuario\AppData\Local\Python\bin\python.exe` has full pip support. When installing Python dependencies for opencode integration, use the system Python — the Hermes venv is for running Hermes, not for package management.
