---
name: comment-writer
description: "Trigger: PR feedback, issue replies, reviews, Slack, GitHub comments. Write warm, direct collaboration comments."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  tags: [communication, comments, reviews, feedback, collaboration]
  related_skills: [branch-pr, cognitive-doc-design]
---

## When to Use

Load this skill whenever you write a comment that another human will read.

Use it for:
- GitHub PR or issue comments
- Review feedback and requested changes
- Maintainer replies
- Slack, Discord, or async project updates

Don't use for:
- Commit messages — follow `branch-pr` conventional commit format
- Technical documentation — use `cognitive-doc-design` skill

---

## Voice Rules

| Rule | Requirement |
|------|-------------|
| Be useful fast | Start with the actionable point. Do not recap the whole PR before feedback. |
| Be warm and direct | Sound like a thoughtful teammate, not a corporate bot. |
| Keep it short | Prefer 1 to 3 short paragraphs or a tight bullet list. |
| Explain why | Give the technical reason when asking for a change. |
| Avoid pile-ons | Comment on the highest-value issue, not every tiny preference. |
| Match thread language | Write in the thread/user language. If writing in Spanish, use Rioplatense Spanish/voseo: `podés`, `tenés`, `fijate`, `dale`. |
| No em dashes | Use commas, periods, or parentheses instead. |

---

## Comment Formula

```text
<Direct observation or request>

<Why it matters, only if needed>

<Concrete next action>
```

---

## Examples

### Request change

```markdown
Buenísimo el enfoque. Acá separaría este cambio en otro commit porque mezcla la validación con el wiring de UI.

Eso le baja carga al reviewer y hace que el rollback sea más claro si falla la integración.
```

### Approve with a note

```markdown
Está bien encaminado y el scope se entiende rápido.

Dejo aprobado. Para el próximo PR, agregá el link al anterior y al siguiente así la cadena queda navegable.
```

### Ask for split

```markdown
Este PR supera el presupuesto de 400 líneas cambiadas, así que necesitamos dividirlo o justificar `size:exception`.

Mi sugerencia: primero foundation + tests, después integración, después docs. Así cada review tiene inicio y fin claros.
```

---

## Pitfalls

1. **Leading with praise before the actionable point.** Start with the request or observation — warmth can follow.
2. **Writing too much.** Long comments dilute the signal. Prefer 1-3 short paragraphs.
3. **Forgetting the "why".** Always explain the technical reason behind a change request.
4. **Nitpicking every detail.** Focus on the highest-value feedback, not every preference.

---

## Verification Checklist

- [ ] Comment starts with the actionable point or observation
- [ ] Technical reason is included (if requesting a change)
- [ ] Concrete next action is stated
- [ ] Comment is 1-3 paragraphs or a tight bullet list
- [ ] Language matches thread context (Rioplatense Spanish for Spanish threads)
- [ ] No em dashes used

---

## Commands

```bash
# Inspect a PR before writing review feedback
gh pr view <PR_NUMBER> --json title,body,additions,deletions,changedFiles
```
