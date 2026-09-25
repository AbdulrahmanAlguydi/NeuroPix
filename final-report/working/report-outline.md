# NeuroPix final report expanded outline

This outline is the content specification for the report. It identifies what each section should explain, the implementation evidence to use, and the visuals or tables that should support the discussion.

Current-release overlay: read `report-rules.md`, `format-specification.md`, and `user-manual-changes-2026-09-19.md` first. The outline describes coverage rather than requiring every planning bullet to become separate prose or an extra table. Current Word length is 57 pages.

Finalized revision overlay, 19 September 2026: all 20 approved diagrams are incorporated in the 57-page DOCX/PDF. The prose distinguishes repeated editing of a staged source from reloading a processed gallery result, zero-to-many user/image ownership, registration from session creation, OpenAI-specific request construction from local user text, and Windows tunnel initiation from EC2 request forwarding. The whole-report review also replaces unsupported competitor-learning comparisons with scope comparisons and separates workflow verification from model-quality evaluation. HLD, SRS, SSH, and TLS are included in the abbreviation list. These concise treatments supersede any older planning bullet that would duplicate them.

Visual-selection rule:

- Use a diagram when the reader needs to understand an invisible process, relationship, decision, or data flow.
- Use a screenshot when the visual appearance or an observed interface state is the evidence.
- Use a table for repeated fields or direct comparison.
- Do not repeat the same information as a diagram, screenshot, and table. Cross-reference the strongest existing visual instead.
- Let figures carry structure, connections, and step order. Use the surrounding prose only for rationale, interpretation, limitations, or a fact that is not legible from the figure; do not narrate a figure node by node.

## Front matter

### Official UBT cover page

- Use the supplied Capstone Coverpage as the layout authority.
- Use the full title `NeuroPix: AI-Enhanced Image Processing and Management Web Application`, adjusted only if the official cover has a fixed title treatment.
- List the HLD-verified students exactly: Abdulrahman Alguydi (YB0062), Mohammed Dafterdar (VA0056), and Saud Almansour (VA0040).
- List the supervisor as Dr. Faisal Arafsha.
- Use `2026` as the academic year, with no year range.
- Omit Group 2. Use the website violet `#6D5DFC` on both cover-title lines.
- Preserve the university and college identification shown in the official cover.
- Do not include a page number on the visible cover page.

### Acknowledgments

- Thank the supervisor for academic and technical guidance.
- Acknowledge the university, department, and any people who materially supported the work.
- Keep the section concise and personal.
- Do not invent contributions or use exaggerated language.

### Table of contents

- Generate the table automatically from Word heading styles.
- Include all Heading 1, Heading 2, and appropriate Heading 3 entries.
- Verify page numbers after the final layout pass.

### List of tables

- Generate the list from Word table captions.
- Use the containing section number alone when it has one table, such as Table 2.3. Where a section has multiple tables, add a sequence suffix, as in Table 3.1-1 and Table 3.1-2. Renumber the caption, List of Tables entry, and every in-text reference together.
- Check that every listed table appears in the document and is referenced in the text.

### List of figures

- Generate the list from Word figure captions.
- Include diagrams, application screenshots, database models, and workflow figures.
- Use the containing section number alone when it has one figure, such as Figure 4.2. Where a section has multiple figures, add a sequence suffix, as in Figure 4.10-1 and Figure 4.10-2. Renumber the caption, List of Figures entry, and every in-text reference together.

### Abstract

- Keep the current 73-word abstract, approved during the final text review. This supersedes the earlier approximate 50-word drafting target while preserving a concise, self-contained summary.
- State the image-editing problem addressed by NeuroPix.
- Identify the browser-based purpose and connected editing workflow.
- Summarize the dual editing approach: standard Pillow processing and AI-assisted editing.
- Describe the approach briefly: conventional editing, hosted and local AI, and cloud-backed image management. Leave the detailed technology inventory to the body chapters.
- State the main implemented outcome.
- End with the implemented workflow and its practical benefit. Keep testing statements, exact test counts, timings, and execution conditions in Chapter 6.
- Keep the abstract self-contained and include no citations, unexplained abbreviations, figures, or tables.

### Keywords

- Select four to six terms that directly represent the work.
- Use image processing, AI-assisted image editing, Flask, OpenAI, Stable Diffusion, and web application.
- Final terms must match the wording used in the report.

### List of abbreviations

- Define abbreviations used repeatedly, such as API, AWS, EC2, S3, SQL, UI, and GPU.
- Exclude terms that appear only once or are already clear in context.

## Chapter 1 Introduction

### 1.1 Problem statement and significance

- Establish who experiences the problem, what the problem is, when it occurs in the editing workflow, and where it occurs in the user's browser-based context.
- Describe the observable effect and the gap between the current fragmented workflow and the desired unified workflow without presenting the solution as the problem statement.
- Describe the difficulty of moving between separate tools for conventional adjustments, generative edits, image comparison, downloading, and personal image management.
- Identify the practical user problem: a user needs a single browser-based workspace that supports both predictable manual changes and prompt-based AI changes.
- Explain the usability gap for users who do not want to install or learn a large desktop editing package.
- Explain why before-and-after comparison is useful when assessing standard and AI-generated results.
- Identify the storage and organization problem addressed by the authenticated gallery.
- State concrete, verifiable constraints that shape the problem, including supported formats, image dimensions, processing time, external-service availability, and user privacy. Quantify only what can be supported by the code or collected test evidence.
- Avoid unmeasured claims about market size, productivity, or user demand.
- Write the problem as a statement rather than a research question.

Planned support:

- One compact problem-to-solution diagram showing the fragmented workflow on one side and the unified NeuroPix path on the other. Do not add a second problem-to-capability table that repeats the same mapping.

### 1.2 Proposed solution

