# Optional Skills

Skills that are **not activated by default**. These skills live in `optional-skills/` and are not auto-loaded by the skill loader.

To activate an optional skill, copy it from `optional-skills/<name>/` to `skills/<name>/`. To deactivate, move it back.

## Why optional?

- **Niche integrations** — specific to certain languages or tools (e.g. Go testing)
- **Specialized workflows** — useful but not daily (e.g. presentations, adversarial review)
- **Heavyweight dependencies** — require additional setup or API keys

By keeping them optional, the default skill set stays lean while curated skills remain available.
