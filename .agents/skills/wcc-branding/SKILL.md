---
name: wcc-branding
description: Applies Women Coding Community's official brand identity, colour palette, logo and tone of voice to anything generated for WCC, README updates, session materials, decks, diagrams, reports, Slack posts, social copy, badges. Use this skill whenever writing, designing or reviewing content that will be seen by the WCC community, for any WCC programme, not just the Harness Series, so it looks and sounds consistently on-brand.
---

# wcc-branding

Applies Women Coding Community's brand identity, so anything written or designed for WCC looks and sounds consistently like WCC, across any programme or repo, not just one series.

## When to use this

Use this skill whenever generating or reviewing content meant for the WCC community: README updates, session materials, decks, diagrams, generated reports (e.g. an HTML report a skill produces), Slack posts and replies, social copy, badges, or any other public-facing WCC material, for any WCC programme.

## Assets

- `assets/WCC_LogoBlack.png` — primary logo, black seal on white, circular "WOMEN CODING COMMUNITY" wordmark around a black disc with `< WCC >` in white. Use this on light backgrounds. Ask before stretching, recolouring, or cropping the ring text, treat it as a fixed lockup.
- `assets/WCC_Colour_Palette.png` — the official colour system as defined in WCC's Figma, three ramps: Primary, Secondary, Tertiary (values below).

### What's still missing (flag if asked, or if Sonika has more to add)

This folder currently only has the logo (black variant) and the colour palette. A complete brand skill would also want:
- A white/reversed logo variant for dark backgrounds (only the black-on-white version is here so far)
- A minimum-size and clear-space rule for the logo (how small can it go, how much empty space around it)
- The actual brand typeface, if WCC has one beyond a system-font fallback, plus weights
- A short tone-of-voice reference doc, if one exists formally beyond what's captured here
- Guidance on which ramp/shade to use for what (e.g. is shade 40 for backgrounds and 90 for text, or the reverse?)
- A link to the live Figma file, so this skill can be checked against the current version rather than going stale
- Any do/don't examples (logo misuse, colour misuse) if WCC has them

If more of these come out of the private Google Drive, drop them into `assets/` and add a line here referencing each one, same pattern as the two files already listed.

## Colour palette

As defined in WCC's Figma (`assets/WCC_Colour_Palette.png`). Three ramps, each numbered 10 (darkest) to 90/98 (lightest):

**Primary**
| Shade | Hex |
|---|---|
| 10–50 | `#001E2E` |
| 60–95 | `#6A96B4` |
| 98 | `#F6FAFE` |

Note: the source export repeats the same hex across shades 10–50 and again across 60–95, the swatches themselves look like a real gradient, so this may just be an export quirk from Figma rather than five identical shades. Worth double-checking against the live Figma file before treating this ramp as final.

**Secondary**
| Shade | Hex |
|---|---|
| 10 | `#390C00` |
| 20 | `#5D1800` |
| 30 | `#822702` |
| 40 | `#A23E19` |
| 50 | `#C3562F` |
| 60 | `#E46E45` |
| 70 | `#FF8B64` |
| 80 | `#FFB59D` |
| 90 | `#FFDBD0` |

**Tertiary**
| Shade | Hex |
|---|---|
| 10 | `#271900` |
| 20 | `#402D04` |
| 30 | `#594319` |
| 40 | `#735B2E` |
| 50 | `#8D7344` |
| 60 | `#A98D5B` |
| 70 | `#C5A773` |
| 80 | `#E2C28C` |
| 90 | `#FFDEA6` |

Default to darker shades (10–40) for text and key UI on light backgrounds, lighter shades (70–98) for backgrounds and large fills, same logic as any tonal design system. When a series-specific accent is needed (e.g. one highlight colour for a deck), pick from Secondary or Tertiary rather than introducing a new colour outside this system.

**Known discrepancy:** the Harness Series deck (Session 1) used `#164863` (navy) and `#E55807` (orange) as its working palette, these are close to Primary and Secondary but not exact matches. Worth reconciling the deck to the official ramp above if pixel-perfect brand consistency matters, flagging rather than silently fixing, since that deck's already shipped.

Font: no confirmed WCC brand typeface yet, defaulting to **Arial** (or the nearest system sans-serif) until a real one is supplied.

## Tone of voice

- Casual, warm, direct. Write like a colleague explaining something, not a corporate deck.
- British English spelling.
- No em dashes, use a comma or colon instead.
- Minimal exclamation marks, a light touch is fine, don't oversell.
- Confident but not salesy: state what something covers plainly rather than hyping it.

## Writing conventions

- **Slack messages:** use mrkdwn, `*bold*` (single asterisk, not double), plain URLs rather than `<url|text>` pipe-links (they don't render reliably in this workspace), bullets with `•` or `-` for lists of three or more items.
- **Markdown files:** match the existing repo's lint config where one exists (e.g. this repo's `.markdownlint.json` disables MD024, MD036, MD013). Match the existing heading style of whichever repo/file you're editing, don't impose a new convention on top of an established one.
- **Generated reports** (HTML/PDF a skill produces): use the colour palette above for headings, score badges and accents rather than an unrelated palette, and use the logo (`assets/WCC_LogoBlack.png`) in the header or footer where a report has one, so WCC-run tooling visibly looks like WCC output.
- Credit sourced material (diagrams, quotes, external images) inline or in a caption rather than presenting it as original WCC work.
- Keep programme facts (session lists, cadence, facilitators) consistent with that programme's own README rather than restating them from memory, check the relevant file if unsure.

## Facilitators and mission, Harness Series specifically

Session/programme-specific facts belong in that programme's own README, not here, so this skill stays reusable. For the current Harness Series:

- **Sonika Janagill** — Series Lead, Google track
- **Rajani Rao** — Founder/Director WCC, Microsoft track, follows up each session mapping the same patterns to Agent Framework and Foundry
- Mission line to reuse: "empower women to be at the forefront of technology and innovation"
- Community channel: `#ai-learning-series` on the WCC Slack

## Gotchas

- Don't invent WCC brand facts that aren't in this file, its assets, or the repo it's being used in, if asked something not covered here (exact logo minimum size, an official tagline, brand fonts), say so rather than guessing.
- Don't reuse the 2025 series' peach/tan background style, it was explicitly dropped from the Harness Series in favour of this palette.
- Keep unrelated pastel/Figma-style palettes used for other, non-WCC work separate from this one, don't blend the two.
- This skill is meant to work across any WCC programme or repo, if you're tempted to hardcode Harness-Series-only facts into the shared sections above, put them in that programme's own README instead and just link to it.
