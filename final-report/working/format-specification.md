# NeuroPix report format specification

Latest authority: the user's saved manual revision, visually documented in `user-manual-changes-2026-09-19.md`. Preserve its individual geometry and formatting; do not regenerate it from an older build script.

## Confirmed typography

- Default body font: Calibri
- Default body size: 12 pt
- Headings: Calibri with larger sizes as needed to establish a clear hierarchy
- Heading color: NeuroPix violet (`#6D5DFC`), fully bold, as approved by the user
- Cover title: both lines use the same violet accent, preserving the official cover layout and existing title sizing.
- Figure/table captions: Calibri 9.5 pt, gray `#5F6368`, with concise titles.
- Data-table text: 11 pt throughout; violet header fill with bold white text. Alternate white and `#F7F7FF` body rows, starting with white. Narrative columns are left aligned; compact result/status fields may be centered.
- Reference text: 11 pt, retaining the existing hanging indents and spacing; the bibliography stays on one page.
- Preserve the 18 native bullet paragraphs' saved indentation (text left indent 630 twips / 0.4375 inch) and aligned continuation lines. Preserve the limited emphasis documented in the manual-change record.
- Body paragraphs have no positive first-line indent; use built-in Word lists for suitable enumerations.
- Contents and figure/table list entries: 11 pt, single spacing, 2 pt after. TOC occupies two pages; each figure/table list remains on one page. Verify visual spacing, including pixel measurements if necessary.

## Confirmed pagination

- Data-table cell padding: 4 pt top and bottom, with content-driven row heights. Table 1.1 retains 2.5 pt to keep its subsection and table together. Do not force equal row heights or shrink text to fit.
- User-saved column grids (twips, 1,440 per inch): Table 2.1 = 1615 / 2250 / 2340 / 3011; Table 3.5 = 1255 / 2520 / 5441; Table 4.1 = 2425 / 1170 / 5621; Table 4.2 = 1345 / 3870 / 4001; Table 4.3 = 1728 / 2317 / 5171. Tables 6.2–6.8 retain 1.4 / 5.0 inches. Other grids remain unchanged. Total table width is 6.4 inches.
- Every paragraph using Word's `Heading 1` style starts on a new page.
- Implement this through the style's `page break before` property rather than manually inserting blank paragraphs.
- Avoid orphaned headings and prevent captions from becoming separated from their figures or tables when practical.
- Keep complete data tables on one page where feasible. Assign widths according to the amount of text, avoiding overly wide short-value columns.
- Current measured length is 57 pages. This is a verified result, not permission to reduce font size or weaken evidence to enforce a page limit.
- Use single line spacing in diagram-only paragraphs so the inline image does not inherit extra body-line height. Keep introductions and captions attached. Preserve the user's individual non-destructive crops and displayed dimensions stored in the current Word master for all 20 diagrams. Figures 4.8 and 4.9 are approximately 6.42 and 6.41 inches wide and remain together on physical page 29. Figure 4.2 remains approximately 5.31 inches wide. Do not reset every image to one standard width.
- Section 3.7 starts on physical page 20 with both data dictionaries; this intentional page break preserves grouping without adding a page.

## Final delivery format

- Keep an editable DOCX master for Word comments, automatic contents, captions, and revisions.
- Deliver the final report as a PDF exported directly from the clean DOCX master.
- Do not export intermediate PDFs during routine drafting or revision. Wait until the DOCX content and review cycle are complete and the document is considered submission-ready.
- Before export, update all Word fields, the table of contents, list of figures, list of tables, captions, cross-references, and page numbers.
- Resolve or remove review comments and finalize tracked changes before generating the submission PDF.
- Enable heading bookmarks and document structure tags during export when Word supports them.
- Preserve searchable text and avoid image-only or print-to-image PDF conversion.
- Use Word's Standard or high-quality PDF optimization rather than Minimum size.
- Verify font embedding or correct font substitution, internal navigation, image sharpness, and page count in the exported PDF.

## Visual review rules

### Report document

- During drafting, inspect significant layout changes in the editable Word document and use structural checks for headings, fields, captions, comments, images, and section breaks.
- Do not perform an intermediate PDF export merely to review an ordinary revision.
- Before the one final export, check text clipping, overlap, inconsistent fonts, broken tables, misplaced figures, caption separation, page-number errors, and excessive blank space in Word.
- After the submission-ready export, render and inspect every PDF page separately. Treat the PDF as the final authority for screenshot legibility, font rendering, page breaks, links, and numbering.

### NeuroPix application UI

- Perform a browser-based visual review after significant interface, layout, responsive, or workflow changes.
- Review the affected screens at the intended screenshot viewport and at representative desktop widths.
- Check alignment, spacing, clipping, wrapping, contrast, loading and error states, modal behavior, image scaling, and before-and-after comparison behavior.
- Minor text-only changes do not require a separate UI pass unless they change wrapping, component size, or page flow.

### Screenshot rows throughout the report

- Capture every live-site step at a fixed 1920 x 1080 browser content viewport and 100 percent browser zoom.
- Use one full-width screenshot per row, in chronological order, normally two screenshots vertically on a page.
- Display screenshots at 6.4 inches wide while preserving their aspect ratio.
- Label each screenshot with its use-case ID, panel letter, and a short description so multi-page evidence stays identifiable.
- Keep the shared numbered figure caption with the final screenshot. Keep each individual screenshot and its label together.
- Insert the full-resolution screenshots into Word and resize them only through their displayed dimensions. Use Word's non-destructive crop controls for unused browser chrome and empty margins.
- Enable `Do not compress images in file` and select `High fidelity` for the Word master. Preserve the embedded image's original pixel dimensions.
- Evidence groups may span pages, but no screenshot or attached label may split. Chapter 5 uses three two-panel figures with one full-width screenshot per row; each pair, introduction, and shared caption stays on one page.
- Inspect every screenshot at normal page view for readable controls, prompts, messages, and results.
- Repeat this legibility check on the final exported PDF at normal page view and when zoomed because PDF conversion may resample images or change spacing.

## Template priority

The official cover page remains the authority for the cover layout. The supervisor guideline and sample guide the report structure. These explicit typography and pagination requirements apply to the report body and take precedence when the supplied examples differ.