- Introduce NeuroPix and summarize the authenticated upload, edit, compare, download, and gallery workflow in one concise paragraph.
- Distinguish Standard editing with Pillow from AI editing through OpenAI or self-hosted Stable Diffusion, including the structured-prompting advantage in one sentence.
- Mention Amazon S3 image storage, MySQL metadata, and the dashboard without repeating the later objectives or deliverables.
- Keep this section at solution level; reserve technical algorithms and code details for Chapters 4 and 5.

### 1.2.1 Aim and objectives

Main aim:

- Design, implement, deploy, and evaluate a web application that combines conventional image processing, AI-assisted editing, visual comparison, and user-specific image management.

Objectives:

- Provide an authenticated browser workflow for uploading and editing supported JPG and PNG images without requiring a desktop editor.
- Provide the implemented Standard controls and purpose-specific AI editing fields, using OpenAI by default and self-hosted Stable Diffusion as the local alternative.
- Store image files in Amazon S3 and account/image metadata in MySQL.
- Support comparison, download, personal gallery management, and re-editing.
- Protect credentials and user-owned records through the implemented hashing, query, session, and ownership controls.
- Verify the principal workflows through a compact automated unit/API-level summary and six live use-case tests.

### 1.2.2 Project deliverables

Use a compact two-column deliverable/evidence table rather than another feature description. Group the rows into deployed application, editing integrations, persistence, deployment and design documentation, and verification and final report. Do not repeat the objectives or workflow details from Sections 1.2 and 1.2.1.

### 1.3 Project domain and intended users

- Define the project domain as web-based digital image processing and AI-assisted image editing.
- Explain the overlap between image manipulation, generative AI, cloud storage, and account-based web applications.
- Describe the primary user as an authenticated account holder seeking straightforward browser-based editing; students, casual creators, and people experimenting with AI edits may be examples without implying completed user research.
- Characterize users by the knowledge actually required: basic browser navigation and no professional image-editing training. Do not invent age, education, or demographic restrictions that the implementation does not impose.
- Describe the operating context briefly and note that the self-hosted provider requires additional server-side hardware and software, not additional setup by the browser user.

### 1.4 Scope and limitations

In scope:

- Account registration and session-based authentication.
- JPG and PNG upload validation.
- Landscape and portrait images within the implemented limits.
- Ten standard editing controls.
- Prompt-based OpenAI image editing.
- Self-hosted Stable Diffusion image-to-image processing.
- Image comparison, download, gallery management, and re-editing.
- Cloud deployment and automated application restart.

Out of scope:

- Layer-based professional editing.
- Video editing, vector graphics, RAW photography formats, and animated images.
- Real-time collaborative editing.
- Social sharing or a public image feed.
- Mobile-native applications.
- Training a new foundation image model.
- Guaranteed preservation of every image detail during generative edits.
- Enterprise-scale performance or availability guarantees that have not been measured.

Technical limitations:

- AI results may vary between requests and may alter unmentioned details.
- The local model can produce larger visual changes or lower detail because it is configured for practical execution on the available hardware.
- OpenAI processing depends on API availability, credentials, latency, model behavior, and account limits.
- The local model depends on Docker, model downloads, and suitable GPU resources.
- Uploads are limited to the supported formats and dimensions enforced by the code.
- The present workflow processes one request synchronously and does not use a background job queue.
- Test and performance claims remain limited to evidence collected during the final verification stage.

### 1.5 Definitions and abbreviations

- Define standard edit, AI edit, prompt, image-to-image generation, upscaling, object storage, metadata, session, and comparison slider.
- Define structured pre-prompting as the server-side addition of field-specific rules, preservation constraints, and source-image context around the user's text before an OpenAI request is sent.
- Define technical abbreviations that recur throughout the report.
- Keep definitions specific to their use in NeuroPix rather than writing general tutorials.

## Chapter 2 Background and related work

### 2.1 Image-editing background

- Distinguish deterministic Pillow controls from probabilistic generative editing in one compact discussion.
- Summarize the browser/server boundary, S3 and RDS separation, and the hosted-versus-self-hosted provider trade-off.
- Connect every concept directly to the implemented project and leave detailed pipelines to Chapter 4.

### 2.2 Related systems

- Keep the complete chapter near one-and-a-half pages of occupied content. This is a short comparison supporting the project, not a full literature review.
- Use exactly two widely used image-editing systems: Adobe Photoshop and Canva. Verify both against their current official product documentation before drafting.
- Give each system one short paragraph covering only the workflow and features needed for comparison with NeuroPix.
- Avoid product history, exhaustive feature inventories, promotional descriptions, or screenshots.

### 2.3 Comparative analysis

Create one compact comparison table whose merged rows cover every comparison category requested by the supervisor without expanding the section:

- Problem addressed and workflow scope.
- Domain and target users.
- Access and design approach, including browser access and installation requirements.
- Outputs and key features, including Standard editing, generative editing, structured prompt guidance, before-and-after comparison, and gallery support.
- Main strength and limitation relevant to the comparison.

The table must distinguish verified facts from unavailable information. A blank or not-documented entry is preferable to guessing.

### 2.4 NeuroPix differentiation

- Summarize how NeuroPix combines standard and generative editing in one student-built system.
- Present simplicity and easy browser access as the main advantages within the project's intended scope.
- Explain that NeuroPix offers a deliberately narrow path from upload to Standard or AI editing, comparison, download, and personal gallery management instead of the much broader professional feature sets of Photoshop and Canva.
- Explain that users do not need to install a desktop editor or learn a complex multi-tool interface for the supported workflow.
- Explain the advantage over using the general OpenAI website as a workflow advantage rather than a model-quality claim: NeuroPix separates the request into content, background, and enhancement fields, adds preservation rules and source-image context automatically, then stores the result for comparison, download, and gallery reuse.
- Avoid claiming that the OpenAI website cannot edit images or that NeuroPix is more powerful. The advantage is the project's focused, repeatable, integrated workflow and reduced prompt-engineering burden.
- Do not add a disclaimer about an unmeasured usability comparison. Avoid unsupported comparative claims without weakening the section with an unnecessary limitation statement.
- Explain the separate standard and AI modes.
- Explain the choice between hosted OpenAI editing and the implemented self-hosted Stable Diffusion service.
- Explain the integrated comparison and gallery reload workflow.
- State that the system is an educational prototype and avoid claiming superiority over commercial products.

