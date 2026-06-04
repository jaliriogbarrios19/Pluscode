---
name: go-testing
description: "Trigger: Go tests, go test coverage, Bubbletea teatest, golden files. Apply focused Go testing patterns."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  tags: [go, testing, bubbletea, teatest, golden-files, coverage]
  related_skills: []
---

## When to Use

- Writing or reviewing Go tests
- Adding test coverage to Go packages
- Testing Bubbletea/TUI flows with `teatest`
- Updating or creating golden files
- User mentions "go test", "coverage", "bubbletea test", "teatest"

Don't use for:
- Non-Go languages — use language-appropriate testing patterns
- Integration tests that need live services — those are deployment tests, not unit/integration

---

## Hard Rules

- Prefer table-driven tests for multiple cases; use `t.Run(tt.name, ...)`.
- Test behavior and state transitions, not implementation trivia.
- Use `t.TempDir()` for filesystem tests; never rely on a real home directory.
- Keep integration tests skippable with `testing.Short()` when they run external commands or slow flows.
- For Bubbletea, test `Model.Update()` directly for state changes; use `teatest` only for interactive flows.
- Golden files must be deterministic; update only through the repo's `-update` path and rerun tests without `-update`.
- Use small mocks/interfaces around system or command execution boundaries.

## Decision Gates

| Target | Test pattern |
|---|---|
| Pure function or parser | Table-driven unit test. |
| Error behavior | Explicit success and failure cases. |
| File operations | `t.TempDir()` plus focused assertions. |
| TUI state transition | Direct `Model.Update()` call with `tea.Msg`. |
| Full TUI interaction | `teatest.NewTestModel()`. |
| Rendered output | Golden file test. |
| Real external command | Integration test; skip in `-short`. |

## Execution Steps

1. Identify behavior under test and the smallest public boundary that proves it.
2. Choose the test pattern from the decision gate.
3. Name cases by scenario, not input mechanics.
4. Assert outputs, errors, state, and side effects explicitly.
5. Run the narrow package test first, then the relevant broader suite.
6. For golden updates: run with `-update`, inspect diff, then rerun without `-update`.

## Pitfalls

1. **Testing implementation instead of behavior.** Test what the function does, not how it's structured internally.
2. **Forgetting `t.Parallel()` on independent table cases.** Slows down test suites unnecessarily.
3. **Golden files with timestamps or random IDs.** Golden files must be deterministic — strip or mock non-deterministic values.
4. **Using `teatest` for simple state tests.** Direct `Model.Update()` is faster and more focused; reserve `teatest` for interactive flows.

## Verification Checklist

- [ ] Table-driven tests use `t.Run(tt.name, ...)` for named cases
- [ ] File operations use `t.TempDir()`
- [ ] Integration tests are skipped with `testing.Short()`
- [ ] Golden files are deterministic (no timestamps, random IDs, or variable output)
- [ ] Bubbletea state tests use direct `Model.Update()`; interactive flows use `teatest`
- [ ] Tests pass both with and without `-short` flag
- [ ] Mocks/interfaces wrap system or command boundaries

## References

- [references/examples.md](references/examples.md) — compact table-driven, Bubbletea, teatest, golden, and command examples.
