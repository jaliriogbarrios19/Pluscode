---
name: obsidian-plugin
description: "Trigger: Obsidian plugin, manifest.json, .obsidian, Obsidian API, plugin review, ItemView, PluginSettingTab, vault, requestUrl. Obsidian plugin development patterns, API version compatibility, community review compliance, and accumulated gotchas."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.1"
  tags: [obsidian, plugin, api, review, community]
  related_skills: [lessons-learned]
  platforms: [linux, macos, windows]
---

## When to Use

- Any task involving Obsidian plugin code (files with `import ... from "obsidian"`)
- Project has `manifest.json` with Obsidian plugin structure
- User mentions Obsidian plugin development, Obsidian API, plugin review bot
- Preparing for or responding to Obsidian community plugin review
- Debugging Obsidian-specific issues: views, modals, settings tabs, vault operations

Don't use for:
- Excalidraw plugin scripting — separate API surface (see `lessons-learned` skill)
- Generic TypeScript issues unrelated to Obsidian — see `lessons-learned/references/typescript.md`

## Critical Rules

- **Check API `@since` BEFORE writing code.** Every Obsidian API method has a `@since` annotation in `node_modules/obsidian/obsidian.d.ts`. Compare against `minAppVersion` in `manifest.json`.
- **Never use `innerHTML`.** The review bot rejects it. Use `createEl()`, `createDiv()`, `createSpan()`.
- **Never use raw `fetch()`.** Use `requestUrl()` from the Obsidian API. Note: `requestUrl()` returns `{ status, json, text }` — `json` and `text` are PROPERTIES (already parsed), not methods.
- **Never use heading elements directly.** Use `new Setting(containerEl).setName("Title").setHeading()` instead of `createEl("h2")` or `createEl("h3")`. The bot rejects raw heading elements for UI consistency.
- **Never use `confirm()`.** Neither bare `confirm()` nor `window.confirm()` is accepted. Use a custom Obsidian Modal subclass with buttons.
- **Never use `window.prompt()`.** Unreliable in Electron/Obsidian — use a custom Modal.
- **Always wrap vault operations in try-catch.** Race conditions with async vault indexing cause silent failures.
- **Use `window.setTimeout()` not bare `setTimeout()`.** For popout window compatibility.
- **Async onClick handlers must return void.** Setting's `onClick` expects `() => void`. If the handler needs async work, wrap in `void (async () => { ... })()`.

## Workflow

### Step 1: Load the domain reference

Read `references/obsidian.md` — accumulated gotchas, API compatibility, review bot compliance, patterns, release workflow, and mobile sync.

### Step 2: Verify every API call against minAppVersion

For each Obsidian API used, check `@since` in `node_modules/obsidian/obsidian.d.ts`. Key replacements:

| API | @since | Compatible alternative |
|-----|--------|----------------------|
| `fileManager.trashFile()` | 1.6.6 | `vault.trash(file, true)` (0.9.7) — or bump minAppVersion |
| `workspace.revealLeaf()` | 1.7.2 | `setActiveLeaf(leaf, { focus: true })` (0.16.3) |
| `PluginSettingTab.display()` | deprecated 1.13.0 | Extract `render()` method, delegate from `display()` |

If bot rules contradict (e.g., `no-unsupported-api` vs `no-deprecated-api`), bump `minAppVersion` to the highest required `@since` version.

### Step 3: Apply review compliance rules

- No `innerHTML` → use DOM creation methods
- No `fetch()` → use `requestUrl()` with `{ url, method?, headers?, body? }`
- `requestUrl()` returns `{ status, json, text }` — `json`/`text` are properties, not methods
- `res.status >= 200 && res.status < 300` instead of `res.ok`
- No `confirm()` / `window.confirm()` → custom Obsidian Modal
- No heading elements → `new Setting(containerEl).setName("...").setHeading()`
- `setTimeout()` → `window.setTimeout()`
- `JSON.parse()` results must be explicitly typed (not `any`)
- `requestUrl().json` must be typed with `as` (e.g., `res.json as { results?: T[] }`)
- Release tags without `v` prefix; `versions.json` updated on every release
- Release assets: only `main.js`, `manifest.json`, `styles.css` — never `versions.json`
- Artifact attestations in CI workflow
- **Never create releases manually** — push the tag and let the CI workflow (`release.yml`) build, attest, and create the release

## Pitfalls

1. **Bot rules contradict between rounds.** `no-unsupported-api` rejects newer APIs; `no-deprecated-api` demands the same APIs. Fix: bump `minAppVersion`.
2. **Custom YAML parser corrupts on special chars.** Always escape `\n`, `\r`, `\\`, `\"`.
3. **`Array.sort()` mutates in-place.** Use `[...arr].sort()` or `arr.toSorted()` in views.
4. **Plugin `data.json` doesn't sync.** Implement book auto-discovery from vault filesystem.
5. **Mobile vault index may be empty during `onload()`.** Fallback to `adapter.list()` / `adapter.exists()`.
6. **`DEFAULT_SETTINGS` only applies to new installs.** Existing users need migration logic.
7. **Manual release creates race condition with CI.** If you `gh release create` manually and the CI workflow also runs `gh release create`, it fails with "release already exists". Only push the tag — CI handles the release.
8. **`requestUrl` has no `signal`/`AbortController` support.** Cannot pass `AbortSignal.timeout()`. Remove timeout logic or wrap with `Promise.race`.
9. **`setTimeout` callbacks that return non-void trigger warnings.** For arrow callbacks like `setTimeout(() => expression)`, the expression's return value is the callback's return. Use block body: `setTimeout(() => { expression; })`.

## Verification Checklist

- [ ] `references/obsidian.md` reviewed for relevant gotchas
- [ ] All Obsidian API calls verified against `minAppVersion` via `@since` annotations
- [ ] No `innerHTML`, raw `fetch()`, `confirm()`, or `window.prompt()` in code
- [ ] Headings use `setHeading()`, not `createEl("h2"/"h3")`
- [ ] `setTimeout()` uses `window.` prefix; async onClick handlers wrapped with `void`
- [ ] `JSON.parse()` and `requestUrl().json` results explicitly typed
- [ ] Release tags have no `v` prefix; `versions.json` up to date on main branch
- [ ] Release assets: only `main.js`, `manifest.json`, `styles.css` (no `versions.json`)
- [ ] Release created by CI workflow, not manually
- [ ] `manifest.json` `minAppVersion` ≥ highest `@since` among APIs used

## References

- `references/obsidian.md` — Full domain knowledge: API compatibility, review bot, gotchas, patterns, releases, mobile, exchange rates