## Chapter 3 System analysis

### 3.1 Requirements identification method

- Explain that the final requirements were recovered from the current implementation rather than copied directly from the older SRS.
- Describe inspection of Flask routes, service modules, database schema, frontend JavaScript, deployment workflow, and recent commits.
- Describe visual inspection of the implemented interface and actual workflows.
- Explain how the older SRS and HLD were used as historical references.
- Treat the SRS and HLD as team-created internal planning documents rather than university-mandated deliverables; use them for context without building a formal traceability matrix around them.
- Record discrepancies between planned and implemented behavior.
- State that no survey, interview, or questionnaire will be claimed unless real evidence is supplied.

Planned table:

- Evidence source, purpose, reliability, and how it was used.
- A compact input-processing-output summary for Standard editing and AI editing, satisfying the template's request to define principal inputs and expected outputs without duplicating the detailed design algorithms.

### 3.2 Stakeholders and user characteristics

- Primary user: authenticated person editing and managing personal images.
- Project team: designs, implements, tests, deploys, and documents the system.
- Supervisor and evaluators: review requirements, implementation, evidence, and report quality.
- External service providers: supply AI processing, cloud storage, hosting, and database availability.
- Describe expected user knowledge as basic web navigation rather than professional image-editing expertise.
- Identify user needs for clear feedback, predictable standard controls, visible results, and ownership isolation.

### 3.3 Functional requirements

Keep this section to approximately one page. Present one two-column table with six requirement groups rather than 33 individually numbered requirements:

- Account access: registration, password hashing, login, authenticated sessions, protected pages, and logout.
- Upload and Standard editing: JPG/PNG validation, dimension limits, temporary staging, the ten Standard controls, processing, comparison, and download.
- OpenAI editing: three purpose-specific request fields, structured pre-prompting, output-size calculation, request submission, and decoded PNG output.
- Local Stable Diffusion: availability checking, provider selection, user-prompt forwarding, image-to-image processing, and unavailability handling.
- Persistence: S3 storage of original and processed files plus Amazon RDS for MySQL metadata.
- Dashboard and gallery: counts, recent activity, owned records, comparison, source selection for re-editing, and deletion.

Retain detailed low-level behaviors in the implementation discussion only where they materially explain the system.

### 3.4 Nonfunctional requirements

Keep this section to approximately half a page. Use a four-row table:

- Security: hashed passwords, parameterized SQL, ownership filtering, protected secrets, and HTTPS.
- Usability: clear controls and feedback, consistent navigation, comparison interaction, and browser access.
- Reliability and compatibility: validation, external-service failure handling, retry behavior, and the browser environment actually verified.
- Maintainability and performance: separated modules, environment-based configuration, synchronous-processing limitation, and only measured timings when available.

### 3.5 Use-case model and use-case descriptions

Primary actor:

- Authenticated NeuroPix user

Supporting external actors:

- OpenAI image service
- Self-hosted local model service
- MySQL database
- Amazon S3

Main use cases should match the six cases that are tested:

- Register a new user.
- Log in and access protected pages.
- Upload and process an image in Standard mode, including comparison and download.
- Edit the staged image with OpenAI.
- Edit the staged image with local Stable Diffusion.
- Verify and delete a processed gallery image.

State shared actor and system assumptions once. Present each detailed use case in a compact table containing preconditions, trigger, main flow, combined alternative or failure flow, postcondition, and related requirement group. Place two short descriptions on a page when they remain readable.
Let the diagram carry the use-case names and actor relationships, and let the descriptions carry conditions and flows; do not add a separate narrative that merely relists all six cases.

Planned figure:

- One use-case diagram showing the authenticated user, external services, and the implemented use cases. A screenshot would not communicate system scope or actor relationships as clearly.

### 3.6 Current system workflows

- Introduce the authenticated editing journey and identify Standard editing and AI editing as alternative processing branches.
- Use prose only for an exception, precondition, or limitation that the activity diagram cannot express clearly; do not restate its steps.

Planned visual:

- One activity diagram carrying the end-to-end sequence: authentication, upload, mode and provider choice, processing, comparison or download, gallery access, re-editing, and deletion.

### 3.7 Data requirements and business rules

- Introduce the ownership and metadata model in one short paragraph without listing fields or rules already carried by the tables.

Planned tables and cross-reference:

- Users and Images data dictionaries containing the current field definitions and constraints.
- Business-rule summary table covering uniqueness, password hashing, one-to-many ownership, required and nullable paths, edit-type values, upload time, S3 object-key storage, and ownership checks using both ImageID and UserID.
- Refer forward to the single ER diagram in Section 4.7 instead of duplicating it here.

### 3.8 Software and hardware requirements, constraints, assumptions, and risks

Mandatory software and hardware requirements:

- Use one concise table covering the browser/client, deployed application server, cloud services, development environment, and self-hosted local-model computer.
- Distinguish the continuously deployed web application from the hardware-dependent Stable Diffusion environment.
- Include the software or service, hardware dependency where applicable, purpose, and whether it is required or optional.
- Keep detailed versions and implementation-specific setup in Section 5.1 rather than duplicating them here.

Constraints:

- Supported formats and resolution limits.
- Synchronous request processing.
- External API and cloud-service dependencies.
- Self-hosted local model hardware and Docker requirements.
- Academic project schedule and infrastructure budget.

Assumptions:

- Users provide images they are authorized to process.
- Required services and credentials are correctly configured.
- The browser supports the JavaScript and pointer events used by the interface.

Risks:

