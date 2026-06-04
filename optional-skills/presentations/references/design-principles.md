# Presentation Design Principles

Reference for the AI when advising on slide design. Apply these rules during Phase 2 (Structure) and Phase 3 (Content).

## The 10/20/30 Rule (Kawasaki)

- **10 slides**: Optimal for a 1-hour pitch. Adjust proportionally for other lengths.
- **20 minutes**: Max talk time before Q&A or interactive segment.
- **30pt minimum font**: If text is smaller than 30pt, you have too much on the slide.

## Slide Structure Rules

| Rule | Rationale |
|------|-----------|
| One idea per slide | Audience can only process one concept at a time |
| 3-5 bullets max | Beyond 5, attention fractures |
| Title = key message | The title should tell the story even if they ignore the body |
| No paragraphs | Bullets or single statements only. Dense text = lost audience |
| 6x6 rule (training) | Max 6 words per bullet, 6 bullets per slide |

## Typography

- **Sans-serif** for presentations: Calibri, Helvetica, Arial, Segoe UI
- **Title**: 32-44pt, bold
- **Body**: 18-24pt
- **Code**: 14-16pt, Consolas or Cascadia Code, light text on dark background
- **Never** go below 14pt for any text
- **Contrast ratio** minimum 4.5:1 for body text (WCAG AA)

## Color

- **3-color palette max**: primary, secondary, accent
- **Dark text on light background** for readability in bright rooms
- **Light text on dark background** for code slides and section dividers
- Avoid red/green as sole differentiators (colorblind accessibility)
- Brand colors override defaults — always ask the user first

## Slide Types and When to Use

| Type | Best for | Avoid |
|------|----------|-------|
| Title slide | Opening, setting tone | Putting logos/agenda here |
| Section divider | Signaling topic transitions | Using more than 3-4 in one talk |
| Bullets | Key points, comparisons, features | Full sentences, >5 bullets |
| Content | Explanations, context | Dense paragraphs, long quotes |
| Code | Live coding, architecture, examples | More than 15 lines |
| Two-column | Before/after, pros/cons, comparison | Different font sizes per column |
| Image | Diagrams, screenshots, data viz | Pixelated images, clip art |
| Mermaid | Architecture, flows, ERDs, sequences | Complex diagrams (split into multiple) |
| Blank | Custom layouts in PowerPoint | Using as filler |
| Closing | CTA, contact, Q&A | New information |

## Image Design Rules

- **Full-bleed images**: Extend to slide edges for impact. Remove top accent bar on those slides.
- **Resolution**: Never below 1920×1080 for full-slide images. PPTX will stretch and pixelate.
- **Text on images**: Always add a dark overlay (40-60% opacity black rectangle) before placing text.
- **Attribution**: If required by license, place photographer credit in 8pt text at bottom-right.
- **Consistency**: If using illustrations (unDraw), use the SAME illustration style throughout.
- **Diagrams**: Mermaid with `"theme": "neutral"` works best on light backgrounds. Use `"theme": "dark"` for dark section slides.
- **Placeholder text**: If an image can't be loaded, the script shows a placeholder. Always verify images render before presenting.

## Common Mistakes

1. **Slideuments**: Slides that are also the handout document. Create separate handouts.
2. **Reading slides aloud**: If the audience can read, don't read to them.
3. **Logo on every slide**: Branding goes on the first and last slide only.
4. **Bullet frenzy**: If everything is a bullet, nothing stands out.
5. **Animation overload**: Animations distract. Use none, or exactly one type consistently.
6. **No narrative arc**: Slides are not the talk. The speaker is the talk. Slides support the speaker.

## Data Slides

- One chart per slide
- The slide title should state the insight, not the data source
- Label axes directly — no legends when avoidable
- Highlight the data point that matters, gray out the rest

## Speaker Notes

- Use notes for what you will SAY, not what's on the slide
- Include transitions between slides ("This leads us to...")
- Include timing estimates per slide
- Include questions to ask the audience
