# Obsidian Plugin Learnings

## YAML Custom Parser

**Gotcha**: Custom YAML parser corrupts files when values contain special chars.
- Always escape `\n`, `\r`, `\\`, `\"` on write
- Always unescape on read
- Textarea inputs (descripcion fields) inject literal newlines — must escape them
- The Obsidian `metadataCache` / `frontmatter` API is safer but requires `processFrontMatter`

## API / RequestUrl vs Fetch

**Gotcha**: `requestUrl` from Obsidian bypasses browser CORS (runs in Node.js context) but does NOT bypass IP geo-blocking.
- Binance API returns HTTP 451 (Unavailable For Legal Reasons) from Venezuela
- `fetch()` in Obsidian browser context adds CORS restrictions
- Use `requestUrl` for most APIs; fall back to alternative sources when geo-blocked
- Always log the full API response before matching fields

## Type System

**Gotcha**: `TFolder.children` returns `TAbstractFile[]`, not `(TFile | TFolder)[]`.
- Cast: `folderObj.children as (TFolder | TFile)[]`
- Check with `instanceof TFile` / `instanceof TFolder` before accessing properties

## TypeScript Configuration

**Gotcha**: TypeScript puede fallar con "No inputs were found in config file" cuando el path del proyecto contiene espacios (ej: `D:\Obsidian Files\...`). El `exclude` default incluye el directorio del proyecto, y con espacios en el path el glob matching puede fallar. Fix: agregar `"exclude": ["node_modules"]` explícito en `tsconfig.json`. Con esto, el `include: ["src/**/*.ts"]` funciona correctamente.

## Import Patterns

**Gotcha**: `esbuild` succeeds with broken `import type` paths because type-only imports are erased at bundle time.
- `tsc` still catches them — always run both
- Paths from `src/modals/` to `src/main.ts` must use `../main`, not `./main`

## State Mutation

**Gotcha**: `Array.sort()` mutates in-place.
- Always use `[...arr].sort()` or `arr.toSorted()` in views
- getDeudas() must return shallow copies: `{ ...deuda }`, not mutate the parsed object

## File Operations

**Gotcha**: `updateFile()` silently drops the markdown body when no body argument is passed.
- Pass regenerated heading or existing body when editing
- Non-string values (arrays like receta) must be `JSON.stringify()` before passing to YAML

**Gotcha**: `vault.createFolder()` y `vault.create()` (para archivos) lanzan "Folder already exists" por race conditions con el índice asincrónico del vault. `getAbstractFileByPath()` puede retornar null aunque la carpeta exista en disco.
- Siempre wrappear en try-catch con reintento: si falla, volver a llamar `getAbstractFileByPath()`
- Usar `adapter.exists()` para verificar el filesystem real, no solo el índice del vault
- `vault.create()` para archivos crea carpetas padre automáticamente y puede fallar igual

**Gotcha**: `window.prompt()` no es confiable en Electron/Obsidian — puede no mostrarse o aparecer oculto. Usar siempre un Modal propio de Obsidian. `window.confirm()` sí funciona correctamente.

## View Lifecycle

**Patrón**: Para auto-refrescar vistas al cambiar de pestaña, usar `registerEvent` con `workspace.on("active-leaf-change")` y un guard `firstRender`:
- Sin esto, `onOpen()` solo se dispara al crear la vista, no al revelarla
- El guard evita doble renderizado en la carga inicial

## Settings

**Gotcha**: `DEFAULT_SETTINGS` solo aplican en instalaciones nuevas del plugin. Usuarios existentes tienen su `data.json` ya guardado y no reciben nuevos defaults automáticamente. Nuevas categorías deben agregarse manualmente en el SettingTab.

## Dev Workflow

**Gotcha**: El directorio del proyecto de desarrollo NO es el vault de Obsidian. Cada `npm run build` genera `main.js` en la raíz del proyecto, pero Obsidian carga el que está en `.obsidian/plugins/<id>/` del vault real. Soluciones:
- Script post-build que copie archivos al vault
- Symlink: `New-Item -ItemType SymbolicLink` de `main.js` del vault apuntando al del proyecto

## Plugin Instance Access from Tools

