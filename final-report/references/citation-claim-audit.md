# Claim and citation audit

Checked 9 October 2026 against the current report, local project sources, and the linked primary sources. This checks claim support separately from IEEE formatting.

| Reference | Claim supported and evidence | Outcome |
|---|---|---|
| 1 Repository | app.py; services/image_editor.py; services/ai_editor.py; services/image_service.py; utils/security.py; utils/s3.py; local_model/server.py; database schema; README deployment notes; .github/workflows/deploy.yml | Supports current implementation. Added alongside library/service documentation where a sentence describes our actual configuration. |
| 2 SRS | docs/SRS Senior Project.pdf, requirements and initial scope | Historical requirements, not evidence for the newer authenticated/local-SD implementation. Intro now explicitly attributes earlier requirements to it. |
| 3 HLD | docs/HLD Senior Project.pdf, architecture and subsystem sections | Historical design, not evidence for later implementation changes. Intro now explicitly attributes earlier design to it. |
| 4 Pillow | Documentation and Image, ImageEnhance, ImageOps sections support crop, rotation, brightness, contrast, color, sharpness, grayscale and blending | Correct library source; paired with repository for the NeuroPix pipeline. |
| 5 Rombach et al. | CVPR paper supports latent-space diffusion and reduced computational requirements; CVF record confirms authors, year, pages | Narrowed wording to the paper's actual finding rather than assigning the later project's model choice to it. |
| 6 OpenAI | Announcement dated 8 September 2026 describes editing through the Images API and Sunburst | Supports product/API context; repository supports NeuroPix's default identifier and prompt builder. |
| 7 Adobe | Generative AI feature overview describes adding/removing/modifying content and links to selections/layers | Appropriate for the related-system description. |
| 8 Canva | Photo editor guide describes editing within designs, adjustments, AI tools, and downloading; site navigation includes templates/design formats | Appropriate for related-system description. |
| 9 AWS RDS | RDS for MySQL guide describes managed MySQL DB instances | Correct for service capability; added repository citation for project deployment choice. |
| 10 Werkzeug | Security Helpers defines generate_password_hash and check_password_hash | Correct for hashing and verification; added to login's verification claim too. |
| 11 Flask | Quickstart Sessions describes session storage and logout | Correct for session mechanism; repository verifies our keys and access checks. |
| 12 SD model card | Linked model card describes v1-5 checkpoint and Diffusers use; page explicitly identifies itself as an unaffiliated mirror | Supports model identity, not proof of our running service. Paired with repository and corrected publisher attribution to linked organization. |
| 13 Diffusers | StableDiffusionImg2ImgPipeline documentation and parameters | Correct for image-to-image mechanism; repository verifies use and exact parameters. |
| 14 AWS S3 | S3 guide defines object keys and buckets | Former placement implied AWS prescribed our original/processed split. Separated the generic key statement from our project-specific storage layout. |
| 15 NGINX | Reverse Proxy documentation defines proxy_pass and forwarding | Correct for forwarding; repository deployment notes support our DNS/HTTPS/Flask arrangement. |
| 16 Certbot | User guide describes certificate issuance, installation and renewal | Correct for TLS certificate management; repository verifies project deployment. |
| 17 EC2 | EC2 guide defines instances as virtual servers and describes OS images | Correct for virtual hosting; README verifies Amazon Linux used by project. |
| 18 GitHub | Self-hosted runners guide describes user-managed workflow execution | Correct for runner concept, not proof of our exact script. Citation now paired with repository at end of deployment-action sentence. |
| 19 Docker | Windows GPU guide supports NVIDIA GPU access through WSL 2 Linux containers | Correct for capability; project configuration/record supplies actual Windows host usage. |
| 20 OpenBSD | ssh -R documentation describes forwarding remote/server port connections to the local side | Correct for reverse tunnel mechanism; project deployment record supplies actual use. |

All cited passages were reviewed, including repeated repository citations and range citations. No citations occur in table cells. Retained all 20 references and first-use ordering. No application code or diagrams changed. Remaining provenance limitation: physical GPU ownership and live deployment are team-recorded facts, not independently proven by public library documentation; this audit does not claim a new live infrastructure test.