- Generative edits can change unintended image details.
- External AI or cloud services may be unavailable, delayed, or costly.
- Public object URLs may present privacy concerns depending on bucket configuration.
- Partial failures between RDS and S3 may leave inconsistent records or objects.
- Synchronous AI processing limits responsiveness and concurrency.

Mitigations and future improvements must be distinguished from behavior already implemented.

## Chapter 4 System design

### 4.1 Architectural approach

- Explain briefly why NeuroPix uses a modular client-server design and keeps processing, credentials, and protected persistence operations on the server.
- Identify the presentation, Flask application, service, persistence, and external-AI layers without cataloguing their components; Section 4.2 carries the topology.
- State the browser's interaction role and the session's security role only where they justify the design boundary.

### 4.2 High-level architecture

- Explain the reasons for separating browser interaction, server-side coordination, metadata, image objects, and AI providers.
- Discuss the main trust boundary and the local-provider availability dependency without narrating every connection shown in the figure.

Planned figure:

- Current high-level architecture diagram derived from the repository, showing the browser and static assets, HTTPS through Nginx to Flask on EC2, application services, Pillow, Amazon RDS for MySQL, Amazon S3, OpenAI, the self-hosted local provider, and non-sensitive trust boundaries.

### 4.3 Frontend design

- Explain the separation between public access and the shared authenticated workspace.
- Discuss the task-oriented movement from dashboard to Studio, result, and gallery, plus the purpose of consistent navigation and responsive behavior.
- Leave the appearance and individual controls to the Section 5.7 screenshots and the JavaScript module responsibilities to Chapter 5.

Planned visual:

- Navigation map showing the landing, about, login, registration, dashboard, Studio, and gallery pages, with the public/authenticated boundary and principal transitions.

### 4.4 Backend and API design

- Group the API responsibilities into public and health access, authentication and session management, upload and processing, local-provider status, download, and owned-gallery operations.
- Explain the shared authentication, validation, response, and error-handling design without repeating each endpoint row in prose.

Planned table:

- API endpoint specification for the current routes (`/`, `/health`, `/api/auth/*`, `/api/local-model/status`, `/api/gallery*`, `/api/upload`, `/api/process`, and `/api/download`) with method, protection, request format, successful response, and main error cases.

### 4.5 Standard editing component

- Explain only why a fixed processing order and preservation of the staged source matter to the user-visible result; the figure carries the operation sequence.
- Keep the explanation at workflow level and leave library-specific mechanics to the code.

Planned figure:

- One detailed processing-order flowchart showing input, RGB conversion, crop, rotation, combined brightness and exposure, contrast, saturation, blur, sharpness, grayscale blending, and JPEG output. Do not add a second component diagram that repeats this flow.
- Approved Figure 4.5 styling: pale violet numbered step badges with left-aligned 16 px numbers, grey arrows, and neutral operation boxes. Preserve the current Word dimensions and crop.

### 4.6 AI editing component

- Explain OpenAI as the default and the local endpoint as an implemented, selectable, availability-checked alternative.
- Explain the usability rationale for structured pre-prompting: short purpose-specific requests become consistent, scoped OpenAI instructions, reducing prompt-engineering effort and unintended changes.
- Contrast this with the local path, which sends only the user's nonempty text, and identify Stable Diffusion v1.5 on the available RTX 3080 as the relevant constraint.
- Mention unsupported-provider and service-unavailability handling briefly; let the figure carry prompt assembly, sizing, and route order.

Planned figure:

- Prompt-assembly and provider-routing diagram. Show the three user fields, OpenAI-only field rules and preservation pre-prompt, aspect-ratio context, output-size calculation, the OpenAI request, and the separate local path that sends only the user's nonempty text. This diagram is more useful than a screenshot because the important behavior occurs inside the backend.

### 4.7 Database design

Explain the Users and Images entities, their one-to-many ownership relationship, the separation between credentials, metadata, and S3 object keys, and the constraints that materially protect data integrity. Do not repeat every column definition already present in the Chapter 3 data dictionaries.

Planned figure and tables:

- ER diagram generated from the current schema.
- Refer back to the Users and Images data dictionaries in Section 3.7 rather than repeating them.

### 4.8 File-storage design

- Explain why temporary staging, S3 file storage, and relational metadata are separated.
- Discuss ownership and lifecycle implications for re-editing, deletion, and cross-service partial failures without narrating the storage path.

Planned figure:

- One storage-flow diagram showing the staged local file, UUID-based names, S3 `inputs` and `outputs` keys, the related Images row, and the re-edit and deletion paths. Keep the figure here and cross-reference it from Section 5.5.

### 4.9 Security design

- Summarize the implemented controls in a compact table: password hashing, session-protected routes, server-side upload validation, parameterized SQL, ownership filtering, environment-based secrets, and HTTPS.
- Discuss only the most relevant remaining limitations: CSRF and cookie hardening, object-access policy, rate limiting, and production logging.
- Avoid explaining routine validation checks individually when they are already covered by the requirements or tests.

### 4.10 Sequence diagrams

Use four consolidated design-level sequences that match current routes and modules:

- Authentication sequence with registration and login alternatives.
- Upload, temporary staging, Standard processing, S3 persistence, and database logging sequence.
- AI-processing sequence with OpenAI and self-hosted local-provider alternatives.
- Gallery sequence covering retrieval, comparison data, reload for re-editing, and deletion.

Each diagram must use the current `/api/process` route rather than the outdated separate editing endpoints.
These are detailed design diagrams. The six Chapter 6 diagrams remain compact test-specific sequences tied to visible steps and assertions, rather than copies of the design diagrams.
Introduce each diagram with its scope and follow it with at most one design observation; do not restate the messages step by step in prose.

### 4.11 Deployment design

- Explain the rationale for the AWS-hosted web tier, separate managed data services, HTTPS boundary, and automated deployment at a high level.
- Explain the reverse SSH tunnel only as the deployment consequence of keeping Stable Diffusion on the RTX 3080 computer, including its availability limitation.
- Do not repeat the diagram's service-by-service topology or deployment command sequence in prose.

