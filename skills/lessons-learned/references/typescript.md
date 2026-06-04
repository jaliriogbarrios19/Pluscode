# TypeScript / Build Learnings

## replaceAll Footgun

**Bug**: `replaceAll("t(")` on source files breaks `.split("T")` in template literals like `` `date-${d.toISOString().split("T")[0]}` ``.
- Use `import { t as i18n }` alias, then manually replace only intended `t(` calls
- Or batch-edit the import first, then do the replaceAll

## esbuild vs tsc

**Discovery**: esbuild and tsc have different resolution behaviors.
- esbuild erases `import type` — broken paths silently pass
- tsc performs full type checking — catches missing imports
- Always run `npx tsc --noEmit` after build

## Array Stringification in YAML

**Bug**: Passing an array directly to `stringifyYaml()` silently converts to `[object Object]`.
- Objects/arrays stored in frontmatter must be `JSON.stringify()` first
- On read, parse back with `JSON.parse()` wrapped in try/catch

## i18n Variable Shadowing

**Gotcha**: `import { t } from "../i18n"` shadows loop variable `for (const t of items)`.
- Rename import: `import { t as i18n }`
- This happens in all views with transaction/debt iteration loops

## Async Button Disabled vs Handler Logic Mismatch

**Bug**: Button `disabled` condition used `(!wavBlob && !selectedFile)` but handler required `mode === "record" && wavBlob` or `mode === "file" && selectedFile`. User could switch modes while stale source kept button enabled.
- Fix: align disabled to mode-specific checks: `(mode === "record" && !wavBlob) || (mode === "file" && !selectedFile)`
- Also reset opposite source when switching modes (`handleChooseFile` clears `wavBlob`, `handleChooseRecord` clears `selectedFile`)

## Upload Path vs Filename Resolution

**Bug**: Frontend used `uploadData.path` (absolute server path) with fallback to local filename. When `path` was empty/corrupt, relative filename reached backend and file was not found.
- Fix: always use `uploadData.filename` (relative). Backend resolves relative paths against `vault_root` consistently.
- Validate upload response: check `uploadData.ok && uploadData.filename` before proceeding.