**Patrón**: Los tools registrados vía `registerTool()` reciben `(App, args)` pero no tienen acceso al plugin ni a settings. Para que un tool lea API keys o config del usuario:
- Crear `setPluginInstance(plugin)` / `getPluginInstance()` en `settings.ts` (mismo patrón que `setSpobBaseUrl`)
- Llamar `setPluginInstance(this)` en `onload()` del plugin
- El tool importa `getPluginInstance` y accede a `plugin.settings`, `plugin.getApiKey()`, etc.
- **CRÍTICO**: limpiar con `setPluginInstance(null)` en `onunload()` — si el plugin se desactiva y reactiva, una instancia stale causa crashes o datos viejos.

## Community Review Compliance

**Gotcha**: El bot de review de Obsidian rechaza automáticamente ciertos patrones de código. Los hard fails confirmados:
- **`innerHTML`**: prohibido. Usar `createEl`, `createSpan`, `createDiv` y DOM methods en su lugar. El resultado visual es idéntico.
- **`fetch()` crudo**: rechazado. Usar `requestUrl()` de la API de Obsidian — ya viene importado en `import { requestUrl } from "obsidian"`. `requestUrl` devuelve `{ status, json }` con JSON ya parseado (no un `Response` con `.json()`).
- **`setAttr()`**: es parte de la API de Obsidian (agregado a HTMLElement), no un problema de review.

- **Command IDs con prefijo del plugin**: el bot marca warning cuando el ID incluye el plugin ID (ej: `supsync-sync-now`). Obsidian ya namespacing automáticamente por plugin. Usar IDs cortos: `sync-now`, `sign-in`, `open-settings`.

- **`onunload()` debe retornar `void`**: La firma de `Plugin.onunload()` espera `void`. Si la lógica de cleanup es asincrónica, wrappear en `void (async () => { ... })()`. Lo mismo aplica para callbacks de `addCommand`: deben ser `() => void`, no `async () => {}`.

- **`app.setting` no está en los tipos de Obsidian**: El bot rechaza `as any` y `@typescript-eslint/no-explicit-any`. Usar declaration merging con un `.d.ts`:
```ts
// src/obsidian-extensions.d.ts
import "obsidian";
declare module "obsidian" {
    interface App {
        setting: {
            open(): void;
            openTabById(id: string): void;
        };
    }
}
```
Esto permite `this.app.setting.open()` sin casts ni eslint-disables.

- **`.obsidian/` hardcodeado en defaults**: La carpeta de configuración es configurable por el usuario. El bot rechaza hardcodear `.obsidian/` en `DEFAULT_SETTINGS` y en placeholders. Usar `app.vault.configDir` en runtime para excluirla dinámicamente. Nunca incluir `.obsidian/` como string literal en defaults o ejemplos.

## API Version Compatibility (`no-unsupported-api`)

**Gotcha**: El bot marca `no-unsupported-api` cuando el código usa APIs más nuevas que `minAppVersion`. Las versiones exactas están en `node_modules/obsidian/obsidian.d.ts` con `@since`. Reemplazos confirmados:

- `fileManager.trashFile()` → @since 1.6.6. Si `minAppVersion >= 1.6.6`, usar `fileManager.trashFile(file)`. Si `minAppVersion < 1.6.6`, usar `vault.trash(file, true)` (@since 0.9.7).
- `workspace.revealLeaf()` → @since 1.7.2. Reemplazar con `workspace.setActiveLeaf(leaf, false, true)` (@since 0.16.3).
- `PluginSettingTab.display()` → deprecated @since 1.13.0. Extraer lógica a `private render()`, hacer que `display()` delegue en `render()`, usar `this.render()` para refrescos internos.
- `JSON.parse()` retorna `any` → siempre tipar explícitamente (`as MiTipo[]`, `as unknown`) para evitar `no-unsafe-assignment`.
- `HTMLElement.createEl("input", { type: "checkbox" })` ya retorna `HTMLInputElement` por overloads genéricos — el `as HTMLInputElement` es redundante y el bot lo marca como `no-unnecessary-type-assertion`.

**Gotcha**: Las reglas del bot pueden contradecirse entre rounds. `no-unsupported-api` rechaza APIs más nuevas que `minAppVersion`, pero `no-deprecated-api` pide usar esas mismas APIs (ej: `vault.trash` → prefiere `fileManager.trashFile`). La solución es bump `minAppVersion` al máximo requerido por las APIs que el bot prefiere — en este caso 1.6.6.