Planned figure:

- Production deployment diagram with network and service boundaries, Namecheap-managed DNS, HTTPS termination through Nginx and Certbot, EC2 application services, OpenAI, Amazon RDS for MySQL, S3, and the reverse SSH path to the RTX 3080 computer.
- Label the reverse SSH connection and request direction clearly, but omit public IP addresses, private keys, security-group identifiers, and other sensitive configuration.

### 4.12 Development choices and cost considerations

Keep this discussion between one and one-and-a-quarter pages. Use one compact table with decision, alternatives considered, primary reason, and trade-off. Its rows should cover AWS hosting, Namecheap rather than paid Route 53 registration, OpenAI as the default provider, local Stable Diffusion rather than Camber Cloud or Lightning.ai for sustained experimentation, and direct work on `main` rather than a branching workflow.

Follow the table with only three short interpretive paragraphs:

- Cost and learning strategy: explain the search for student offers, free tiers, existing hardware, and widely supported services; Namecheap's student offer avoided an uncovered Route 53 registration charge, while AWS provided extensive resources and transferable deployment experience. Do not claim universal price or technical superiority.
- AI providers: explain OpenAI's documented API, ease of integration, popularity, and newly released image-editing model; then explain that the RTX 3080 constrained the local model choice to the mature Stable Diffusion v1.5 path. Camber Cloud and Lightning.ai consumed free credits while GPU instances remained active and added operational friction, whereas local execution avoided recurring runtime charges and allowed repeated tuning. Acknowledge availability, speed, and quality trade-offs, and describe the cloud services only as evaluated.
- Version control: explain that working on `main` kept Git understandable for teammates without prior Git or GitHub experience, while sacrificing branch isolation and formal review and making careful local checks important because pushes trigger deployment.

Do not repeat every table cell in the paragraphs. Keep the reverse SSH mechanism out of this decision section; Section 4.11 documents it as a deployment consequence of the local-model choice.

## Chapter 5 Implementation

### 5.1 Implementation environment and technology stack

Keep this section under one page by combining the hardware, software, and technology-stack material.

- Refer to the mandatory software/hardware requirements table in Section 3.8 instead of reproducing it.
- Use one compact implementation-stack table for the actual client, deployed server, cloud services, self-hosted local-model computer, and material technologies: Python and Flask, Pillow, Amazon RDS for MySQL, Amazon S3 and boto3, OpenAI, Docker and Diffusers with Stable Diffusion, Nginx and systemd, and GitHub Actions.
- Mention verified versions only when they affect reproducibility or compatibility.
- Briefly identify required external accounts or API access without cataloguing routine dependencies, HTML/CSS/JavaScript, or license details that do not affect the project.

### 5.2 Frontend and authentication implementation

- Summarize how the vanilla HTML/CSS/JavaScript frontend separates public and authenticated pages, coordinates page state, and communicates with the API.
- Let the Section 5.7 screenshots show the upload preview, editing controls, loading feedback, comparison interface, and gallery appearance instead of listing those visible elements again in prose.
- Mention caching or duplicate-request prevention only if it materially affects an observed workflow or test result.
- Describe significant UI improvements identified during visual review without explaining ordinary DOM operations.
- Summarize the authentication flow from registration validation and password hashing through login, session-protected pages, and logout.
- Mention duplicate usernames and generic login errors as security behavior, but do not describe every request field, session value, redirect, or endpoint again.

Evidence:

- Relevant HTML, CSS, and JavaScript files.
- Verified screenshots and interaction results.

### 5.3 Upload and Standard image-processing implementation

- Describe upload through drag-and-drop or file selection, the complementary browser/server validation, temporary staging, and the distinction between a staged upload and a saved gallery record.
- Explain that the ten controls are submitted to the shared processing route and applied in the fixed order shown in Section 4.5.
- State that Standard output is normalized to JPEG and that successful original and processed files are persisted with their metadata.
- Omit routine temporary-file-cleanup discussion, as requested; distinguish temporary staging from persistence without claiming that the code lacks cleanup.
- Discuss an edge case only if it appears in testing or materially changes the visible result.

Visual choice:

- Use the Section 4.5 processing-order diagram for the internal algorithm and the curated Section 5.7 interface figures for the controls. Refer to UC-T03 for step-by-step live evidence instead of repeating another screenshot pair here.

### 5.4 AI editing implementation

- Confirm that the implementation follows the provider and structured-prompt design in Section 4.6 without restating its field rules or assembly sequence.
- Focus on the implementation boundary: source-image preparation, provider invocation, result persistence, and safe failure handling.
- Keep the general-OpenAI-workflow advantage in Section 2.4 and the design rationale in Section 4.6 rather than repeating it here.
- Name the configured OpenAI default `gpt-image-2.5-sunburst`, noting that configuration can override it.

Visual choice:

- Use the Section 4.6 prompt-assembly diagram for backend behavior and the curated Section 5.7 AI-controls and comparison screenshots for appearance. Refer to UC-T04 for live execution evidence.

- Identify the Stable Diffusion v1.5 image-to-image pipeline.
- Explain that the available RTX 3080 and the goal of avoiding recurring cloud-GPU cost influenced the Stable Diffusion choice.
- Describe the Dockerized local path as an implemented, selectable, availability-dependent provider, not an unimplemented optional feature.

### 5.5 Persistence, dashboard, and gallery implementation

- Focus on the implementation controls that are not already visible in the storage-flow diagram: parameterized queries, ownership checks, success-state coordination, and the current partial-failure limitation.

Visual choice:

- Refer to the storage-flow diagram in Section 4.8. Do not repeat it in the implementation chapter.

Dashboard:

- Explain how owned records are summarized into edit counts and recent activity; mention cached data only if it materially affects observed behavior.

Gallery:

- Explain owned-record retrieval and the behaviors behind comparison, source selection for re-editing, deletion, and state refresh.
- Let Section 5.7 show card contents, thumbnails, labels, dates, dialogs, and empty or error states rather than inventorying them in prose.

