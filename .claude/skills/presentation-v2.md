# Build presentation skill

## Purpose

Generate a scrollable HTML presentation website from a source document (PDF, markdown, or text file). Uses a standard design template with consistent branding, layout patterns, and navigation.

## Trigger

`/presentation [path-to-source-file]`

The source file is the outline/content guide. It can be a PDF, markdown file, text file, or any readable document that contains the presentation content and structure.

## Process

### 1. Read the source document

- Read the file at the specified path
- If PDF, read all pages to extract content
- Identify the presentation structure: title, slides, key messages, data points, callouts

### 1.5. Check for quality issues

- Review all extracted text for spelling, grammar, and punctuation errors
- Fix obvious errors silently (typos, missing full stops, capitalisation)
- If the meaning is ambiguous or the correction could change intent, ask the user for clarification
- Check for consistency in terminology (e.g. "First Strike" vs "first strike" should be consistent)

### 2. Analyse the content and map to slide layouts

For each section of the source document, choose the best layout pattern from the template. Use these guidelines:

| Content type | Layout pattern | Class name |
|---|---|---|
| Title/opening with image | Title slide | `.slide-title` |
| Bold mission/vision statement | Big statement | `.slide-statement` |
| Team announcements, people updates | Announcement list | `.announcement-list` |
| Visual diagram + supporting metrics | Visual with metrics | `.visual-metrics` |
| Big numbers, key metrics | Stat grid | `.stat-grid` |
| 2-4 concepts with descriptions | Numbered card grid | `.card-grid-2`, `.card-grid-3`, `.card-grid-4` |
| Explanation with illustration | Split layout | `.split` or `.split.reverse` |
| Team/category overview with icons | Icon grid | `.icon-grid` |
| Category labels (e.g. ingredients, layers) | Tag cards | `.tag-cards` |
| Sequential process/workflow | Zigzag flow | `.zigzag-flow` |
| Ordered steps in a model | Numbered steps | `.numbered-steps` |
| Cyclical/reinforcing model | Flywheel | `.flywheel-layout` |
| Primary idea + supporting points | Asymmetric cards | `.asymmetric-layout` |
| Open questions or discussion prompts | Question cards | `.question-grid` |
| Side-by-side comparison | Summary boxes | `.summary-boxes` |

**Key rules:**
- One concept per slide - never overload
- Every slide gets an h2 heading and optional subheading paragraph
- Add a `.callout` at the bottom of slides that have a key insight or takeaway
- Use `.badge` spans for section labels (e.g. "Worked Example", "Our Strategy")
- Add `.animate` classes to elements for scroll-triggered fade-in
- Use `.text-muted` spans within statement text to create emphasis contrast (lighter colored words vs dark)

### 3. Build the HTML

- Read the template: `scripts/templates/presentation_template_v2.html`
- Copy the full `<head>` section (includes all CSS and design tokens)
- Copy the navigation and script sections
- For each slide, use the appropriate commented-out pattern from the template
- Populate with actual content from the source document
- Number the slide IDs sequentially: `slide-1`, `slide-2`, etc.
- Update the total slide count in the navigation

### 4. Handle images and branding

**Images:**
- If the source document references images, ask the user for image file paths
- If the user points to an existing presentation folder with images, check for reusable assets (PNGs, SVGs)
- Use relative paths from the presentation HTML file to the images
- For illustrations that don't exist as files, create simple inline SVGs using the design system colors:
  - Primary strokes: `#B8D4F0` (light) or `#1B2559` (dark)
  - Fills: `#E8F0FE`, `#D0DFFF`, `#C5D8F7`
- For icon grids, create simple SVG icons (48x48 viewBox, stroke-based, `#B8D4F0` color)

**Corporate branding:**
- If the user provides corporate template screenshots or references a brand style, examine them for logo placement, color palette, and header bar styles
- Add `class="branded"` to `<body>` to enable subtle logo watermark on slides
- The template includes a default Autodesk-style triangle logo; replace the SVG data URI in the CSS if a different brand is needed
- Title and statement slides automatically hide the watermark to keep them clean

### 5. Save and open

- Ask the user where to save the file (suggest a folder near the source document)
- Create a subfolder if needed (e.g. `presentation/`)
- Save as `index.html`
- Open in browser: `open [path]/index.html`

### 6. Iterate

- The user will review and request changes
- Make edits directly to the HTML file
- Changes are typically: copy edits, spacing adjustments, adding/removing slides, swapping layouts

## Design system reference

**Colors:**
- `--navy: #1B2559` - headings, primary text
- `--light-blue: #E8F0FE` - card backgrounds, highlights
- `--card-border: #D0DFFF` - borders, subtle accents
- `--accent-pink: #E96EC0` - emphasis (use sparingly)
- `--body-text: #3C4257` - body copy
- `--callout-bg: #DEEAFC` - callout box background
- `--text-muted: #8BAEE3` - lighter colored emphasis text within statements

**Typography:**
- Font: Inter (Google Fonts CDN), weights 400/600/700/800
- h1: 3.2rem/800, h2: 2.6rem/800, h3: 1.25rem/700, h4: 1.1rem/700
- Body: 1rem/400, line-height 1.6
- Statement text: 2.6rem/800 (for `.slide-statement`)

**Components:**
- Cards: 12px border-radius, 1px border `--card-border`, light-blue header strip
- Callout boxes: `--callout-bg` background, 12px radius, info icon (circled "i") + text
- Badges: uppercase, small, `--light-blue` background, 6px radius
- Navigation: fixed bottom-right, arrow buttons + page counter, keyboard arrows supported
- Announcements: icon (emoji in colored rounded-rect) + heading + description, separated by subtle dividers
- Metric rows: circular icon container + text, stacked vertically

**Slide structure:**
```html
<section id="slide-N">
  <div class="slide-inner">
    <!-- content here -->
  </div>
</section>
```
- Each slide: `min-height: 100vh`, scroll-snap aligned
- `.slide-inner`: max-width 1200px, centered

**Announcement icon types:**
- `.celebrate` - warm orange background, use for promotions/wins
- `.farewell` - light blue background, use for departures
- `.welcome` - light green background, use for new joiners
- `.info` - light purple background, use for general updates

## Template file

`scripts/templates/presentation_template_v2.html`

Contains the full CSS design system, all 16 layout patterns as commented HTML blocks, corporate branding support, navigation, and JavaScript. When building a presentation, read this file and use it as the base.

## Presentation best practices

- **One idea per slide** - if you're cramming, split it
- **Callouts are for the "so what"** - the insight the audience should take away
- **Badges label sections** - use them to group related slides (e.g. "Our Strategy", "Worked Example")
- **Bold key phrases** in card descriptions to aid scanning
- **Stats should be large and central** - if a number matters, make it huge
- **Process flows alternate top/bottom** - odd steps top, even steps bottom
- **Images go on the left by default** - use `.split.reverse` to flip
- **Statement slides create rhythm** - use them to transition between sections with a bold message
- **Announcements group by type** - celebrations first, then farewells, then welcomes, then general info
- **Fix errors proactively** - correct spelling and grammar without being asked; only flag ambiguous cases
