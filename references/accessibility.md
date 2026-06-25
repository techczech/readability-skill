# Accessibility Considerations

## Who Benefits from Readable Documents

All the readability principles help **everyone**, but especially benefit:

- **Dyslexic readers** - struggle with dense text, benefit from chunking and visual guides
- **Non-native speakers** - simpler language and structure aids comprehension
- **Screen reader users** - properly marked headings are essential
- **Low vision users** - larger fonts, more space, shorter lines
- **Attention disorders** - chunked content and clear structure reduce cognitive load
- **People under stress** - approachable formatting reduces barrier to entry

## Key Accessibility Principles

### Headings Must Be Marked with Styles

**Critical:** Use Heading 1, Heading 2, etc. styles - not just bold text.

Why:
- Screen readers use headings to navigate
- Users can jump between sections
- Creates automatic table of contents
- Bold text alone provides no structure for assistive technology

### Text Alternatives for Images

When documents include images or tables:
- Write **functional descriptions** focusing on the textual alternative
- Describe what the image communicates, not just what it shows
- Tables need headers marked properly

### Colour Contrast

WCAG AA requires minimum contrast ratios between text and its background:

| Text type | Minimum ratio |
|-----------|--------------|
| **Normal text** (under 18pt) | **4.5:1** |
| **Large text** (18pt+ or 14pt+ bold) | **3:1** |
| **UI components** (buttons, inputs, icons) | **3:1** |

**Common failures:**
- Light gray text on white backgrounds (the "designer gray" problem — `#999` on `#fff` is only 2.8:1)
- Low-contrast placeholder text in form fields
- Coloured text on coloured backgrounds without checking the ratio
- Text over images or gradients where contrast varies

**How to check:** Use the browser DevTools accessibility audit, the WebAIM Contrast Checker (web tool), or the Colour Contrast Analyser (desktop app). Most design tools (Figma, Sketch) have built-in contrast checking.

**Safe defaults:** Black (`#000`) on white is 21:1. Dark gray (`#333`) on white is 12.6:1. Both are well above the 4.5:1 minimum.

### Colour Cannot Be the Only Indicator

Never use colour as the only way to convey information.

**Bad:** "Items marked in red are compulsory"

**Good alternatives to add:**
- Bolding
- Shapes or outline styles
- Asterisks
- Consistent position
- Different icons

### PDF Accessibility

For accessible PDFs:
1. Start with accessible source document (Word with proper headings)
2. Export/save as PDF with accessibility options enabled
3. Check reading order
4. Ensure all images have alt text
5. Add bookmarks for navigation
6. Test with a screen reader if possible

### Common Issues

**Five most common accessibility issues:**
1. Missing heading structure (just bold instead of heading styles)
2. Images without alt text
3. Links without meaningful text ("click here")
4. Colour-only information
5. Poor reading order in PDFs

## Dyslexia-Specific Considerations

What helps dyslexic readers:
- **Increased line spacing** (1.5 minimum)
- **Shorter lines** (50-60 characters ideal)
- **Sans-serif fonts** (though research is mixed)
- **Larger font sizes** (14pt minimum)
- **Left-aligned text** (not justified)
- **Clear structure** with headings and bullets
- **Bold key phrases** for scanning
- **Avoiding italics** for long passages
- **Cream or light coloured backgrounds** instead of pure white

## Screen Reader Considerations

For screen reader users:
- Proper heading hierarchy (H1, H2, H3 in order)
- Meaningful link text
- Alt text for images
- Table headers marked correctly
- Lists using actual list formatting
- Language specified in document
- Reading order matches visual order
