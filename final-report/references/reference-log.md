# IEEE reference ledger

This ledger records the report's sources. The supervisor's October review requires at least 20 relevant references, each cited in the text. Working IDs remain stable; IEEE numbers follow first appearance.

Internal verification dates below are research records, not report bibliography text. Per the user's decision, omit `[Accessed: ...]` suffixes from the Word references while retaining publication dates and URLs.

Current IEEE numbering after the whole-report review: [1] repository, [2] SRS, [3] HLD, [4] Pillow, [5] latent diffusion paper, [6] OpenAI, [7] Adobe, [8] Canva, [9] AWS RDS. Working source IDs below remain stable and are not bibliography numbers.

| Working ID | Organization or author | Title | Source type | URL or publication | Accessed | Main use | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SRC-01 | NeuroPix project team | NeuroPix source repository | Project repository | `https://github.com/AbdulrahmanAlguydi/NeuroPix` | 2026-09-18 | Current implementation, architecture, tests, and deployment | Yes |
| SRC-02 | NeuroPix project team | Software Requirements Specification | Repository project document | `docs/SRS Senior Project.pdf` | 2026-09-18 | Historical requirements and terminology, checked against code | Yes |
| SRC-03 | NeuroPix project team | High-Level Design | Repository project document | `docs/HLD Senior Project.pdf` | 2026-09-18 | Historical architecture, authorship metadata, and earlier diagrams | Yes |
| SRC-04 | R. Rombach, A. Blattmann, D. Lorenz, P. Esser, and B. Ommer | High-Resolution Image Synthesis with Latent Diffusion Models | Primary research paper | `https://arxiv.org/abs/2112.10752` | 2026-09-18 | Latent-diffusion and Stable Diffusion background | Yes |
| SRC-05 | OpenAI | Introducing ChatGPT Images 2.5 | Official product announcement | `https://openai.com/index/introducing-chatgpt-images-2-5/` | 2026-09-18 | Rationale and current OpenAI image-model context | Yes |
| SRC-06 | Pillow contributors | Pillow documentation | Official library documentation | `https://pillow.readthedocs.io/en/stable/` | 2026-09-18 | Conventional image-processing terminology and implemented operations | Yes |
| SRC-07 | Amazon Web Services | Amazon RDS for MySQL | Official service documentation | `https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_MySQL.html` | 2026-09-18 | Managed MySQL deployment background | Yes |
| SRC-08 | Adobe | Generative AI features in Photoshop | Official product documentation | `https://helpx.adobe.com/photoshop/desktop/generative-ai/generative-ai-features-overview.html` | 2026-09-18 | Adobe Photoshop related-system analysis | Yes |
| SRC-09 | Canva | Edit photos with Canva photo editor | Official product documentation | `https://www.canva.com/en_gb/help/image-editor/` | 2026-09-18 | Canva related-system analysis | Yes |

## October supervisor revision: additional sources

Verified on 9 October 2026. These IEEE entries support specific claims in Sections 5.2–5.6; configuration choices remain attributed to the project repository.

- [10] Pallets, “Security helpers,” Werkzeug documentation. [Online]. Available: https://werkzeug.palletsprojects.com/en/stable/utils/#security-helpers.
- [11] Pallets, “Sessions,” Flask documentation. [Online]. Available: https://flask.palletsprojects.com/en/stable/quickstart/#sessions.
- [12] CompVis and Runway, “Stable Diffusion v1-5 model card,” Hugging Face. [Online]. Available: https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5.
- [13] Hugging Face, “Image-to-image,” Diffusers documentation. [Online]. Available: https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/img2img.
- [14] Amazon Web Services, “What is Amazon S3?” Amazon S3 User Guide. [Online]. Available: https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html.
- [15] F5, “NGINX reverse proxy,” NGINX documentation. [Online]. Available: https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/.
- [16] Electronic Frontier Foundation, “User guide,” Certbot documentation. [Online]. Available: https://eff-certbot.readthedocs.io/en/stable/using.html.
- [17] Amazon Web Services, “What is Amazon EC2?” Amazon EC2 User Guide. [Online]. Available: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html.
- [18] GitHub, “Self-hosted runners,” GitHub Docs. [Online]. Available: https://docs.github.com/en/actions/concepts/runners/self-hosted-runners.
- [19] Docker, “GPU support in Docker Desktop for Windows,” Docker Docs. [Online]. Available: https://docs.docker.com/desktop/features/gpu/.
- [20] OpenBSD, “ssh(1): OpenSSH remote login client,” OpenBSD manual pages. [Online]. Available: https://man.openbsd.org/ssh#R.

