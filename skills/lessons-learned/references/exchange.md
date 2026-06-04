# Exchange Rates / Currency Learnings

## bcvPrice Must Not Be Rebasing

**Bug**: `_BCV_PRICE` in `tasasCambio` gets corrupted when `rebaseRates()` divides it.
- It's a raw constant (VES per USD), not a rate
- Store in separate settings field: `this.plugin.settings.bcvPrice`
- Save from raw API response BEFORE rebase

## monto_referencia — Freeze at Creation

**Pattern**: Historical accounting cannot change with live rates.
- Add `monto_referencia` field to TransaccionData
- Compute and store at transaction creation time using current rates
- Dashboard uses `monto_referencia || convertir(...)` — frozen value has priority
- Debt payments auto-create transactions with frozen monto_referencia too

## Convertir Formula

**Bug**: Formula was `(monto / rate) * ref_rate` instead of `monto * rate / ref_rate`.
- Only noticeable when rate ≠ 1 (e.g., VES = 0.0018)
- Test all conversion functions with non-trivial values
- The rate means "how many reference units per 1 unit of this currency" (e.g. 1 VES = 0.0018 USD)

## displayFactor

**Pattern**: Bridge between stored rate and human-readable display.
- VES_BCV stores "per 1 VES" (0.0018) but displays "per 1 BCV dollar" (×544.58)
- Best solution: store the rate in the unit the user expects (VES_BCV = 1 per dollar instead of 0.0018 per VES)
- Removes the need for displayFactor entirely

## DolarAPI Field Names

**Discovery**: DolarAPI uses `fuente` ("oficial"), `nombre` ("Dólar"), and `promedio` (price).
- NOT `titulo` as initially assumed
- Always log raw API response structure before writing matching logic
- Parallel rate comes from `fuente: "paralelo"` or `nombre: "Paralelo"`
- USDT rate: `parallel_price / _BCV_PRICE` = USDT in USD terms

## Binance Geo-Block

**Discovery**: Binance returns HTTP 451 from Venezuela.
- No technical workaround available — IP-level block
- Use DolarAPI parallel rate as fallback for USDT
- `requestUrl` doesn't help (it's at the network level, not browser)