### 5.6 Deployment and continuous delivery

- Refer to the Section 4.11 deployment diagram for topology, HTTPS, CI/CD, and the reverse SSH path.
- Describe only the implemented operational behavior: systemd service management, deployment health checking, and the local provider's environment-dependent availability.
- Keep credentials and private infrastructure values out of the report; omit routine local-installation instructions.

### 5.7 Input and output screens

For every screenshot, use a brief purpose-driven caption that identifies what the reader should notice. Do not add a paragraph that inventories controls or text already visible in the figure.

Use three two-panel figures, each with its screenshots stacked in full-width rows on one page:

- Access and workspace: landing page, registration or login, dashboard, and empty Studio.
- Editing interface: valid upload preview, Standard controls, AI fields and provider selector, and processing state.
- Results and management: processed-result comparison, populated gallery, and re-edit or deletion state.

Label the two panels `(a)` and `(b)` with short descriptions. The shared Figure caption below the pair supplies the figure number; do not repeat an old figure number in each panel label.

Add a validation-error or responsive screenshot only if it demonstrates a distinct interface behavior not already visible in Chapter 6. Do not repeat all live-test screenshots here; these figures document the interface structure, while Chapter 6 screenshots document executed steps and observed results.

Screenshot rules:

- Capture at the fixed 1920 x 1080 browser content viewport and 100 percent zoom.
- Use controlled demonstration data.
- Hide credentials, keys, private URLs, and unrelated personal data.
- Review the UI visually before capture.
- Do not add screenshots that repeat the same information.

## Chapter 6 Testing

### 6.1 Testing objectives and strategy

- Keep live use-case testing as the primary method, following the supervisor's specific direction, and include a very small supporting unit-testing summary.
- Present the six cases as functional acceptance tests derived from the implemented requirements and main user workflows.
- Execute the six principal use-case tests against `https://neuropix.me` in Google Chrome whenever the required services are available.
- Use the connected Chrome extension to control the real Chrome session. Prefer its semantic Playwright locators for reliable interaction and its native screenshot capture for evidence; use a separate Playwright browser only as a documented fallback if the extension becomes unavailable.
- Reuse controlled state between the six live tests through explicit preconditions so login, upload, and setup steps are not repeated unnecessarily.
- Keep every test logically reproducible by stating the exact preconditions and test data it requires.
- State the implemented functionality covered by each use case without adding a separate traceability matrix.
- Do not claim exhaustive verification of every low-level requirement; describe the six tests as evidence for the principal user workflows selected by the supervisor.
- Report only results that were actually executed and recorded.

Test-plan coverage across Sections 6.1–6.3, case preconditions, and Section 6.10 (no duplicate standalone table):

- Test approach: a brief automated unit/API-level check followed by six use cases treated as combined functional and acceptance testing.
- Scope and features tested: registration, login/protected access, Standard editing, OpenAI editing, self-hosted Stable Diffusion editing, and gallery verification/deletion.
- Features excluded or deferred, consolidated in Section 6.10.
- Test environment and controlled data, with details in Section 6.2.
- Test schedule recorded as the actual execution date or date range rather than an invented schedule.
- Testing tasks and responsibility: preparation, execution, screenshot capture, result recording, defect review, and cleanup.
- Entry and completion conditions, including required service availability and evidence captured for each case.

The live use cases remain the focus of the chapter. The unit-testing material below must not displace their diagrams, screenshots, or discussion.

#### Automated summary within Section 6.1

Keep this subsection to approximately one third to one half of a page.

- Describe the repository's automated tests as unit and API-level tests because `tests/test_api.py` uses Flask's test client and mocks external database, storage, and AI boundaries, while `tests/test_security.py` checks password-security behavior.
- Run only `python -m pytest -q tests/test_api.py tests/test_security.py` for the reported unit-test result.
- Preserve the recorded execution: 28 tests passed in 3.97 seconds on 18 September 2026. Editorial reviews do not constitute new executions.
- Use one compact aggregate result row with the command and outcome. Brief surrounding prose explains scope and mocked boundaries; do not add a file-by-file test inventory.
- Cover health, registration and authentication validation, session behavior, upload validation, Standard and AI processing paths, local-provider prompt handling, save failures, mocked persistence orchestration, repeated object-key generation, and password hashing where the tests actually assert them.
- Do not reproduce individual test cases, terminal screenshots, or code excerpts.
- Do not add a sequence diagram for unit tests.
- Keep the real RDS, S3, and workflow scripts under `tests/integration/` out of this small subsection; the live use-case evidence remains the report's main integration and acceptance evidence.

### 6.2 Test environment

- Record the live website URL, test date, Google Chrome version, Windows version, and the fixed 1920 x 1080 browser content viewport used for the screenshots.
- Use a dedicated demonstration account and controlled, non-sensitive JPG or PNG test images.
- Record whether OpenAI and the self-hosted Stable Diffusion service were available during execution.
- For the local-provider test, record the RTX 3080, Docker service, network connection, and reverse SSH tunnel as environment dependencies.
- Record how the test-created database rows and S3 objects are retained for evidence or removed after testing.
- Exclude all secret values.
- If the live deployment or a required external service is unavailable, record the test as blocked. A local fallback may be reported separately but must not be presented as a live pass.

### 6.3 Live use-case test method

Run the six tests as one controlled acceptance-test scenario while retaining a separate objective, expected result, and status for each test.

Each test subsection must include:

1. Test ID and covered functionality.
2. Objective.
3. Preconditions and reused state from earlier tests.
4. Controlled test data.
5. Numbered user actions.
6. Expected and actual result for each action.
7. Final pass, fail, blocked, or not-run status.
8. One compact sequence diagram reflecting the live implementation.
9. A labeled Chrome screenshot after every numbered, user-visible step.
10. Defects, observations, and evidence-file references.

