---
name: lessons-learned
description: "Trigger: learned, lessons learned, aprendido, aprendizaje, lo que aprendimos, recordar aprendizajes. Domain-routed skill covering accumulated patterns, gotchas, bugs, and discoveries."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "2.1"
  tags: [learning, patterns, gotchas, bugs, memory, retrospective]
  related_skills: [judgment-day]
---

## When to Use

- User asks "what did we learn", "aprendizaje", "recordá los aprendizajes"
- A significant bug was just fixed and should be documented for future sessions
- Planning similar work — check relevant domain file BEFORE implementing
- User wants a retrospective on past discoveries

Don't use for:
- Generic documentation — use `cognitive-doc-design` skill
- Adversarial code review — use `judgment-day` skill

---

## Routing Logic

This skill acts as a router. Based on the current task context, load the relevant domain file:

| Context | Domain File |
|---------|------------|
| Obsidian plugin, YAML, views, modals, API calls, Excalidraw | [references/obsidian.md](references/obsidian.md) |
| TypeScript, esbuild, i18n, build errors | [references/typescript.md](references/typescript.md) |
| Exchange rates, currency, tasas, convertir, BCV, USDT | [references/exchange.md](references/exchange.md) |
| UX, naming, user domain, Venezuela-specific | [references/ux.md](references/ux.md) |
| OpenCode config, skills, SDD, agents, provider auth | [references/opencode.md](references/opencode.md) |
| OpenCode config, skills, providers, models, agent setup | [references/opencode.md](references/opencode.md) |

Load ALL domain files when the task spans multiple areas or the user asks for a full retrospective.

---

## Hard Rules

- NEVER repeat a documented gotcha. Check the relevant domain file first.
- After fixing a complex bug or discovering a non-obvious pattern, propose adding it to the appropriate domain file.
- Each domain file entry: one paragraph max — what, why, fix.
- Multiple contexts active → load multiple domain files.

---

## Pitfalls

1. **Skipping domain file check.** Always check the relevant domain file BEFORE implementing — documented gotchas exist to prevent repeat mistakes.
2. **Not documenting after fixes.** When a complex bug is fixed or a non-obvious pattern is discovered, propose adding it immediately — future sessions won't have this context.
3. **Over-documenting.** Each entry is one paragraph max (what, why, fix). Don't turn domain files into essays.

---

## Verification Checklist

- [ ] Relevant domain file(s) loaded based on task context
- [ ] Documented gotchas checked before implementation
- [ ] After bug fix: proposed adding new entry to appropriate domain file
- [ ] Domain file entries are concise (one paragraph: what, why, fix)

---

## References

Domain files referenced via the routing table above.