**Gotcha**: `setActiveLeaf(leaf, pushHistory, focus)` tiene la firma deprecada. La forma nueva es `setActiveLeaf(leaf, { focus: true })` — ambas son @since 0.16.3, así que son seguras con cualquier minAppVersion ≥ 0.16.3.

## Vault Binary Storage

**Gotcha**: `vault.createBinary(path, ArrayBuffer)` crea un TFile correctamente registrado en el vault. Para leer la URL del recurso: `vault.getResourcePath(file)` devuelve una URL `app://` usable en `<img>` y `<embed>`.
- Eliminar archivos binarios: intentar `vault.delete(file)` con TFile; si no está en caché, fallback a `vault.adapter.remove(path)`.
- PDF preview con `<embed>` no es confiable cross-platform en Obsidian — usar botón "Ver PDF" con `openLinkText()` como fallback.

## Obsidian Releases

**Gotcha**: `versions.json` es obligatorio para que Obsidian detecte nuevas versiones en community plugins. Mapea cada versión a `minAppVersion`. Debe estar en la raíz del repo, en el branch `main`. El bot de Obsidian IGNORA los GitHub releases — solo lee `versions.json` + `manifest.json` del branch default.

**Gotcha**: `versions.json` NO debe incluirse en los assets del release de GitHub. Solo `main.js`, `manifest.json` y `styles.css` son soportados. El bot rechaza archivos extra en los assets. El `versions.json` va en el repo (main branch) pero no en los release assets.

**Gotcha**: El bot de review solo lee el branch `main` de GitHub. Cambios pusheados a branches como `staging` o `staging2` NO son detectados. Hay que mergear a `main` para que el bot los vea.

**Gotcha**: El campo `name` en `manifest.json` solo acepta caracteres ASCII. Tildes, eñes y otros caracteres Unicode son rechazados por el bot con el error "This name is not allowed in the directory". Ej: "Mi Agrupación" → rechazado; "Mi Agrupacion" → aceptado. El campo `id` sí permite guiones y lowercase sin restricción.

**Gotcha**: `gh release create` con `--notes` falla en Windows si hay caracteres especiales (comillas, tildes). Usar `--notes-file` con un archivo temporal.

**Gotcha**: El bot de review recomienda artifact attestations (GitHub Actions) para `main.js` y `styles.css`. No es hard-fail pero suma. Se configura con `actions/attest-build-provenance@v2` en un workflow disparado por tag push. Requiere `id-token: write` en los permissions del workflow.

**Gotcha**: `actions/attest-build-provenance@v2` puede fallar con "Resource not accessible by integration" en repos personales si el repo no tiene habilitado el soporte de attestations a nivel organización/cuenta. Si falla, es seguro remover el paso — es opcional y no bloquea la aceptación del plugin.

**Gotcha**: Los tags de release NO deben tener prefijo "v". Obsidian compara el string exacto del campo `version` en `manifest.json` contra el tag del release de GitHub. Si el manifest dice `"0.6.0"` pero el tag es `v0.6.0`, el plugin no se puede instalar ("no GitHub release with that version has been published yet"). Esto pasó dos veces (Research_and_Paper y Audio_Transcript). Fix: (1) eliminar releases/tags con "v" y recrearlos sin prefijo, (2) agregar validación en el workflow: `if: startsWith(github.ref_name, 'v')` → `exit 1`.

**Patrón**: El workflow de release debe aceptar ambos patrones de tag (`[0-9]*.[0-9]*.[0-9]*` y `v[0-9]*.[0-9]*.[0-9]*`) en el trigger para que los tags con "v" disparen el CI y fallen con mensaje claro en vez de ser ignorados silenciosamente. Sin el segundo patrón, un push de `v0.6.0` crea el tag en GitHub pero nunca ejecuta el workflow.

## Vault Enumeration Review Compliance

**Gotcha**: El bot de review de Obsidian recomienda no enumerar archivos del vault (`getMarkdownFiles`, `getAllLoadedFiles`, `getFiles`) porque le da al plugin acceso a todas las rutas del vault. Es una recomendación, no hard-fail, pero puede escalar.

