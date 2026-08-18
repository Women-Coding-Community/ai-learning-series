---
name: accessibility-report
description: Audits a URL for accessibility (a11y) issues against the WCAG 2.2 standard using Chrome and Lighthouse. It returns a scored report, writes the findings as both Markdown (accessibility_report.md) and interactive HTML (accessibility_report.html) reports, and automatically creates GitHub issues for any critical failures in the GitHub repository. Make sure to use this skill whenever the user requests an accessibility audit, a11y check, WCAG 2.2 audit, or Lighthouse analysis on any website or webpage.
---

# accessibility-report

Audits a URL for accessibility issues against WCAG 2.2 standards, generating Markdown/HTML reports and filing GitHub issues for critical failures.

## When to use this

Use this skill when the user asks to check, audit, test, or evaluate the accessibility of a webpage or run a WCAG 2.2 audit/Lighthouse report on any URL.

## Steps

1. Call the `new_page` tool from `chrome-devtools-mcp` with the target `url` to open the webpage in Chrome.
2. Wait for the page load to complete.
3. Call the `lighthouse_audit` tool from `chrome-devtools-mcp` with `device: "desktop"` and `mode: "navigation"`.
4. Parse the audit results. Retrieve the overall accessibility score, failing audits, and warning audits.
5. Map each failed audit to the corresponding WCAG 2.2 Success Criteria (e.g., Success Criterion 1.1.1 Non-text Content, Success Criterion 1.3.1 Info and Relationships, Success Criterion 2.4.4 Link Purpose).
6. Generate two files in the workspace directory:
   - **`accessibility_report.md`**: A clean, structured Markdown report showing the overall score, the top 3 most critical fixes first, and a breakdown of other findings sorted by WCAG 2.2 Criteria and severity.
   - **`accessibility_report.html`**: A visually stunning, responsive HTML report featuring:
     - Styled using the `wcc-branding` skill (`.agents/skills/wcc-branding/`): WCC's official colour palette for the layout, score badges and accents, and the WCC logo (`wcc-branding/assets/WCC_LogoBlack.png`) in the header, rather than a generic palette. Fall back to a clean modern default only if `wcc-branding` isn't available.
     - Clean CSS layout showing the Accessibility Score at the top.
     - Section for the "Top 3 Critical Fixes" highlighted with a distinct colour from the WCC palette.
     - Collapsible detail views for all other findings.
7. Identify any critical (Level A) failures. For each critical failure, file a GitHub issue using the `issue_write` tool from `github-mcp-server` with:
   - `method`: `"create"`
   - `owner`: `"Women-Coding-Community"`
   - `repo`: `"ai-learning-series"`
   - `title`: A descriptive title such as `[A11Y] Fix <Issue Title> - <domain>`
   - `body`: A clear description of the failing elements, the corresponding WCAG 2.2 Success Criterion, and the required remedy.
   - `labels`: `["bug", "accessibility"]`
8. Call `close_page` from `chrome-devtools-mcp` to close the page.

## Inputs it needs

- `url`: The absolute URL of the webpage to audit.

## Output

- A formatted markdown accessibility report starting with the score and top-3 fixes first.
- GitHub issues created for any critical accessibility failures.

