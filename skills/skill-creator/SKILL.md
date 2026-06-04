---
name: skill-creator
description: "Trigger: new skills, agent instructions, documenting AI usage patterns. Create LLM-first skills with valid frontmatter."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.0"
  tags: [skills, authoring, conventions, skill-md]
  related_skills: [skill-registry]
---

## When to Use

- Creating a new skill from scratch
- Updating or modernizing an existing skill
- Documenting repeated AI usage patterns as skills
- User asks to "create a skill", "add a skill", "document this pattern"

Use ONLY when the pattern is genuinely reusable. Don't create a skill for one-off tasks or trivial patterns — use normal documentation instead.

## Hard Rules

- Apply `docs/skill-style-guide.md` as the NORMATIVE source first. This skill's inline rules are the FALLBACK when that guide is unavailable.
- A skill is a runtime instruction contract for an LLM, NOT human documentation.
- Never add a `Keywords` section; preserve essential trigger words in `description`.
- References must point to local files.
- Keep the skill body concise: target 180-450 tokens, recommended max 700, hard max 1000.

## Decision Gates

| Need | Action |
|------|--------|
| Code templates, schemas, fixtures, generated examples | Put them in `assets/` |
| Conceptual detail, edge cases, existing docs | Put local links in `references/` |
| Long explanation in `SKILL.md` | Move it to a supporting file |
| Multiple meaningful paths | Add a compact decision table |
| Action/invokable skill | Use Template A (When to Use → Critical Rules → Workflow → Pitfalls → Verification) |
| SDD/orchestrator skill | Use Template B (Purpose → What You Receive → Execution Contract → Steps → Output) |

## Execution Steps

1. Read `docs/skill-style-guide.md` as the normative source.
2. Survey peer skills in the same category to match tone and structure.
3. Confirm the skill does not already exist and the pattern is reusable.
4. Create `skills/{skill-name}/SKILL.md` with this directory structure:
   ```
   skills/{skill-name}/
   ├── SKILL.md              # Required — main skill file
   ├── references/           # Optional — links to local docs
   ├── templates/            # Optional — file templates
   ├── scripts/              # Optional — helper scripts
   └── assets/               # Optional — schemas, fixtures, examples
   ```
5. Use this frontmatter as the starting shape:
   ```yaml
   ---
   name: {skill-name}
   description: "Trigger: {trigger words}. {one-sentence capability}."
   license: Apache-2.0
   metadata:
     author: gentleman-programming
     version: "1.0"
     tags: [tag1, tag2, tag3]
     related_skills: [other-skill]
   ---
   ```
   For SDD/internal skills, add `disable-model-invocation: true` and `user-invocable: false`.
6. Follow the canonical section order from `docs/skill-style-guide.md`.
7. Register the skill in `AGENTS.md` when it is a project skill.

## Inline Fallback Rules

Use these ONLY when `docs/skill-style-guide.md` is unavailable:

- `description` MUST be one physical line, quoted, YAML-safe, and start with trigger words (`"Trigger:"` or `"Use when"`).
- `description` SHOULD be ≤160 chars and MUST be ≤250 chars. End with a period.
- Frontmatter MUST include `name`, `description`, `license`, `metadata.author`, `metadata.version`.
- Frontmatter SHOULD include `metadata.tags` (2-5 lowercase tags) and `metadata.related_skills` (or empty `[]`).
- Every skill MUST have a `## Verification Checklist` section at the end.
- Use imperative instructions, not tutorials or background prose.
- Put supporting material in `assets/`, `references/`, `templates/`, or `scripts/`, not the main skill body.
- Tools referenced in prose must use opencode tool names in backticks (`edit`, `read`, `grep`, `bash`, `task`).

Good:
```yaml
description: "Trigger: Jira task, ticket, issue, task creation. Create Jira tasks in the team format."
```

Bad:
```yaml
description: >
  Create Jira tasks in the team format.
  Trigger: Jira task, ticket, issue, or task creation.
Keywords: jira, task
```

## Output Contract

Return:
- Files created or modified.
- Whether the style guide or inline fallback rules were used.
- Any AGENTS.md registration change.
- Any supporting files added under `assets/`, `references/`, `templates/`, or `scripts/`.

## Verification Checklist

- [ ] `docs/skill-style-guide.md` was consulted as normative source
- [ ] Frontmatter has `name`, `description`, `license`, `metadata.{author, version}`
- [ ] Description starts with `"Trigger:"` or `"Use when"` and is ≤250 chars
- [ ] `metadata.tags` present with 2-5 lowercase tags
- [ ] `metadata.related_skills` present (or empty `[]` for standalone)
- [ ] Body follows canonical section order (When to Use → Critical Rules → Workflow → Pitfalls → Verification)
- [ ] `## Verification Checklist` section present at end
- [ ] Body ≤1000 tokens (moved excess to `references/` if needed)
- [ ] No `Keywords` section, no `#` H1 header
- [ ] Tools referenced use opencode tool names in backticks

## References

- `docs/skill-style-guide.md` — normative LLM-first skill style guide for this repo.
