---
name: presentations
description: "Trigger: presentacion, presentación, slides, diapositivas, PowerPoint, PPTX, talk, charla, keynote, deck, pitch. Design structure and content together, then generate .pptx files for refinement."
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.2"
  tags: [presentations, slides, pptx, powerpoint, talks, design]
  related_skills: [cognitive-doc-design]
---

## When to Use

Use this skill when the user wants to create a presentation — technical talks, business pitches, training, conference talks, lightning talks, project demos.

Don't use for:
- Documentation or READMEs — use `cognitive-doc-design` skill
- Simple text documents — use a document format, not slides

---

## Workflow (5 phases)

```
DISCOVERY  →  STRUCTURE  →  CONTENT  →  GENERATE  →  REFINE
   ↑                                                      │
   └──────────────────────────────────────────────────────┘
```

### Phase 1: Discovery

Ask these questions. Do NOT skip — bad presentations start with bad assumptions:

1. **Audience**: Who are they? (technical, executive, mixed, general public)
2. **Goal**: What should they think/feel/do after this talk?
3. **Format**: Talk length, Q&A?, live demo?, conference/meeting?
4. **Constraints**: Brand colors, template required, max slides?

**Output**: A single sentence that captures the core message. If you can't state it in one sentence, the talk isn't focused enough.

### Phase 2: Structure

Build the slide outline BEFORE writing content. Use this framework:

| Pattern | Use for | Slide count |
|---------|---------|-------------|
| Situation-Complication-Resolution | Problem-solving talks | 8-12 |
| Past-Present-Future | Vision/roadmap talks | 10-15 |
| Feature-Benefit-Proof | Sales/demo pitches | 8-10 |
| What-Why-How | Educational/training | 12-20 |
| Hook-Problem-Solution-Examples-Action | Keynotes | 10-15 |

For each slide, define: **type**, **title**, **key message** (one sentence the audience must remember).

**Rules**:
- Max one idea per slide
- 10/20/30 rule as default starting point (10 slides, 20 min, 30pt font minimum)
- Opening slide: hook or promise
- Closing slide: call to action

**Output**: Numbered slide outline. Do NOT proceed until user approves the structure.

### Phase 3: Content

For each approved slide, write the content using these rules:

- **Titles**: Action-oriented, 1-7 words. "Why X Matters" not "Introduction to X"
- **Bullets**: 3-5 max per slide. Each bullet = one idea. No full sentences unless quoting.
- **Code**: Show only the essential. Highlight the key line. Use `assets/generate_pptx.py` code slide type.
- **Data**: Prefer one chart/table per slide. Include the insight as the title.

**Output**: Complete content for all slides. User must approve before generation.

### Phase 4: Generate

Create a JSON file and run the generator script. See `assets/generate_pptx.py` for the JSON schema and usage.

**Before running**, verify:
- python-pptx is installed (`python -c "from pptx import Presentation"`)
- If not: install with `pip install python-pptx` or `python -m pip install python-pptx`
- The script is at `skills/presentations/assets/generate_pptx.py` (resolve full path at runtime)

Command:
```bash
python <path-to-skill>/assets/generate_pptx.py input.json output.pptx
```

**Python discovery**: On Windows, try multiple Python installations. The venv Python might lack pip. Use `Get-Command python -All` to find available installations, then test each with `-c "from pptx import Presentation"`.

The script supports these slide types:
- `title` — title slide with subtitle, author, date
- `section` — section divider with large centered title
- `bullets` — title + bullet list (2 levels of nesting)
- `content` — title + free text paragraphs
- `code` — title + syntax-highlighted code block
- `two_column` — title + two text columns side by side
- `image` — title + image (local path or URL, auto-downloaded)
- `mermaid` — title + Mermaid diagram rendered via mermaid.ink (flowcharts, sequences, ERDs, etc.)
- `blank` — empty slide for custom work in PowerPoint
- `closing` — thank you / call to action slide

Every slide supports optional `notes` for speaker notes.

### Image Sourcing

During Structure and Content phases, identify slides that need images. Options by need:

| Need | Tool | How |
|------|------|-----|
| **Stock photo** (background, generic) | Unsplash API | `python assets/search_stock.py "query" --download N` |
| **Stock photo** (no API key) | Unsplash Source | Use URL `https://source.unsplash.com/1600x900/?<keywords>` directly in JSON |
| **Diagram** (architecture, flow, ERD) | Mermaid | Use `"type": "mermaid"` with `"diagram": "..."` — renders automatically |
| **Hand-drawn diagram** | Excalidraw | User creates, exports PNG, use `"type": "image"` |
| **Illustration** (conceptual) | unDraw | Browse https://undraw.co, download SVG/PNG, use `"type": "image"` |
| **Icon** (bullet decoration) | Heroicons | Download SVG, insert manually in PowerPoint during Refine phase |

For Unsplash API: user needs a free key from https://unsplash.com/developers. Set via `$env:UNSPLASH_ACCESS_KEY`.
For full sourcing reference: `references/image-sourcing.md`.

### Phase 5: Refine

After generation:
1. Open the .pptx in PowerPoint
2. User adjusts visuals (colors, images, alignment)
3. If structural changes needed, return to Phase 2 or 3, regenerate
4. Rehearse timings, adjust content

---

## Critical Rules

1. **Never generate slides before structure is approved**. Bad structure → bad presentation.
2. **One idea per slide**. If a slide has two ideas, split it.
3. **Text is a crutch**. Every slide with >30 words must be justified.
4. **The .pptx is a starting point**, not the final product. PowerPoint is for visual polish.
5. **Respect the user's brand/template**. If they have a .pptx template, use it as the base.

---

## Pitfalls

1. **Skipping discovery questions.** Bad presentations start with bad assumptions. Always ask audience, goal, format, and constraints.
2. **Generating before approval.** Never generate slides before structure and content are approved by the user.
3. **Too much text per slide.** Every slide with >30 words must be justified — text is a crutch, not the message.
4. **Forgetting speaker notes.** Use the `notes` field on every slide — what you say is more important than what's on screen.

---

## Verification Checklist

- [ ] Discovery questions answered (audience, goal, format, constraints)
- [ ] Core message captured in one sentence
- [ ] Structure approved by user before content
- [ ] Content approved by user before generation
- [ ] python-pptx installed and verified
- [ ] .pptx generated and opened for refinement
- [ ] Speaker notes present on key slides

---

## References

- `references/design-principles.md` — Visual design rules, color theory, typography for slides
- `references/image-sourcing.md` — Complete guide to stock photos, diagrams, illustrations, icons
- `assets/generate_pptx.py` — PPTX generation script with full JSON schema (10 slide types)
- `assets/search_stock.py` — Unsplash stock photo search and download
