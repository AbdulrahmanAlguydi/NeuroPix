# NeuroPix report and presentation diagrams

These project-specific preferences come from the user's diagram reviews. Apply
them before drawing or revising diagrams in this directory. Do not use BMAD.
The goal is clarity, readability, and visual continuity—not rigid compliance
with a layout rule. Move nodes, resize containers, or change the aspect ratio
when this improves the result.

## Start from the established design

- Preserve the original diagram's visual language and useful structure. Do not
  replace a clean diagram with a generic redesign or decorative complexity.
- Use Calibri/Arial for human-readable text and Consolas for technical details
  and small stage tags. Match the existing font sizes, weights, and palette.
- Use white backgrounds, restrained grey borders, pale container backgrounds,
  modest rounded corners, and the project's purple accent (#6D5DFC).
- Accent highlights the components or flows relevant to the section. It does
  not automatically mean “AI provider.” Explain its actual meaning in a legend.
- Restore/retain useful small top-left node tags such as INPUT, PREPARE, API,
  OPENAI, LOCAL, and RESULT. Put container titles at the top left.
- Center node body text horizontally and vertically in its available space,
  accounting for the stage tag. Center text inside tags and label backgrounds.
- Keep legends outside the diagram, not floating among nodes or connectors.

## Layout and spacing

- Prefer landscape diagrams for this report, with enough vertical separation
  for larger, readable text. Avoid both extremely wide strips and tall stacks.
- Use compact horizontal flow with vertical branches where helpful. Do not
  make every stage vertical simply to create space for labels.
- Reuse empty space before enlarging the canvas. An input can sit below its
  preparation node, as in the approved Figure 4.6 preview.
- Consider more than one routing/layout approach before choosing. Preserve
  useful grouping and balance rather than spreading nodes arbitrarily.
- Give request and response captions separate clear areas. Increase the
  distance between arrow groups when their captions become crowded.
- Crop excess outer whitespace after arranging the diagram; do not crop away
  labels, arrowheads, or needed breathing room.

## Connectors

- Use straight connectors for aligned nodes and rounded orthogonal bends
  otherwise. Avoid gratuitous detours, loops, crossings, or bridge/hop shapes.
- A simple interaction should look simple. Prefer a direct downward request
  with a horizontal caption beside it over a multi-bend loop solely for a label.
- Extend a useful horizontal segment when a caption needs more space, but
  weigh that against the complexity of the resulting path.
- Show actual request AND response paths when the project sends and receives
  information. Do not invent components or omit exchanges merely to simplify.
- Center a single arrow's attachment on the node edge. Center send/receive
  pairs as a group, using distinct attachment points with comfortable spacing.
- Keep a request/response pair closer together than unrelated arrow groups.
  Multiple groups may be farther apart while remaining balanced on the edge.
- Keep arrowheads consistent and unobstructed. Do not route through unrelated
  nodes, overlap strokes, or hide arrows behind label backgrounds.
- Reroute around a container title rather than moving that title from top left;
  widening the container is another option.

## Wording and arrow labels

- Review ALL diagram text, especially arrow labels, for clarity and accuracy.
  Labels must be direct, specific, and understandable without guessing.
- Name the actual request, data, operation, or response. Avoid vague shorthand
  such as “records / saved” or “data” when more precise wording fits.
- For example, use “Query results / confirmation” for the RDS response,
  “Image data / confirmation” for S3, and “Image + constructed prompt” for
  OpenAI: its full prompt contains more than the base pre-prompt alone.
- Check wording against the implementation. Do not imply unsupported features,
  a direct S3-to-RDS exchange, or guaranteed cleanup when the code does not.
- Prefer horizontal labels when they can be clearly associated with the arrow,
  including beside a vertical segment. Avoid rotated text where a small layout
  adjustment would make horizontal text practical.
- Prefer centering each label over its chosen clear segment. This is a
  preference, not an absolute requirement; clarity takes priority.
- Keep request/response label treatments consistent within a pair. When rotated
  text is necessary, follow the arrow direction: downward reads top to bottom,
  upward reads bottom to top. Never stack individual letters vertically.