**Patrón de fix en 3 niveles**:
1. **Funcionalidad core que requiere scan completo** (ej: indexador de transcripciones que busca callouts): documentar con un comentario por qué es necesario ("this is the plugin's core indexing feature — it must search the vault").
2. **Features nice-to-have que escanean el vault** (ej: agregar cualquier nota como contexto de chat): eliminar el scan, usar solo datos ya cacheados o indexados.
3. **Listado de carpetas** (ej: dropdown de "carpeta de grabaciones"): usar `vault.getRoot().children` en vez de `getAllLoadedFiles()`. Solo muestra carpetas raíz — es más performante y no deep-enumera.

## Exchange Rates (USDT / VES)

**Gotcha**: Binance API (`api.binance.com/api/v3/ticker/price?symbol=USDTVES`) está geo-bloqueada desde IPs de EEUU. Fly.io región IAD (Virginia) recibe HTTP 200 con mensaje de "restricted location". Usar DolarAPI (`ve.dolarapi.com/v1/dolares`) como fuente primaria desde servidores en EEUU.

**Gotcha**: DolarAPI devuelve entradas con `nombre` diferente según la fuente: `"Dólar"` para oficial y `"Paralelo"` para paralelo. No asumir que todas las entradas tienen `nombre: "Dólar"`. Match por `fuente: "paralelo"` sin filtrar por nombre.

**Patrón**: Al construir sistemas multi-fuente de tasas de cambio, implementar fallback en cadena: intentar fuente A → si falla, fuente B → si falla, usar caché stale → si no hay caché, error. Agregar endpoint `/admin/set-rate` para override manual como último recurso.

## Mobile Sync (Plugin Settings vs Vault Data)

**Gotcha**: `data.json` (plugin settings) se guarda en `.obsidian/plugins/<id>/` que es almacenamiento interno del plugin — NO viaja con Obsidian Sync ni iCloud. Solo los archivos del vault (.md, adjuntos) se sincronizan. Consecuencia: en un segundo dispositivo el plugin arranca con defaults aunque los datos del vault estén sincronizados.

**Solución**: Auto-detección de libros desde el filesystem. Escanear la carpeta base buscando subdirectorios que contengan carpetas de datos (`Clientes/`, `Transacciones/`, etc.) y agregarlos automáticamente a `libros` en settings. Triple fallback: (1) índice del vault, (2) búsqueda case-insensitive en root, (3) `adapter.list()` a nivel filesystem real.

## Mobile vault index timing

**Gotcha**: En mobile (iOS), el índice virtual del vault (`getAbstractFileByPath`, `getRoot().children`) puede no estar poblado durante `onload()`. El plugin carga antes de que Obsidian termine de indexar. `getAbstractFileByPath` devuelve null aunque la carpeta exista físicamente. Solución: usar `adapter.list()` y `adapter.exists()` como fallback — estos leen el filesystem real, no el índice.

## Case Sensitivity (Windows vs iOS)

**Gotcha**: Windows es case-insensitive, iOS es case-sensitive. Una carpeta `OrderManager` creada en Windows podría matchear con `ordermanager`, pero en iOS eso son dos carpetas distintas. Solución: al buscar la carpeta base, hacer comparación case-insensitive (`toLowerCase()`) y corregir el `baseFolder` almacenado para que coincida con el casing real del disco.

## Ticket / Canvas Image Generation

**Patrón**: Para generar imágenes sin dependencias externas (html2canvas), usar `document.createElement("canvas")` con `fillText()` manual. Dibujar fondo blanco, textos con fuentes del sistema, y exportar con `canvas.toBlob("image/png")`. Para compartir en iOS: `navigator.share({files: [new File([blob], ...)]})` abre el share sheet nativo con contactos. Fallback: `navigator.share({text})` para navegadores que no soportan file sharing, y `URL.createObjectURL + <a>.click()` para descarga directa.

## Book Auto-Discovery

**Patrón**: `discoverBooks()` no debe confiar solo en el índice del vault. Mergear resultados de `getAbstractFileByPath` + `TFolder.children` (índice) con `adapter.list()` (filesystem real) usando `[...new Set([...a, ...b])]`. El índice puede estar incompleto en mobile — el adapter nunca miente.

