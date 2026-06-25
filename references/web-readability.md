# Web & Screen Readability

Guidance for making web pages, dashboards, and HTML documents readable. Based on GOV.UK design system research, WCAG accessibility standards, and reading comprehension studies.

The same Five Principles apply to web content, but **screen reading differs from print** in important ways: readers scan faster, attention is more fragile, and the environment (screen size, brightness, distance) varies enormously.

## Body Text Size

The browser default of 16px is too small for sustained reading.

| Context | Recommended size | Why |
|---------|-----------------|-----|
| **Reading surfaces** (articles, reports, briefs) | **19px** (1.1875rem) | GOV.UK standard. Reduces eye strain ~15-20% vs 16px on sessions over 5 minutes. |
| **UI surfaces** (navigation, labels, cards, filters) | **16px** (1rem) | Acceptable for scanning. Density is correct for metadata-heavy interfaces. |
| **Small labels** (captions, timestamps, tags) | **12-14px** (0.75-0.875rem) | Minimum readable. Never use for body text. |
| **Projected content** (meeting slides, shared screens) | **21-24px** (1.3-1.5rem) | Must be readable from across a room. |

Use `rem` units, not `px`, so text scales with user preferences.

## Line Height

| Context | Line height | Ratio |
|---------|------------|-------|
| **UI text** (labels, nav, cards) | 1.2-1.4 | Compact but legible |
| **Body paragraphs** | 1.5 minimum | Acceptable |
| **Sustained reading** (200+ words) | **1.625** | Optimal. GOV.UK's standard, discovered through large-scale accessibility testing. |
| **Projected/meeting mode** | 1.5-1.6 | Slightly tighter is OK because text is larger |

The 1.625 ratio (roughly 25px leading on 19px text) creates "breathing room" between lines without wasting vertical space. It is measurably better than 1.5 for reading comprehension.

## Line Length (Measure)

Never allow text to stretch across the full viewport width.

| Context | Max characters | CSS |
|---------|---------------|-----|
| **Optimal reading** | **65-75ch** | `max-width: 70ch` |
| **Dyslexic readers** | 50-60ch | `max-width: 55ch` |
| **Presentation slides** | Under 30ch | -- |
| **Cards / sidebar text** | 40-50ch | Natural constraint from column width |

On mobile, the viewport naturally constrains line length. The danger is on wide desktop screens where unbounded text becomes unreadable.

## Paragraph Spacing

Use **margin-bottom, not indentation**, to separate paragraphs on screen. Indentation works in print but is ambiguous on screen where line breaks are unpredictable.

- **15px** (roughly 0.8em) bottom margin is the GOV.UK standard
- Paragraphs should be visually distinct — readers must see where one ends and the next begins at scanning speed
- Between sections (under headings), use **20-32px** spacing

## Heading Hierarchy

Screen scanning is faster and less linear than print scanning. Headings must create **dramatic visual breaks** that the eye catches in peripheral vision.

| Level | Recommended size | Purpose |
|-------|-----------------|---------|
| **H1** | 2.5-3rem (40-48px) | Page title. One per page. |
| **H2** | 1.75-2.25rem (28-36px) | Major sections. The main navigation landmarks. |
| **H3** | 1.25-1.5rem (20-24px) | Subsections within an H2. |
| **H4** | Body size, bold | Minor divisions. Often unnecessary. |

**Heading margins matter as much as heading size.** An H2 with only 8px bottom margin doesn't create sufficient visual pause. Use:
- **H2**: 24-32px top margin, 16-20px bottom margin
- **H3**: 20-24px top margin, 10-15px bottom margin

## Font Family

The right font depends on **reading duration**, not personal preference.

| Surface | Recommended | Why |
|---------|-------------|-----|
| **Navigation, labels, filters** | Sans-serif (system stack) | Optimised for quick scanning at small sizes |
| **Articles, reports, briefs** | Serif (Georgia, Palatino) | Improves comprehension for sustained reading. This is why newspapers and books use serif. |
| **Code, IDs, references** | Monospace | Visual distinction for technical identifiers |

You can — and should — use both in the same page. Sans-serif for the UI chrome, serif for the reading column. This is the pattern used by most quality publications (Guardian, FT, NYT online editions).

## Colour Contrast

WCAG AA requires minimum contrast ratios:

| Text type | Minimum ratio | Example |
|-----------|--------------|---------|
| **Normal text** (<18pt) | **4.5:1** | Black (#000) on white (#fff) = 21:1. Dark gray (#333) on white = 12.6:1. |
| **Large text** (18pt+ or 14pt+ bold) | **3:1** | -- |
| **UI components** (buttons, inputs, icons) | **3:1** | -- |

**Common failures:**
- Light gray text on white (the "designer gray" problem)
- Low-contrast placeholder text in form fields
- Coloured text on coloured backgrounds without checking

**Testing tools:** browser DevTools accessibility audit, WebAIM contrast checker.

## Focus States

For keyboard navigation and accessibility:

- Every interactive element needs a **visible focus indicator**
- Use a **3px solid outline** in a high-contrast colour
- GOV.UK uses `#ffdd00` (bright yellow) — visible on both light and dark backgrounds
- Add `outline-offset: 2px` so the ring doesn't touch the element edge
- **Never** use `outline: none` without providing an alternative focus style

## Responsive Typography

Text must remain readable across devices without requiring zoom.

**Principles:**
- Use `rem` for font sizes (scales with user preferences)
- Set a comfortable base on `<html>` or `<body>` (not a fixed px on every element)
- On mobile (<720px), reduce heading sizes but **never reduce body text below 16px**
- On mobile, line length is naturally constrained — don't add `max-width` that creates horizontal scroll

**Simple responsive scale:**
```css
body { font-size: 1.1875rem; }  /* 19px */

@media (max-width: 720px) {
  body { font-size: 1rem; }  /* 16px — acceptable on mobile */
  h2 { font-size: 1.5rem; }  /* Scale down headings */
}
```

## Print Styles

When generating HTML that might be printed:

- Remove navigation, sidebars, toggle buttons
- Set body background to white
- Ensure headings have `break-after: avoid`
- Cards and panels: `break-inside: avoid`
- Remove decorative backgrounds and shadows
- Ensure sufficient contrast without colour (borders instead of background tints)

## Quick Reference: Reading Surface Checklist

For any page where people will read for 5+ minutes:

- [ ] Body text 19px (1.1875rem) or larger
- [ ] Line height 1.625
- [ ] Paragraph spacing 15px+
- [ ] Line length capped at 70-75ch
- [ ] Serif font for body text
- [ ] H2 at least 1.75rem with 16px+ bottom margin
- [ ] Colour contrast passes WCAG AA (4.5:1)
- [ ] Focus states visible on all interactive elements
- [ ] Print styles hide chrome, keep content
