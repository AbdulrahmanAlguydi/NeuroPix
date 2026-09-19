# User's saved Word changes — visual record

Reviewed on 19 September 2026. This records the user's manual edits, not new edits made by the assistant. The Word master and submission PDF were not changed during this review.

## Comparison and authority

- Before: the assistant's immediately preceding table-spacing revision, identified by the hash recorded below.
- After: the saved master `../NeuroPix-Final-Report.docx` and the current submission PDF `../NeuroPix-Final-Report.pdf`.
- Compared verified PDF renders side by side at their original render resolution. Inspected all 37 changed pages; the remaining 20 pages were pixel-identical. Both editions had 57 pages.
- Checked Word's XML to distinguish actual text/style edits from automatic wrapping and image cropping. The temporary comparison renders and machine-readable diff were removed during release cleanup after this durable summary was completed.
- The user's saved master is now the formatting authority. Earlier generation scripts, draft text, and historical QA files must not overwrite it.

## Tables

### Alternating row shading

The body rows now alternate white and very pale violet (`#F7F7FF`), beginning with a white first body row. This is visible in 23 tables. Table 6.1 has only one body row, so it remains white. Violet header fills, bold white header text, and fine gray borders are retained.

### More consistent, larger text

All 24 tables now use 11 pt text. Tables 2.1, 3.2, 3.5, 4.1, 4.2, 4.3, and 6.9 increased from 10.5 to 11 pt; the others were already 11 pt. Some tables are consequently taller. Do not undo this increase to match older page geometry.

### Adjusted column proportions

All five changed tables retain a total width of 6.4 inches. Exact stored widths below are in twips (1,440 twips = 1 inch); rounded inch values are for orientation only.

| Table | Previous widths, twips | User's widths, twips | Current widths, inches | Visible effect |
|---|---|---|---|---|
| 2.1 | 1728 / 2304 / 2304 / 2880 | 1615 / 2250 / 2340 / 3011 | 1.122 / 1.563 / 1.625 / 2.091 | More width for NeuroPix, with smaller adjustments to the other columns. |
| 3.5 | 1512 / 2664 / 5040 | 1255 / 2520 / 5441 | 0.872 / 1.750 / 3.778 | More room for the principal flow; narrower identification and precondition columns. |
| 4.1 | 2880 / 1080 / 5256 | 2425 / 1170 / 5621 | 1.684 / 0.813 / 3.903 | More room for responsibility text and slightly more for methods; narrower route column. |
| 4.2 | 1512 / 3852 / 3852 | 1345 / 3870 / 4001 | 0.934 / 2.688 / 2.778 | Narrower area labels and wider explanatory columns. |
| 4.3 | 1728 / 2088 / 5400 | 1728 / 2317 / 5171 | 1.200 / 1.609 / 3.591 | Wider alternatives column; its heading now fits on one line. |

Other table grids, including Table 6.9 and Tables 6.2–6.8, are unchanged. The existing 4 pt top/bottom cell padding, with the 2.5 pt exception for Table 1.1, predates these manual edits and must not be attributed to this revision. Preserve content-driven heights rather than imposing uniform rows.

## Diagrams and screenshots

All 20 diagrams have non-destructive Word crops and adjusted displayed dimensions. The tighter outer whitespace makes the diagram contents larger and brings their embedded titles closer to the surrounding report text. The original embedded image files are byte-identical to the preceding edition: these are placement/crop edits, not changes to diagram nodes, arrows, labels, or colors.

Affected figures:

- Figure 1.1.
- Figures 3.1 and 3.2.
- Figures 4.1 through 4.11.
- Figures 6.1, 6.3, 6.5, 6.7, 6.9, and 6.11.

Most displayed widths are now approximately 6.41–6.45 inches. Figure 4.2 remains narrower, approximately 5.31 inches, with top/bottom cropping. Figures 4.8 and 4.9 increased from 6.2 inches to approximately 6.42 and 6.41 inches and still share physical PDF page 29. Preserve the crops and dimensions stored in the current Word master rather than applying a blanket width reset.

Screenshot placements, crop settings, and source images are unchanged. The existing one-screenshot-per-row layout remains in place. Caption wording and numbering are unchanged.

## Bullets and selective emphasis

- All 18 existing native bullet paragraphs have revised indentation: text starts at 630 twips (0.4375 inch), and the old style-level hanging indent is removed. First and continuation lines align more cleanly, with more separation between the bullet and its text. The lists remain native Word lists, not typed bullet symbols. Their wording is unchanged.
- The six `Precondition:` labels in Sections 6.4–6.9 are now bold, without bolding the full paragraphs.
- Both `Final status` and `Pass` are bold in the final rows of Tables 6.3–6.8.
- In Section 4.6, the exact phrase `Only the OpenAI` is bold; the following word `path` remains normal weight. Record this as saved rather than silently broadening the emphasis.
- Table 3.3's `Implemented behavior` header was already bold. Its changed run boundaries do not constitute newly added emphasis.

## Small text and line-break adjustments

- Table 3.5: manual breaks separate the UC-T01, UC-T02, UC-T04, UC-T05, and UC-T06 identifiers from their names. UC-T03 already wraps without the same new break.
- Table 4.1: a manual break before `/api/auth/me` helps separate the grouped authentication routes.
- Table 6.1: a manual break separates the test command from the sentence reporting the 28 passing tests.
- Table 6.9: `Automated API/security checks` becomes `Automated API and security checks`, with an explicit break before `security checks`.

No prose paragraph was reworded. The Table 6.9 conjunction is the only wording change found; the other text differences are line breaks. Test outcomes and counts, model names, section order, captions, and reference entries retain their meaning.

## References

All nine references increased from 10.5 to 11 pt. This causes additional wrapping, particularly in reference [2], and makes the block taller while keeping it on one page. Hanging indentation and paragraph spacing were already present and are retained. Word also stores 14 pt paragraph-end formatting on references [6]–[9]; their visible text remains 11 pt. Do not mistake the paragraph-end property for 14 pt reference text.

## Preservation instructions for future work

1. Start from the latest saved Word master, not an earlier generated DOCX or Markdown draft.
2. Make targeted changes only. Preserve the user's crops, drawing sizes, table grids and shading, font sizes, bullets, manual line breaks, and limited bolding.
3. Do not rebuild whole paragraphs, tables, or image runs merely to change a few words: that can discard manual formatting.
4. Keep the current source images at full resolution and retain Word crop metadata. Any later PDF export must account for the saved crop rectangles.
5. Treat 57 pages as the current verified result, not a reason to shrink text. Check affected pages visually after any future layout-impacting edit.
6. Historical draft scripts and notes remain useful evidence but are not instructions to revert the manual changes. No regeneration, re-export, Git staging, commits, or pushes occurred during this documentation review.

## Exact artifact identities

- Before DOCX SHA-256: `f98f09a05c7af1b77d6aabe43e09feb8ad81f776365908060b8b472eefb0d4d2`.
- User-saved DOCX SHA-256: `1222ea5bd397ffe51dad8c32501000174c4cae227b320060c4553055d1fff435`.
- Current PDF SHA-256: `e8873b4725591c7ef2de1b79d779c261d06daa342dbeb54714772e232fcb6716`.

These identify the saved versions reviewed, not any unsaved work currently open in Word.
