---
name: judgment-day
description: "Trigger: judgment day, dual review, adversarial review, juzgar. Run blind dual review, fix confirmed issues, then re-judge."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.5"
  tags: [review, quality, adversarial, dual-review, verification]
  related_skills: [lessons-learned]
---

## When to Use

- User explicitly asks for "Judgment Day", dual review, or adversarial review
- Spanish triggers: `juzgar`, `que lo juzguen`, `revisión adversarial`
- Reviewing a specific target: files, feature, PR, or architecture slice

Use ONLY when explicitly asked. This is not a routine review — it's a formal adversarial review process.

---

## Hard Rules

- Resolve project skills before launching agents: read skill registry, match compact rules by target files/task, and inject the same `Project Standards` block into both judge prompts and fix prompts.
- Launch **two blind judges in parallel** with identical target and criteria; never review the code yourself.
- Wait for both judges before synthesis; never accept a partial verdict.
- Classify warnings as `WARNING (real)` only if normal intended use can trigger them; otherwise downgrade to INFO as `WARNING (theoretical)`.
- Ask before fixing Round 1 confirmed issues.
- After any fix agent runs, immediately re-launch both judges in parallel before commit/push/done/session summary.
- Terminal states are only `JUDGMENT: APPROVED` or `JUDGMENT: ESCALATED`.
- After 2 fix iterations with remaining issues, ask the user whether to continue.

---

## Decision Gates

| Condition | Action |
|---|---|
| Target unclear | Ask for scope; do not launch judges. |
| No skill registry | Warn, proceed with generic criteria, and record `Skill Resolution: none`. |
| Both judges find same CRITICAL/real WARNING | Confirmed; ask/fix according to round rules. |
| One judge finds issue | Suspect; report and triage, do not auto-fix. |
| Judges contradict | Escalate for manual decision. |
| Round 2+ has only theoretical warnings/suggestions | Report as INFO; do not re-judge. |

---

## Execution Steps

1. Confirm target and optional custom criteria.
2. Resolve compact project standards from registry or warn if missing.
3. Start Judge A and Judge B concurrently via delegation.
4. Synthesize findings into confirmed, suspect, contradiction, and INFO buckets.
5. Ask before Round 1 fixes; delegate a separate fix agent for confirmed approved fixes only.
6. Re-judge in parallel after fixes; repeat until approved, escalated, or user asks to stop.
7. Before any terminal action, verify every active Judgment Day has a terminal state.

---

## Pitfalls

1. **Lauching judges without project standards.** Always resolve the skill registry first and inject compact project rules into judge prompts.
2. **Accepting a single judge's verdict.** Never act on one judge's findings — both judges must complete before synthesis.
3. **Auto-fixing suspect issues.** Only confirmed issues (both judges agree) get fixed. Suspect issues (one judge found) are reported and triaged.
4. **Not re-judging after fixes.** Every fix round must be followed by a fresh parallel re-judgment before any terminal action.

---

## Verification Checklist

- [ ] Target and scope confirmed with user
- [ ] Project standards resolved from skill registry (or warning recorded)
- [ ] Both judges launched in parallel with identical criteria
- [ ] Synthesis complete: confirmed, suspect, contradiction, and INFO buckets
- [ ] Round 1 fixes approved by user before execution
- [ ] Re-judgment completed after each fix round
- [ ] Terminal state reached: `JUDGMENT: APPROVED` or `JUDGMENT: ESCALATED`

---

## References

- [references/prompts-and-formats.md](references/prompts-and-formats.md) — judge/fix prompts, warning rubric, verdict tables, and language snippets.
