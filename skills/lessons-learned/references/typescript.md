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

## Promise.all vs Promise.allSettled for Independent APIs

**Gotcha**: `Promise.all` fails-fast — si una promesa rechaza, TODAS las demás se descartan aunque ya hayan resuelto. Para llamadas a APIs independientes (PubMed ∥ OpenAlex), usar `Promise.allSettled`:
```ts
const [a, b] = await Promise.allSettled([fetchA(), fetchB()]);
const resultsA = a.status === "fulfilled" ? a.value : [];
const resultsB = b.status === "fulfilled" ? b.value : [];
```
Si PubMed está caído, OpenAlex igual entrega resultados. Con `Promise.all`, el usuario se queda sin nada.

## Async Button Disabled vs Handler Logic Mismatch

**Bug**: Button `disabled` condition used `(!wavBlob && !selectedFile)` but handler required `mode === "record" && wavBlob` or `mode === "file" && selectedFile`. User could switch modes while stale source kept button enabled.
- Fix: align disabled to mode-specific checks: `(mode === "record" && !wavBlob) || (mode === "file" && !selectedFile)`
- Also reset opposite source when switching modes (`handleChooseFile` clears `wavBlob`, `handleChooseRecord` clears `selectedFile`)

## Upload Path vs Filename Resolution

**Bug**: Frontend used `uploadData.path` (absolute server path) with fallback to local filename. When `path` was empty/corrupt, relative filename reached backend and file was not found.
- Fix: always use `uploadData.filename` (relative). Backend resolves relative paths against `vault_root` consistently.
- Validate upload response: check `uploadData.ok && uploadData.filename` before proceeding.

## Build Verification Before Release

**Patrón**: Siempre correr `tsc -noEmit -skipLibCheck` localmente antes de crear un tag de release. Evita ciclos de CI fallidos (build → error → fix → commit → tag → push → esperar → falló otra vez). Son 30 segundos locales vs minutos en GitHub. Esto aplica especialmente después de refactors que tocan tipos (fetch→requestUrl, ScriptProcessor→AudioWorklet, casts de Component).

## window.setInterval Return Type

**Gotcha**: `setInterval` y `setTimeout` retornan `number` en tipos de browser, no `NodeJS.Timeout`. Usar `number | null` para IDs de intervalos/timers en vez de `ReturnType<typeof setInterval>` o `ReturnType<typeof window.setInterval>`. Ambos fallan en CI porque `window.setInterval` tiene un tipo diferente según el contexto (DOM vs Node).