**Patrón UX**: Para "Carpeta base", usar dropdown con `vault.getRoot().children` (carpetas raíz) en vez de solo texto libre. Si la carpeta actual no matchea ninguna raíz por casing, mostrarla como opción "actual". El botón "Detectar" ejecuta `discoverBooks()` y persiste libros + baseFolder detectados.

**Gotcha**: `customColorPalette` no existe en la versión 2.23.7. La API correcta es `colorPalette` con estructura anidada: `{ elementStroke: [...], elementBackground: [...], canvasBackground: [...] }`.

**Gotcha**: `startupScriptPath` es relativo a la raíz del vault, DEBE incluir `.md`, y el plugin usa `vault.getFileByPath()` (no `getAbstractFileByPath()`) para resolverlo.

**Gotcha**: `runStartupScript()` ejecuta el contenido CRUDO del archivo como AsyncFunction. NO extrae código de bloques markdown. Las fences ` ```js ` causan SyntaxError. Startup scripts deben ser JS puro.

**Gotcha**: Los hooks (`onFileOpenHook`) se setean como propiedades de `ea`. `ea.getExcalidrawAPI()` retorna null sin vista activa. Scripts en `Downloaded/` son tratados como de la tienda — los propios van fuera.

## Mobile View Activation

**Gotcha**: `workspace.getRightLeaf(false)` asume un layout con sidebar derecho que solo existe en desktop. En mobile (Android/iOS) Obsidian usa single-pane sin sidebars — `getRightLeaf()` devuelve `null` y la vista nunca se abre.
- Fix: usar `workspace.getLeaf(true)` que funciona en ambas plataformas.

**Gotcha**: `addRibbonIcon` no dispara el evento click/touch en algunos dispositivos Android (confirmado en Redmi 8). El icono se ve pero al tocarlo no pasa nada.
- Fix: agregar un `addStatusBarItem()` como alternativa mobile-friendly. El status bar usa un mecanismo de eventos distinto que sí funciona en todos los dispositivos. También sirve la paleta de comandos (`addCommand`).

## MarkdownRenderer Component Lifecycle

**Gotcha**: `MarkdownRenderer.render(app, markdown, el, sourcePath, component)` requiere un `Component` como 5to argumento para manejar el ciclo de vida de los hijos renderizados. Si se usa la instancia del plugin (`this.plugin`), el bot la rechaza ("lifecycle is too long, can cause memory leaks"). Si se usa `""` no compila porque no es `Component`.
- Fix: usar `this` cuando el render ocurre dentro de un Modal o ItemView (ambos extienden `Component`). Para tipos estrictos: `this as unknown as Component`.

## requestUrl and AbortSignal

**Gotcha**: `requestUrl()` no tiene parámetro `signal` para `AbortController`. Las funciones de transcripción necesitan cancelar requests en curso. Solución: wrapper con `Promise.race` contra el evento `abort` del signal. Para tipo estricto, usar `as RequestUrlParam` en vez de type annotation porque el spread `{ url, ...rest }` no matchea exactamente.

## activeDocument Availability

**Gotcha**: El bot recomienda `activeDocument` en vez de `document` para compatibilidad con ventanas popout, pero `activeDocument` NO está exportado en los tipos de Obsidian. Revertir a `document` — es un warning, no error.

## Audio Recording: ScriptProcessorNode → AudioWorklet

**Gotcha**: `createScriptProcessor()` y `onaudioprocess` están deprecados (2014). La API moderna es `AudioWorkletNode`. El worklet processor puede inyectarse inline vía Blob URL sin archivos externos:
```ts
const blobUrl = URL.createObjectURL(new Blob([WORKLET_CODE], { type: "application/javascript" }));
await audioCtx.audioWorklet.addModule(blobUrl);
URL.revokeObjectURL(blobUrl);
```
Pausa se maneja con `port.postMessage({ paused: true })` en vez de setear `onaudioprocess = null`.

## Modal open() Promise Pattern

**Patrón**: `Modal.open()` retorna `void`. Para modales que necesitan devolver un valor asincrónico (confirmación, selección), crear un método `prompt()` separado que retorne `Promise<T | null>` e internamente llame a `super.open()`. Esto evita el conflicto de tipos con el `open()` de la clase base.
```ts
open(): void { super.open(); }
prompt(): Promise<T | null> { return new Promise(resolve => { this.resolve = resolve; super.open(); }); }
```

## i18n / Localization

**Patrón**: Para multi-idioma, usar `getLanguage()` de Obsidian que devuelve el ISO code configurado por el usuario (default `"en"`). Los códigos disponibles están en [obsidian-translations](https://github.com/obsidianmd/obsidian-translations?tab=readme-ov-file#existing-languages).

Estructura:
```
src/i18n/
  index.ts      → initLocale() y t(key, params?)
  en.json       → fallback (siempre presente)
  es.json       → idiomas adicionales