- Center text in a tightly sized label background with consistent padding.
  Backgrounds on white canvas should be barely grey (#F8F9FB); inside pale-grey
  containers, use white. Do not make the backgrounds visually heavy.
- Aim for an 8–12 px label-to-stroke gap and about 12 px clearance from nodes,
  bends, container edges, and other labels. Adjust for clarity rather than
  squeezing a label into a rule-compliant but unreadable position.

## Verify before showing or inserting

- Render and inspect the actual output, including zoomed labels, arrow tips,
  node edges, and any crowded areas. Check readability at report placement size.
- Check node/label centering, padding, pair spacing, label associations, crossings,
  overlapping captions, and routes through non-endpoint nodes.
- Compare against the original and the approved reference: it should retain
  their clean, organized feel while explaining the updated content accurately.
- Use SVG/HTML or drawing tools for diagram edits and visual annotations, not
  AI-generated pictures of diagrams or highlighted screenshots.
- Show previews first. Do not insert these previews into Word or replace the
  submitted artifacts until the user approves that step.
- Preserve original files and existing user edits. Do not commit or push unless
  asked. Do not promise a perfect first attempt; use these checks to reduce
  avoidable iterations.

## Current visual references

- Figure 4.6: `figures/source/fig-4-4-ai-prompt-routing.html` and its PNG.
  The user approved its look: input below preparation, a central provider fork,
  four provider stages stacked on the right, simple downward requests with
  horizontal labels, and separate returns to a shared result.
- Figure 4.2: `figures/source/fig-4-1-high-level-architecture.html` and its PNG.
  This routes browser/S3 exchanges through the top and uses tighter right nodes.
- Figure 4.11: `figures/source/fig-4-11-deployment.html` and its PNG.
  It uses narrower local nodes and keeps response captions clear of boundaries.
- These approved versions are inserted in the revised report. Their maintained
  HTML sources and full-resolution PNGs are in `figures/source` and `figures/png`.
- Render directly from vector/HTML sources at 4x, then resize report diagrams
  to 1440 pixels high. Never enlarge a preview bitmap or a downsampled PDF image.
  Disable Word's automatic image compression and preserve lossless PDF images.
  Apply tight non-destructive cropping with a small safety margin around all
  labels, arrowheads, and legends. The selected report uses raster images; the
  SVG and hybrid experiments were discarded. Legend keys use actual line samples.

## Sequence diagram completion markers and self-calls

- Place each non-actor X close beneath that participant's final activation bar,
  not on a shared bottom row. Leave a consistent small gap (current reference:
  15 px from the bar's bottom to the top of the X) and end its lifeline there.
  Do not add an X to the actor. Retain the report's explanation that X denotes
  completion in the illustrated interaction, not shutdown of a running service.
- End the actor's lifeline at the same vertical level as the Browser lifeline's
  endpoint, without adding an actor X. Do not extend it farther down by default.
- Prefer self-call labels to the RIGHT of the loop, vertically centred beside
  it, when that space is available. Do not put them above the loop by default.
- Nested activation bars should overlap their parent bars by half the parent
  width, not float a full bar-width away to the right. Match loop-return
  arrowheads to the nested bar's right edge after adjusting the offset.
- Check branch-condition captions (such as “[Delete confirmed]”) against the
  following message label. Give them a visibly separate row with comfortable
  vertical clearance; add space rather than changing approved wording.
- Keep self-call wording short and direct. Ensure its background does not cover
  the next message caption, the loop itself, a neighbouring activation, or a
  lifeline. Shorten wording or adjust spacing rather than crowding wrapped text.
- This placement is approved for all ten Chapter 4 and Chapter 6 sequences.
- Do not put an X-explanation note beneath individual sequence diagrams. Leave
  that bottom area empty; explain the convention in report prose instead.
- When wording is approved but a label is hard to read visually, preserve that
  wording and add space around its loop and neighbouring message. Check label
  backgrounds too: they must not hide the loop or another label.

## Editable code listings

- Keep code as selectable, editable text, not screenshots. Use a two-column
  table: a narrow line-number column and a wider code column. Restart numbering
  at 1 for each snippet; the numbers refer to the excerpt, not source-file lines.
- Use the code listings in `NeuroPix-Final-Report-Revised.docx` as the visual
  reference. Number-column fill: #E8E3FF; code-column fill: #F7F7FF.
  Use a thin 0.5 pt purple (#6D5DFC) divider BETWEEN the columns only. No outer
  left accent line or other visible borders. Keep square corners.
- Give numbers padding on their right and code padding on its left. Keep the
  number column compact, with a little space to the left of the numbers.
  Current reference: 0.38-inch number column, 5 pt right padding for numbers,
  and 5.5 pt left padding for code; adapt widths to the document if needed.
- Use Consolas, preserve indentation and exact code, and use conventional,
  restrained syntax colours independently of the project's accent palette.
  The approved preview uses 8.5 pt type and 12 pt line spacing. Avoid awkward
  wrapping or clipping; verify the rendered result rather than shrinking blindly.
- Keep the listing caption immediately above and attached to the snippet.
- Keep EACH ENTIRE SNIPPET ON ONE PAGE when it can fit on a full page. If it
  cannot fit in the remaining space, move its caption and whole code block to
  the next page. Do not split it merely to fill the preceding page.
- Split only when a snippet is too large to fit on a full page at readable
  formatting. In that case split at sensible boundaries, keep each logical
  source line together where possible, and continue numbering across pages.
- Include relevant supporting definitions, such as FIELD_RULES alongside
  BASE_PROMPT, rather than explaining them without showing their actual code.
- Selecting only the code column in Word can omit the numbers when copying.
  Do not claim that copying a whole table or from PDF always omits numbers.