Keep the detailed six test reports in Chapter 6 because the supervisor specifically requested the sequence and screenshots for each use-case test. Do not create an appendix for API explanations, source code, or testing evidence.
Use the test table for action, expected result, and actual result; use the sequence diagram for actor and system interactions; and use screenshot rows for observed interface state. Do not add a prose retelling of the same steps after these three forms of evidence.
Use the same layout for all six cases: preconditions and a compact sequence diagram, an execution-results table, then chronological full-width screenshot rows. Treat a test step as a meaningful user action that produces a distinct visible state, not every click or field focus. Keep each test heading and introduction with its sequence diagram. The approved larger evidence layout supersedes the earlier one-page and one-and-a-half-page test budgets.

Screenshot protocol:

- The assistant will execute the tests and capture the screenshots directly from Google Chrome.
- Use the connected Chrome extension with semantic Playwright locators inside the real Chrome tab, then save screenshots directly from that same tab.
- Keep the Chrome content viewport fixed at 1920 x 1080 and browser zoom at 100 percent throughout the suite, independently of the physical 2K monitor resolution, then reset any temporary viewport override after testing.
- Save a full raw screenshot after every numbered visible step and insert the full-resolution image into the DOCX. Resize it only through Word's displayed dimensions; do not downsample it before insertion.
- Use the established test-folder and numbered-filename pattern, such as `final-report/evidence/use-case-tests/UC-T03/01-city-skyline-uploaded.png`.
- Store raw and report-ready evidence under `final-report/evidence/use-case-tests/<test-id>/`.
- Use concise captions that identify the test ID, step number, and observed result without reproducing the full action or table entry.
- Mask credentials and exclude browser notifications, unrelated tabs, personal bookmarks, private URLs, keys, and other sensitive information.
- Review each screenshot for clipping, overlap, broken layout, unexpected messages, and inconsistent state before accepting it as evidence.
- Arrange all screenshots one per full-width row at 6.4 inches wide, preserving aspect ratio. Two screenshots normally fit vertically on a page. Keep each Chapter 5 pair with its introduction and caption on one page.
- Label panels with the use-case ID, `(a)` through `(d)`, and a short step description. Keep the shared numbered figure caption with the final panel.
- Use Word's non-destructive crop controls to hide unused browser chrome and empty margins while preserving the embedded image's original pixels. If permanent redaction is necessary, create a full-resolution redacted copy without resampling.
- Check controls, prompts, messages, and results at normal page view and when zoomed.
- Keep rows in chronological top-to-bottom order. Evidence groups may span pages, but each screenshot must stay with its step label.

### 6.4 UC-T01: Register a new user

Purpose:

- Verify that a new user can submit valid registration data and reach the login page.

State and evidence:

- Create the dedicated account used by the remaining live tests.
- Capture the registration page with non-sensitive demonstration values and the resulting login page or success state.
- Sequence the user, Chrome interface, Flask registration route, password hashing, and MySQL user record.

### 6.5 UC-T02: Log in and access protected pages

Precondition:

- The dedicated account exists from UC-T01.

Purpose and evidence:

- Verify login, session creation, dashboard access, displayed username, and access to the authenticated Studio.
- Do not repeat registration.
- Capture the completed login form with the password obscured, the authenticated dashboard, and the protected Studio state.
- Sequence the user, Chrome interface, Flask login route, MySQL user lookup, session, and protected-page request.

### 6.6 UC-T03: Upload and process an image in Standard mode

Preconditions:

- The user remains authenticated from UC-T02.
- Use `final-report/evidence/test-assets/neuropix-test-city-skyline.png`, copied from the existing repository city-lights asset. It is a 1920 x 1080 PNG below the five-megabyte client limit.

Purpose and evidence:

- Document the verified upload, browser preview, Standard-mode configuration, processing, result presentation, and comparison. Download is implemented but was not covered by a separate live case; do not extend the executed coverage claim.
- Use the executed settings: crop 90% × 85%, rotation 90°, brightness 115%, contrast 160%, and grayscale 100%. Do not add unexecuted sharpness changes.
- Retain the staged original for the two subsequent AI-provider tests.
- Capture each distinct visible state without repeating the login steps.
- Sequence Chrome, `/api/upload`, temporary staging, `/api/process`, Pillow, S3, MySQL, result URLs, and comparison. Keep the session as a precondition rather than repeating login.

### 6.7 UC-T04: Edit the staged image using OpenAI

Preconditions:

- The user is authenticated and the valid source image from UC-T03 remains staged.
- OpenAI credentials, account access, and internet connectivity are available.

Purpose and evidence:

- Verify AI-mode selection, OpenAI-provider selection, prompt entry, processing state, generated result, and original-versus-result comparison.
- Use the executed dramatic futuristic-city prompt shown in `final-report/evidence/use-case-tests/UC-T04/01-structured-openai-prompts.png` so the visual change is obvious.
- Do not repeat login or upload.
- Limit execution to the required generation request and avoid duplicate paid requests.
- Sequence Chrome, Flask, prompt construction, the OpenAI image service, S3, MySQL, and the returned result.

### 6.8 UC-T05: Edit the staged image using local Stable Diffusion

Preconditions:

- The user is authenticated and the valid source image from UC-T03 remains staged.
- The RTX 3080 computer, Dockerized Stable Diffusion service, network connection, and reverse SSH tunnel are active.

Purpose and evidence:

- Verify local-provider availability, prompt entry, processing state, generated result, and original-versus-result comparison.
- Use the same futuristic-city prompt as UC-T04 so both providers receive the same source and intended transformation.
- Do not repeat login or upload.
- If any local dependency is unavailable, record the test as blocked rather than substituting an unsupported pass.
- Sequence Chrome, Flask, the EC2 loopback endpoint, reverse SSH forwarding, the local Docker service, S3, MySQL, and the returned result.

### 6.9 UC-T06: Verify and delete a processed gallery image

Preconditions:

