# Image Sourcing Guide for Presentations

Reference for the AI when helping the user find images. Each section covers a different need.

---

## Stock Photos (free, high-quality)

### Unsplash
- **Site**: https://unsplash.com
- **API**: Free, 50 req/hour. Register at https://unsplash.com/developers
- **License**: Free for commercial use, attribution appreciated but not required
- **Use the script**: `python assets/search_stock.py "query" --download N`
- **Direct URL format** (no API key, random image):
  `https://source.unsplash.com/1600x900/?<keywords>`

### Pexels
- **Site**: https://pexels.com
- **API**: Free, 200 req/hour. Key at https://pexels.com/api
- **License**: Free for commercial use, attribution appreciated

### Pixabay
- **Site**: https://pixabay.com
- **API**: Free. Key at https://pixabay.com/api/docs
- **License**: Free for commercial use, no attribution required
- **Extra**: Includes vector illustrations

---

## Diagrams & Architecture

### Mermaid (INTEGRATED)
- **Description**: Text-to-diagram. Write code, get rendered diagrams.
- **In the JSON**: Use `"type": "mermaid"` with a `"diagram"` field
- **Themes**: `"default"`, `"neutral"`, `"dark"`, `"forest"`
- **Common diagram types**:

| Type | Mermaid syntax | Use for |
|------|---------------|---------|
| Flowchart | `graph TD` / `flowchart LR` | Architecture, processes |
| Sequence | `sequenceDiagram` | API flows, interactions |
| Class | `classDiagram` | OOP structures |
| State | `stateDiagram-v2` | Lifecycles, state machines |
| ER | `erDiagram` | Database schemas |
| Gantt | `gantt` | Timelines, roadmaps |
| Pie | `pie` | Data breakdown |
| Mindmap | `mindmap` | Brainstorming, outlines |

### Excalidraw
- **Site**: https://excalidraw.com
- **Description**: Hand-drawn style diagrams, collaborative
- **Export**: PNG, SVG. Save .excalidraw files for later editing

### draw.io / diagrams.net
- **Site**: https://app.diagrams.net
- **Description**: Full diagram editor, saves to .drawio XML

---

## Illustrations

### unDraw
- **Site**: https://undraw.co/illustrations
- **Description**: Open-source SVG illustrations, consistent style
- **License**: MIT — free for commercial use
- **Search by keyword**: https://undraw.co/search
- **Customizable**: Change the accent color directly in the URL
  `https://undraw.co/illustrations?primaryColor=<hex>`
- **When to use**: Conceptual slides, onboarding, abstract ideas

### Storyset
- **Site**: https://storyset.com
- **Description**: Animated and static illustrations by Freepik
- **License**: Free with attribution, or premium without
- **Styles**: Multiple (rafiki, bro, amico, cuate, pana)

### Humaaans
- **Site**: https://humaaans.com
- **Description**: Mix-and-match human illustrations
- **License**: CC0 — completely free

---

## Icons

### Flaticon
- **Site**: https://flaticon.com
- **Description**: Largest icon library, multiple styles per icon
- **License**: Free with attribution, premium without
- **Formats**: PNG, SVG, EPS

### Font Awesome
- **Site**: https://fontawesome.com/icons
- **Description**: Icon font and SVGs
- **License**: Free tier has 2000+ icons (solid/brands)

### Feather Icons
- **Site**: https://feathericons.com
- **Description**: Minimal, consistent stroke-based icons
- **License**: MIT — completely free, 280+ icons

### Heroicons
- **Site**: https://heroicons.com
- **Description**: By Tailwind CSS team. Outline and solid variants.
- **License**: MIT — completely free

---

## Quick Decision Table

| Need | Best source | Why |
|------|-----------|-----|
| Background image for title slide | Unsplash | Highest quality, widescreen format |
| Architecture diagram | Mermaid (integrated) | Text-based, fast, version-controllable |
| Hand-drawn process flow | Excalidraw | Warm, approachable style |
| Abstract concept illustration | unDraw | Consistent style, customizable color |
| Single icon for bullet point | Heroicons or Feather | SVG, tiny, MIT license |
| Data breakdown chart | Mermaid pie | No external tool needed |
| Team/people illustration | Humaaans | Mix-and-match, CC0 |
| Animated slide illustration | Storyset | Attention-grabbing for key slides |

---

## Image Resolution Guide for PowerPoint

| Use | Minimum | Recommended |
|-----|---------|-------------|
| Full-slide background | 1920×1080 | 2560×1440 |
| Half-slide image | 1280×720 | 1920×1080 |
| Small inset image | 800×600 | 1280×720 |
| Icon (SVG) | Vector | Vector |

For widescreen 16:9 slides, always prefer landscape images at 16:9 or wider.
