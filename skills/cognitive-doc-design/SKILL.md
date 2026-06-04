---
name: cognitive-doc-design
description: "Trigger: writing guides, READMEs, RFCs, onboarding, architecture, review-facing docs. Design docs that reduce cognitive load."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  tags: [documentation, design, readability, cognitive-load, reviews]
  related_skills: [comment-writer]
---

## When to Use

Load this skill when creating or editing documentation that people need to understand quickly, retain, or use during review.

Use it especially for:
- PR descriptions and review notes
- Contributor or maintainer guides
- Architecture, workflow, or onboarding docs
- Any doc that currently feels long, dense, or hard to scan

Don't use for:
- Commit messages — follow `branch-pr` conventional commit format
- Review comments — use `comment-writer` skill

---

## Critical Patterns

| Pattern | Rule |
|---------|------|
| Lead with the answer | Put the decision, action, or outcome first. Context comes after. |
| Progressive disclosure | Start with the happy path, then add details, edge cases, and references. |
| Chunking | Group related information into small sections. Keep flat lists short. |
| Signposting | Use headings, labels, callouts, and summaries so readers know where they are. |
| Recognition over recall | Prefer tables, checklists, examples, and templates over prose that must be remembered. |
| Review empathy | Design docs so reviewers can verify intent without reconstructing the whole story. |

---

## Documentation Shape

Use this default structure unless the repo already provides a stronger template:

```markdown
# <Outcome-oriented title>

<One paragraph: what changed, who it helps, and why it matters.>

## Quick path

1. <First action>
2. <Second action>
3. <Verification or expected result>

## Details

| Topic | Decision |
|-------|----------|
| <area> | <concise explanation> |

## Checklist

- [ ] <Reader can confirm this>
- [ ] <Reader can confirm that>

## Next step

<Link or action that continues the workflow.>
```

---

## PR and Review Docs

When documenting a PR, reduce reviewer burnout by making the review path explicit:

- State what to review first.
- State what is intentionally out of scope.
- Link the previous and next PR when work is chained.
- Keep each section focused on one decision or unit of work.
- Use checklists for acceptance criteria and verification.

---

## Pitfalls

1. **Leading with context instead of the answer.** Readers scan for the outcome first. Put decisions and actions before explanations.
2. **Wall of text without signposting.** Use headings, tables, and callouts so readers can navigate without reading everything.
3. **Missing review path.** Reviewers need to know what to look at first and what's out of scope — without it, they read everything linearly.
4. **Over-documenting.** Every section must earn its place. If a detail doesn't help someone act or decide, cut it.

---

## Verification Checklist

- [ ] Document leads with the answer, decision, or action
- [ ] Happy path is visible first; details and edge cases follow
- [ ] Sections are chunked; no walls of text
- [ ] Headings and labels provide clear navigation
- [ ] Tables or checklists used where they reduce recall burden
- [ ] If a PR doc: review path is explicit (what first, what's out of scope)

---

## Commands

```bash
# Check markdown files changed in the current branch
git diff --name-only -- '*.md'

# Inspect PR changed-line count for cognitive load
gh pr view <PR_NUMBER> --json additions,deletions,changedFiles
```
