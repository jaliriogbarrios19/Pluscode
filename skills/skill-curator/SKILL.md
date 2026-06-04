---
name: skill-curator
description: "Trigger: curator, curate skills, review skills, archive skills, improve skills, skill maintenance. Manage skill lifecycle with user-authorized tracking, archiving, and self-improvement."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
  tags: [skills, curator, maintenance, archiving, self-improvement]
  related_skills: [skill-creator, skill-registry]
---

## When to Use

- User says "curate skills", "review skills", "check skills", "skill maintenance"
- A complex task was just completed and the agent discovered a new pitfall or pattern
- Skills haven't been reviewed in a while (stale detection)
- The agent wants to improve a skill based on recent experience

Don't use for:
- Creating new skills from scratch — use `skill-creator`
- Updating the skill index — use `skill-registry`

---

## Critical Rules

1. **NEVER act without authorization.** Every archive, patch, or structural change MUST be explained and approved by the user before execution.
2. **Never delete.** The most destructive action is archive (move to `.archive/`). Skills can always be restored.
3. **Only touch agent-created skills.** Bundled/core skills (shipped with opencode) and pinned skills are IMMUNE to automated actions.
4. **Pinned skills are sacred.** A pinned skill is exempt from ALL automated transitions, including the review pass.
5. **Proposals are cheap, actions are expensive.** It's safe to propose improvements. It's dangerous to apply them without authorization.

---

## Skill Provenance

The curator distinguishes between **autonomous management** and **user-requested actions**:

- **Autonomous**: ONLY applies to skills with `created_by: "agent"` provenance. Review, staleness detection, and archiving operate on agent-created skills without user prompting (but always WITH user authorization per action).
- **User-requested**: Install, deactivate, and explicit patch proposals apply to ALL skills — agent-created, bundled, or user-created — when the user explicitly asks. Optional skills management falls here.

Provenance is stored in the SKILL.md frontmatter:
```yaml
metadata:
  created_by: agent        # agent-created — curator CAN autonomously manage
  pinned: true             # pinned — curator CANNOT touch, even on user request
```

Bundled skills and optional skills are managed via user-requested actions only (install, activate, deactivate). The curator never autonomously reviews or archives them.

---

## Operations

### Operation 1: Track Usage

After a skill is loaded and used in a session, record the usage in `~/.config/opencode/.skill-usage.json`:

```json
{
  "skills": {
    "branch-pr": {
      "use_count": 42,
      "last_used": "2026-05-29T14:30:00Z",
      "state": "active",
      "pinned": false,
      "created_by": "bundled"
    },
    "my-custom-skill": {
      "use_count": 3,
      "last_used": "2026-04-15T09:00:00Z",
      "state": "active",
      "pinned": false,
      "created_by": "agent"
    }
  }
}
```

How to track:
1. Read `.skill-usage.json` (create if missing with `{"skills": {}}`)
2. For each skill used this session, increment `use_count`, update `last_used` to now
3. Write back

### Operation 2: Review and Propose

When the user invokes the curator, review ALL agent-created skills for staleness.

Staleness rules:
- **Active**: used within last 30 days → no action
- **Stale**: unused for 30-90 days → propose review
- **Archivable**: unused for 90+ days → propose archiving

For each stale or archivable skill, present:
```
## Skill Review: {skill-name}

**Last used**: {date} ({N} days ago)
**Use count**: {N}
**State**: {active/stale/archivable}

**Proposal**: {review needed / archive recommended}

[Explain why in one sentence]

Do you want to:
1. Keep active (resets timer)
2. Archive to .archive/ (recoverable)
3. Skip for now
```

Wait for user response before acting.

### Operation 3: Archive

To archive a skill:
1. User MUST authorize
2. Move the skill directory from `skills/{name}/` to `skills/.archive/{name}/`
3. Update `.skill-usage.json` → `state: "archived"`, set `archived_at`
4. Report: "Archived {name} to .archive/. Restore with: move skills/.archive/{name}/ back to skills/{name}/"

**Restoration**: Move the directory back from `.archive/` to `skills/`, update state to `active`, reset `last_used`.

### Operation 4: Self-Improvement (Patch)

This is the ON-THE-FLY learning loop. During or after any task, if the agent discovers:

- A new pitfall that should be in a skill's `## Pitfalls` section
- A better pattern that should replace a `## Critical Rules` entry
- A missing edge case that should be in the `## When to Use` section
- A verification step that should be in the `## Verification Checklist`

It proposes a patch using this exact pattern:

```
## Skill Improvement Proposal: {skill-name}

**Trigger**: [What happened that revealed this gap? One sentence.]

**What I'd change**: [The exact section and content to add/modify.]

**Current text**:
```
{exact existing text from the skill — or "none" if adding new}
```

**Proposed text**:
```
{exact new text — copy-pasteable into the skill}
```

**Why**: [Technical reason. What would break or be missed without this change.]

Apply this change?
```

Wait for user authorization. If approved:
1. Use `edit` (not `write`) to make the precise change
2. Increment `patch_count` in `.skill-usage.json`
3. Update `last_activity_at`

If declined, record the proposal was considered and move on. Do NOT argue. The human always leads.

**What can be patched**: Pitfalls, rules, examples, verification checklist items, trigger descriptions.

**What CANNOT be patched without full rewrite**: Skill name, structural reorganization, new major sections.

### Operation 5: Pin / Unpin

```
Pin:   → skill is immune to all automated curator actions
Unpin: → skill returns to normal lifecycle
```

Pinning requires user authorization. Toggled via `.skill-usage.json` `pinned: true/false`.

---

## Sidecar File: .skill-usage.json

Full schema:

```json
{
  "skills": {
    "{skill-name}": {
      "use_count": 0,
      "view_count": 0,
      "patch_count": 0,
      "last_used": "ISO8601",
      "last_activity_at": "ISO8601",
      "created_at": "ISO8601",
      "archived_at": "ISO8601 or null",
      "state": "active | stale | archived",
      "pinned": false,
      "created_by": "bundled | agent | user"
    }
  },
  "last_review": "ISO8601",
  "review_count": 0
}
```

Location: `~/.config/opencode/.skill-usage.json`

---

## Optional Skills

Skills in `optional-skills/` are NOT auto-loaded. To activate one:
1. User requests it explicitly
2. Curator proposes installing it when relevant
3. If `skills/{name}/` already exists, report the conflict and ask: overwrite, merge, or cancel.
4. Installation = copy from `optional-skills/{name}/` to `skills/{name}/`

To deactivate:
1. For user-created optional skills: move from `skills/{name}/` to `optional-skills/{name}/`
2. For agent-created skills: always archive to `.archive/` instead (Operation 3)

List available optional skills with: `ls optional-skills/`

---

## Verification Checklist

- [ ] `.skill-usage.json` exists and is valid JSON
- [ ] All agent-created skills reviewed for staleness
- [ ] Every proposed action was authorized by user before execution
- [ ] Archived skills are in `skills/.archive/`, not deleted
- [ ] Pinned skills were NOT touched
- [ ] Bundled/core skills were NOT touched
- [ ] Self-improvement proposals include exact before/after text and explanation
