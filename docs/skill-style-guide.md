# Skill Style Guide

Normative style guide for authoring and maintaining opencode skills. This guide takes precedence over the inline fallback rules in `skill-creator`. All skill PRs and edits MUST conform to this document.

Inspired by the [Hermes Agent](https://github.com/NousResearch/hermes-agent) skill authoring standards and adapted for opencode's conventions.

---

## Frontmatter Rules

### Required Fields

Every SKILL.md frontmatter MUST include these fields, in this order:

```yaml
---
name: {skill-name}
description: "Trigger: {trigger words}. {what the skill does}."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---
```

### Required Field Rules

| Field | Rule |
|---|---|
| `name` | Lowercase, hyphen-separated, ≤64 chars. MUST match the folder name. |
| `description` | One physical line, YAML-quoted. MUST start with trigger keywords (`"Trigger:"` or `"Use when"`). MUST end with a period. SHOULD ≤160 chars, MUST ≤250 chars. |
| `license` | `Apache-2.0` for user-facing skills; `MIT` for internal/SDD orchestration skills. |
| `metadata.author` | `gentleman-programming`. |
| `metadata.version` | Semantic version string. |

### Recommended Fields

```yaml
metadata:
  tags: [tag1, tag2, tag3]
  related_skills: [other-skill-name, another-skill]
  platforms: [linux, macos, windows]
```

| Field | Rule |
|---|---|
| `metadata.tags` | 2-5 lowercase search tags. No marketing words ("powerful", "comprehensive"). |
| `metadata.related_skills` | List of skill `name` values this skill depends on or commonly pairs with. Prefer in-tree skills only. |
| `metadata.platforms` | OS-gating list. Only include if the skill genuinely has platform-specific behavior. Verify against actual script imports. |

### Custom Fields (opencode-specific)

```yaml
disable-model-invocation: true
user-invocable: false
```

Use these ONLY for orchestration-internal skills (SDD phases, `_shared`):
- `disable-model-invocation: true` — skill is not auto-loaded; the orchestrator loads it explicitly.
- `user-invocable: false` — skill cannot be invoked directly by the user.

User-facing skills MUST NOT have these fields.

### Description Format (HARDLINE)

The description IS the trigger mechanism. It MUST:

1. **Start with trigger keywords**: `"Trigger: {words}"` for action skills or `"Use when {condition}"` for gating skills.
2. **Front-load concrete words** the user or agent will say: filenames, task names, domain terms.
3. **State the capability, not the implementation**: "Create Jira tasks in the team format", NOT "Uses the Jira API to..."
4. **One sentence, ends with a period.**
5. **≤250 characters** (hard limit). **≤160 characters** (soft target).

GOOD:
```yaml
description: "Trigger: Go tests, go test coverage, Bubbletea teatest, golden files. Apply focused Go testing patterns."
```

GOOD:
```yaml
description: "Use when writing guides, READMEs, RFCs, or architecture docs. Design docs that reduce cognitive load."
```

BAD:
```yaml
description: >
  A comprehensive and powerful skill for creating Jira tasks
  in the team format using the Jira API with advanced features.
  Trigger: Jira task, ticket, issue, or task creation.
Keywords: jira, task
```

BAD:
```yaml
description: "Design docs that reduce cognitive load. Trigger: writing guides, READMEs, RFCs, onboarding, architecture, or review-facing docs."
```
(Trigger words MUST come FIRST, not mid-description.)

---

## Section Order

### Action Skills (user-invocable)

Skills the user invokes directly (branch-pr, issue-creation, comment-writer, etc.) follow this order:

```
## When to Use          # Triggers + scope + contra-triggers ("Don't use for:")
## Critical Rules       # Non-negotiable rules (or "Hard Rules")
## Workflow             # Step-by-step procedure (or "Execution Steps")
## Decision Gates       # (Optional) Decision table for multi-path skills
## Pitfalls             # (Recommended) Common mistakes and their fixes
## Verification Checklist  # Post-action verification items
## Commands             # (Optional) Quick-reference command table
## References           # (Optional) Links to related docs
```

### SDD / Orchestrator Skills (internal)

Skills invoked by the SDD orchestrator only follow this order:

```
## Purpose              # What this phase does in the SDD pipeline
## What You Receive     # Input artifacts from previous phase
## Execution and Persistence Contract  # Engram saves required
## What to Do           # Step-by-step execution (or "Execution Steps")
## Hard Rules           # (Optional) Non-negotiable constraints
## Decision Gates       # (Optional) Decision table
## Output Contract      # What must be returned/persisted
```

---

## Structural Standards

### "When to Use" Section

Every user-invocable skill MUST have a `## When to Use` section as the first content section after frontmatter. It MUST include:

1. **Positive triggers**: Bulleted list of concrete scenarios/words that activate the skill.
2. **Contra-triggers**: `"Don't use for:"` or `"Use ONLY when..."` bullet list.

Example:
```markdown
## When to Use

- Creating or opening a PR for review
- Preparing a branch with conventional commits
- User mentions "PR", "pull request", "create PR"

Don't use for:
- Stacked/chained PRs over 400 lines — use `chained-pr` skill
- Commit planning without a PR — use `work-unit-commits` skill
```

### "Verification Checklist" Section

Every skill MUST end with a verification checklist (before Commands/References). Items must be concrete and verifiable:

```markdown
## Verification Checklist

- [ ] PR body follows the template format
- [ ] Branch name uses conventional prefix (feat/, fix/, refactor/, docs/, ci/)
- [ ] All commits are conventional (type(scope): description)
- [ ] Issue references are linked (Closes #N)
- [ ] CI checks are passing or auto-fix has been attempted
```

### "Pitfalls" Section

Recommended for complex skills. Numbered items with the mistake and the fix:

```markdown
## Pitfalls

1. **Using wrong base branch.** Always verify with `git fetch origin` before branching.
2. **Forgetting to link issues.** PRs without `Closes #N` lose traceability.
3. **Squashing before review.** Don't squash commits during active review — destroys incremental context.
```

---

## Content Rules

### Tools in Prose

When referencing tools in skill prose, use the opencode tool name in backticks:
- `` `edit` ``, `` `read` ``, `` `grep` ``, `` `glob` ``, `` `bash` ``, `` `task` `` (not shell utilities like `cat`, `grep`, `find`)
- If the skill needs an external MCP server, declare it in a `## Prerequisites` section.

### Skill Body Length

- Target: 180-450 tokens
- Recommended max: 700 tokens
- Hard max: 1000 tokens
- If exceeding, move content to `references/*.md` or `assets/`.

### Supporting Files

```
skills/{skill-name}/
├── SKILL.md              # Required - ~200 lines max
├── references/           # Optional - supporting docs, checklists, templates
│   └── new-pr-salvage.md
├── templates/            # Optional - code/file templates
│   └── report-template.md
├── scripts/              # Optional - helper scripts the agent can run
│   └── validate.sh
└── assets/               # Optional - schemas, fixtures, examples
    └── schema.json
```

### Cross-Referencing Skills

Use `metadata.related_skills` to declare dependencies. Prefer in-tree skills only (user-local skills won't resolve for other users).

```yaml
metadata:
  related_skills: [branch-pr, work-unit-commits]  # correct — both in-tree
```

When mentioning another skill in prose, use the skill name:
```markdown
See the `chained-pr` skill for splitting oversized PRs.
```

---

## Two Structural Templates

### Template A: Action Skill

```markdown
---
name: my-skill
description: "Trigger: {concrete trigger words user says}. {one-sentence capability}."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
  tags: [tag1, tag2, tag3]
  related_skills: [other-skill]
  platforms: [linux, macos, windows]
---

## When to Use

- {trigger scenario 1}
- {trigger scenario 2}

Don't use for:
- {contra-trigger}

## Critical Rules

- {non-negotiable rule 1}
- {non-negotiable rule 2}

## Workflow

### Step 1: {Name}

{what to do}

### Step 2: {Name}

{what to do}

## Pitfalls

1. **{Mistake}.** {Fix}.

## Verification Checklist

- [ ] {verifiable item 1}
- [ ] {verifiable item 2}

## Commands

| Action | Command |
|--------|---------|
| {action} | `{command}` |
```

### Template B: SDD/Orchestrator Skill

```markdown
---
name: sdd-phase-name
description: "Trigger: {orchestrator trigger words}. {one-sentence phase purpose}."
license: MIT
disable-model-invocation: true
user-invocable: false
metadata:
  author: gentleman-programming
  version: "3.0"
  tags: [sdd, {phase-tag}]
  related_skills: [sdd-init, sdd-previous-phase]
---

## Purpose

{What this phase does in the SDD pipeline — one paragraph. Use `## Activation Contract` as an equivalent alternative.}

## What You Receive

- {artifact from previous phase}
- {another input}

## Execution and Persistence Contract

| Artifact | Persistence |
|----------|-------------|
| {artifact name} | `mem_save` type=`{type}` |
| {another} | `mem_save` type=`{type}` |

## What to Do

### Step 1: {Name}

{instructions}

### Step 2: {Name}

{instructions}

## Hard Rules

- {rule 1}
- {rule 2}

## Output Contract

Return:
- {what the phase produces}
- {persistence confirmation}
```

---

## Upgrade Checklist

When modernizing an existing skill, verify:

- [ ] Frontmatter has `name`, `description`, `license`, `metadata.{author, version}`
- [ ] Description starts with `"Trigger:"` or `"Use when"` and is ≤250 chars
- [ ] `metadata.tags` present (2-5 tags)
- [ ] `metadata.related_skills` present (or explicitly empty `[]` for standalone skills)
- [ ] `## When to Use` section is first (action skills) OR `## Purpose`/`## Activation Contract` is first (SDD skills)
- [ ] `## Verification Checklist` section present at end (action skills) OR `## Output Contract` section present (SDD skills)
- [ ] No `#` H1 header (use `##` for sections)
- [ ] Description is one physical line, YAML-quoted
- [ ] No "Keywords" section
- [ ] Tools referenced in prose use opencode tool names in backticks
- [ ] Body ≤1000 tokens (move excess to `references/`)