- The user remains authenticated.
- Gallery records produced by UC-T03, UC-T04, and UC-T05 are available, except for any correctly documented blocked provider test.

Purpose and evidence:

- Open the live gallery and verify that a processed image created by an earlier test is present with the expected thumbnail and edit-type label.
- Delete the selected test image and verify that it is removed from the visible gallery.
- Use the existing records instead of creating additional processed images.
- Limit the test evidence to the gallery before deletion, the deletion action or confirmation, and the gallery after deletion.
- Sequence Chrome, gallery retrieval, the ownership-filtered MySQL query, the delete API, the database record, the related S3 objects, and the updated gallery response.
- Cover comparison, re-editing, and other gallery interface states in the report's normal application screenshots rather than duplicating them in this use-case test.

### 6.10 Consolidated results and discussion

- Use the compact Test / Scope / Result summary table. Keep detailed actions and outcomes in their individual cases instead of repeating them in an oversized matrix.
- Summarize passed, failed, blocked, and not-run live tests.
- Discuss defects discovered and corrected, remaining failures, and environment-dependent behavior.
- Include measured timings only when a repeatable timing method is used.

#### Known gaps within Section 6.10

- List untested browsers, mobile layouts, infrastructure failures, concurrency conditions, and other excluded cases.
- Identify use cases blocked by credentials, external services, hardware, or tunnel availability.
- Explain whether each gap affects core functionality, optional functionality, or future scalability.
- Do not hide failures or convert blocked tests into passes.

## Chapter 7 Conclusion

Keep the complete conclusion on its current one page; do not expand it to fill the earlier one-and-a-half-page allowance.

### 7.1 Summary and evaluation

- Summarize achievement of the aim in one concise paragraph, keeping implemented scope distinct from tested evidence.
- Omit the proposed objective-status table because it would duplicate the objectives and Chapter 6 results.
- Refer to the live and automated evidence without repeating its tally or individual cases.

### 7.2 Strengths, limitations, and lessons learned

- Strengths: simple browser access, focused Standard/AI workflow, structured OpenAI pre-prompting, comparison, personal gallery, cloud storage, and self-hosted local AI.
- Limitations: generative variability, RTX 3080 and tunnel dependence for local AI, synchronous processing, non-transactional cross-service failures, security hardening, and limited formats.
- Lessons: separating browser and server responsibilities, coordinating RDS metadata with S3 files, controlling AI prompts, and adapting internal SRS/HLD plans to the final implementation.
- Keep each part to one short paragraph grounded in actual implementation or testing evidence.

### 7.3 Future work

Frame this as the work the team would prioritize with another six months. Keep the five existing actions, ordered as recovery, branches/review/staging, background processing, local prompting, and evaluation. Briefly explain that reliability and safer deployment come first. Preserve the approved recovery wording and do not invent delivery dates.

### 7.4 Final conclusion

Keep the existing concise closing paragraph focused on the implemented system and the constraints under which it was delivered. Do not repeat the future-work priorities from Section 7.3, add a second results table, or repeat test counts.

## References

- Use IEEE numerical citations in order of first appearance.
- Begin with the NeuroPix GitHub repository, SRS, and HLD as the three project references.
- Add only sources needed for claims that the repository, SRS, and HLD cannot support.
- Use a minimal external set: the Stable Diffusion or latent-diffusion primary source, official OpenAI image-model documentation, Pillow documentation, official Amazon RDS for MySQL documentation, and one official source for each selected related system.
- Do not add separate references for Namecheap, Camber, Lightning.ai, or every software dependency when the report is only describing the team's own development experience or implemented configuration.
- Prefer official documentation and original research papers for the small external set.
- Record authors or organizations, title, publication, date, URL, and access date.
- Verify every URL immediately before finalization.
- Do not cite search-result pages or unsupported AI summaries.

## Appendix policy

- Do not include an appendix in the planned report.
- Keep API explanations in Sections 4.4 and 5.2-5.5 at the level necessary to understand the design and implementation; a separate API reference is unnecessary.
- Keep all six use-case reports, sequence diagrams, and screenshot rows in Chapter 6.
- Retain the original full-resolution screenshots in the local evidence folder and embed those full-resolution files in the DOCX rather than creating an appendix.
- Add an appendix only if the supervisor later requests a specific supporting item.

## Cross-document quality requirements

- Maintain an editable DOCX master for drafting, comments, automatic fields, captions, and revision history; deliver the final report as PDF.
- Use Calibri 12 pt as the default body font.
- Use Calibri headings with a clear size hierarchy unless an official cover element must be preserved.
- Configure Word Heading 1 with `page break before`.
- Use automatic numbering, captions, cross-references, and contents fields where practical.
- Start every Heading 1 section on a new page.
- Keep figures and captions together when possible.
- Number tables and figures by chapter.
- Refer to every table and figure in the body text.
- Use actual test results and verified screenshots.
- Run the Humanizer review after substantive drafting.
- During drafting and revision, keep work in DOCX and use Word comments, structural checks, and targeted in-document review. Do not export an intermediate PDF after each revision.
- Before PDF export, accept or reject tracked changes as intended, remove or resolve comments, update the table of contents and all caption lists/cross-references, and verify the page numbering.
- Disable image compression for the Word master and use High fidelity as the default image resolution so full-resolution screenshots remain available when readers zoom.
- Export the PDF only after the content and Word revision cycle are complete and the report is considered submission-ready. Export directly from the clean Word master using Standard or high-quality output, with document structure tags and heading bookmarks when supported. Do not create the submission PDF by printing pages to images.
- Verify that the final PDF has searchable text, working internal navigation where exported, embedded or correctly substituted fonts, sharp diagrams, and readable screenshot rows.
- Render every page of the exported PDF to images and inspect it independently from the DOCX. The PDF, rather than the Word rendering, is the final layout authority.
- Perform browser-based visual review after significant UI changes, but not after minor text-only changes unless they affect layout.
