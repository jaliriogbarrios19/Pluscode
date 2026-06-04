---
name: chained-pr
description: "Trigger: PRs over 400 lines, stacked PRs, review slices. Split oversized changes into chained PRs that protect review focus."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  tags: [pull-requests, chaining, stacked-prs, review, split]
  related_skills: [branch-pr, work-unit-commits]
---

## When to Use

- Planned PR may exceed **400 changed lines**
- SDD forecasts `400-line budget risk: High` or `Chained PRs recommended: Yes`
- User asks for chained/stacked PRs, review slices, or reviewer-load control

Don't use for:
- PRs ≤400 lines with clear scope — single PR is simpler
- Urgent hotfixes where maintainer accepts `size:exception`

---

## Hard Rules

- Split PRs over **400 changed lines** unless a maintainer explicitly accepts `size:exception`.
- Keep each PR reviewable in about **≤60 minutes**.
- Use one deliverable work unit per PR; keep tests/docs with the unit they verify.
- State start, end, prior dependencies, follow-up work, and out-of-scope items in every chained PR.
- Every child PR must include a dependency diagram marking the current PR with `📍`.
- In Feature Branch Chain, create a draft/no-merge tracker PR; child PR #1 targets the tracker branch, later children target the immediate parent branch.
- Treat polluted diffs as base bugs: retarget or rebase until only the current work unit appears.
- Do not mix chain strategies after the user chooses one.

## Decision Gates

| Condition | Action |
|---|---|
| PR ≤400 changed lines and focused | Keep single PR. |
| PR >400, each slice can land independently | Use Stacked PRs to main. |
| PR >400, feature must integrate before main | Use Feature Branch Chain with tracker. |
| Generated/vendor/migration diff cannot split cleanly | Ask maintainer for `size:exception`. |
| SDD provides `delivery_strategy` | Follow it before apply/PR creation. |

## Execution Steps

1. Estimate changed lines and identify independent work units.
2. Ask for a chain strategy when none is cached and the budget is exceeded.
3. Create branches/PRs using the chosen strategy only.
4. Add Chain Context to each PR without replacing the repo PR template.
5. Verify each PR independently: CI/tests/docs/manual checks, rollback scope, and clean diff.
6. Keep tracker PR draft/no-merge until all child PRs are reviewed and integrated.

## Pitfalls

1. **Mixing chain strategies.** Choose one (Stacked or Feature Branch Chain) and stick with it through the entire change.
2. **Polluted diffs.** When a child PR shows changes from its parent, retarget or rebase until only the current work unit appears.
3. **Forgetting dependency diagrams.** Every child PR must include a diagram marking its position with `📍` so reviewers see the full chain context.
4. **Tracker PR merged early.** Keep the tracker PR as draft/no-merge until ALL children are reviewed and integrated.

## Verification Checklist

- [ ] Each PR is ≤400 changed lines (or has `size:exception`)
- [ ] Each PR is reviewable in ≤60 minutes
- [ ] Dependency diagram present in each child PR with `📍` marker
- [ ] Tracker PR is draft/no-merge until all children done
- [ ] Each child PR has clean diff (no parent changes leaked)
- [ ] Tests and docs are in the same PR as the code they verify
- [ ] Chain strategy documented and consistent across all PRs
- [ ] Branch naming follows `branch-pr` conventions

## References

- [references/chaining-details.md](references/chaining-details.md) — strategy diagrams, PR body section, branch commands, and reviewer guidance.