## Source rules

Final IEEE check, 9 October 2026: all 20 sources are cited in first-use numerical order. The report's 17 online entries now include Accessed dates using the verification records above (18 September for the original sources, 9 October for the added sources), followed by [Online]. Available: and the URL without a terminal period. The report bibliography is the authoritative formatted list; the older working entries above retain their historical wording.

Claim-level audit, 9 October 2026: read all cited passages and checked each reference against its linked primary source or local project document/code. Separated current implementation from historical SRS/HLD claims, paired general service/library citations with the repository where a sentence describes NeuroPix, narrowed the latent-diffusion claim to the research paper's finding, separated S3 object-key semantics from the project's original/processed storage split, and added the password-verification source to the login claim. Reference [12] now attributes the linked model-card mirror to stable-diffusion-v1-5 rather than implying the organization is CompVis/Runway. All 20 sources remain in first-use order. Details: [citation audit](citation-claim-audit.md). Word/PDF refreshed; visually checked affected PDF pages 10, 13, 26, 34–36 and 58. The report remains 58 pages. No live infrastructure test was performed.

- Retain the 20 cited sources verified for the October supervisor text revision. Add further sources only for specific claims that need support.
- Use the repository, SRS, and HLD for project-specific facts, with the current code taking precedence over older documents.
- Use official documentation and the primary paper only for background or current product facts.
- Do not add separate citations for Namecheap, Camber Cloud, Lightning.ai, the direct-to-main workflow, or every software dependency when the report is describing the team's own experience.
- Record the exact claim supported during drafting and verify each web page again before final submission.
- Convert the working IDs to IEEE numbers in order of first appearance, and remove any source that is not cited.

## Presentation asset notes

The current presentation is `final-report/NeuroPix-Project-Presentation.pptx`; its matching PDF has the same basename. It contains 16 slides. Both replace the dated drafts and alternative decks.

- Project content and original test images come from the final report, repository, and `evidence/use-case-tests/`. The gallery live case includes finding, downloading, and deleting images, as confirmed by the team.
- The cover uses the team's supplied laptop mockup with the NeuroPix homepage and the same gallery cards used on Slide 9. The arrangement takes inspiration from [Product Design Review Feature Deck](https://www.figma.com/community/file/1542584763080422627/product-design-review-feature-deck-presentation-template). The current cover is a custom composition, not the rejected AI-generated mockup.
- Icons use [Lucide](https://lucide.dev/) and provider artwork from [Lobe Icons](https://github.com/lobehub/lobe-icons). These are presentation asset sources, not additions to the report bibliography.
- The current architecture source is `figures/source/presentation-architecture.svg`. It includes the corrected reverse-SSH arrowhead.
- `evidence/presentation/ai-editing-prompts.png` is the browser-rendered screenshot used on Slide 6. Its prompt font was enlarged with temporary browser CSS; application source was not changed for the capture.
- `evidence/presentation/local-sd-upscaled.png` is an AI-upscaled presentation crop of the saved local-model output. It is not a new model test or a recovered high-resolution original. Original test evidence remains unchanged.
- All presentation images are embedded in the PPTX; it has no dependency on the removed build folders or the local archive.