```

**initLocale()**: llamar en `onload()` después de `loadSettings()`. Lee `getLanguage()`, selecciona el locale o cae en `en`.

**t(key, params?)**: busca en el locale actual, fallback a `en`, fallback al key crudo. Soporta `{param}` con reemplazo via `String(v)`:
```ts
t("plugin.connected", { email: user.email, vault: this.vaultName })
// → "SupSync: Connected as foo@bar.com to MyVault"
```

**Gotcha**: Los locales deben importarse como JSON (`import en from "./en.json"`). Requiere `resolveJsonModule: true` en tsconfig. esbuild maneja JSON nativamente sin config extra.

**Gotcha**: Las keys deben ser consistentes entre todos los locale files. Si falta una key en un locale, `t()` hace fallback a `en.json`. Si tampoco está en `en`, devuelve el key crudo como string.

## Promise-in-void-context Patterns

**Gotcha**: El bot marca "Promise returned in function argument where a void return was expected" en varios patrones. No solo en async callbacks — también en callbacks sincrónicos con retorno implícito.

### Sync callbacks with implicit return

Arrow functions without block body return the expression value. Si no es `void`, TypeScript advierte:

```ts
// MAL: .onChange((v) => (this.sector = v)) — la asignación retorna string
// MAL: .forEach((t) => d.addOption(t, t)) — addOption retorna DropdownComponent
// BIEN:
.onChange((v) => { this.sector = v; })
.forEach((t) => { d.addOption(t, t); })
```

### Async in setInterval/setTimeout

```ts
// MAL: setInterval(() => this.pullChanges(), ms) — pullChanges retorna Promise
// BIEN:
setInterval(() => { void this.pullChanges(); }, ms)
```

### Async callback to constructor expecting void

Cuando un constructor/model espera `(arg) => void` pero necesitás async:

```ts
// MAL: new LoginModal(app, async (email) => { ... })
// BIEN:
new LoginModal(app, (email) => { void (async () => {
    ...
})(); })
```

## Eliminating unsafe-any in Views with ScanResult<T>

**Patrón**: Los views que consumen datos de `scanRecords()`/`scanAllRecordsInCycle()` reciben `Record<string, unknown>` y generan docenas de warnings de unsafe member access. La solución es tipar en la capa de datos con un generic:

```ts
// En data/manager.ts
export interface ScanResult<T> {
    file: TFile;
    data: T;
}

// scanAllRecordsInCycle retorna tipos concretos:
Promise<{
    visitas: ScanResult<Visita>[];
    vidaComunitaria: ScanResult<VidaComunitaria>[];
    procesoEducativo: ScanResult<ProcesoEducativo>[];
}>

// El cast se hace UNA vez en el manager:
visitas: visitas.map(r => ({ file: r.file, data: r.data as unknown as Visita }))
```

Los views importan `ScanResult` y usan tipos concretos — se eliminan TODOS los unsafe-any warnings de una vez. Los type guards (`Array.isArray`, `typeof x === "string"`) se vuelven innecesarios porque los tipos ya garantizan el shape.

## Line Count Management

**Gotcha**: El límite de 300 líneas por archivo fuente se viola fácilmente en plugins Obsidian que tienen modals complejos y vistas con mucha lógica de UI. Archivos que típicamente exceden:
- `data/manager.ts` — CRUD + file I/O + templates (extraer file I/O a `data/files.ts`)
- Modales con formularios grandes — extraer el form a un componente separado o helper
- `settings.ts` — separar secciones de settings en tabs o archivos por sección

No partir archivos sin consultar al usuario, pero señalarlos proactivamente cuando se detecten.
