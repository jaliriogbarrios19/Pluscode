# UX / User Domain Learnings

## The User Knows Their Domain

**Principle**: When a user says "X and Y are not the same thing", trust them and redesign. The code might be mathematically correct but practically wrong.
- Example: VES and BCV dollar are different economic concepts even if they share a numeric base
- Don't argue with domain expertise

## Naming Matters

**Lesson**: "Negocio" (business) excludes non-commercial users. "Libro" (accounting book) is the correct universal term.
- Always choose the most inclusive, domain-correct term
- Ask the user: "what word would you use?"

## displayFactor is a UX Bridge, Not a Data Model

**Lesson**: Stored rates use consistent units (per 1 base unit). Display factors convert to human units. But the best fix is aligning the stored unit with the expected unit.
- Don't patch display issues with multipliers — fix the data model
- User thinks in "dollars", not in decimal fractions of bolívars

## Venezuela Has Different Rule of Law

**Lesson**: Financial software for Venezuela must handle:
- BCV official rate ≠ parallel market rate
- Both coexist and are equally real
- Users transact in both depending on context
- Geo-blocking of major APIs (Binance 451)
- Daily rate fluctuation is the norm, not the exception
- Manual rate overrides are essential (the user might have local info APIs don't)

## Confirmation Before Destruction

**Lesson**: Every delete action needs `confirm()`.
- Applies to: all views (table rows), all modals (delete button)
- The user WILL accidentally click × at some point

## Selectors: Always Pull from the Source of Truth

**Lesson**: Student/user selectors that only populate from runtime data (imported/manually entered) break the UX when no data exists yet. The selector should always pull from the configuration (the source of truth) as a fallback, and merge with runtime data when available.
- A student dropdown showing zero options with the message "no hay datos" blocks the user from even starting their work
- Pattern: populate first from config/static list, then overlay runtime data for enriched display
- The qualitative and quantitative data paths should be independent - one should never block the other
