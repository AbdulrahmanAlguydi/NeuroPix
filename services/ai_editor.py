import base64
import os

from openai import OpenAI


def build_ai_prompt(settings):
    prompt_parts = []

    for key, instruction in (
        (
            "generativeModification",
            "Generative modification (content scope): use this field only for explicit changes to people, objects, clothing, colors, or other visible details in the main image. Apply only the content changes named in the user request below. Do not use this field to change the background, technical quality, orientation, crop, or size.",
        ),
        (
            "backgroundManipulation",
            "Background manipulation (environment scope): use this field only for explicit changes to the scenery, weather, time of day, atmosphere, or other background elements. Apply only the background changes named in the user request below. Keep the main subject and foreground intact unless another category explicitly changes them. Do not use this field for content, quality, orientation, crop, or size changes.",
        ),
        (
            "enhancement",
            "Enhancement (quality scope): use this field only for explicit technical changes such as named adjustments to sharpness, noise, exposure, lighting, contrast, color balance, or detail. Apply only the quality adjustments named in the user request below; the examples in this description are not automatic edits. Do not use this field to add or remove objects, change the background, alter orientation, crop, or resize.",
        ),
    ):
        value = str(settings.get(key, "")).strip()
        if value:
            prompt_parts.append(f"{instruction} User request: {value}")

    upscaling = str(settings.get("upscaling", "1")).strip()
    if upscaling and upscaling != "1":
        prompt_parts.append(
            f"Upscaling (size scope): the user selected {upscaling}x. Enlarge the final result by this amount, but never exceed the 1080p limit of 1920x1080 for landscape images or 1080x1920 for portrait images. Preserve the original aspect ratio exactly; if the selected scale would exceed the limit, use the largest dimensions that fit within it. Keep the content, framing, and composition unchanged. Do not crop, stretch, squeeze, reframe, or add unrelated details."
        )

    if not prompt_parts:
        prompt_parts.append(
            "No specific edit request was provided. Preserve the original image and make no changes."
        )

    return (
        "Edit the provided image using only the explicit user requests below. "
        "The category descriptions explain each field's scope; they are rules, not edits. "
        "Apply only the part of each field that belongs to its scope and ignore unrelated text in that field. "
        "An empty field means no change for that category. "
        "Preserve the original subject, identity, pose, foreground, framing, composition, and all unmentioned details unless a matching user request explicitly changes them. "
        "Do not invent objects, styles, backgrounds, lighting, quality improvements, or other details. "
        "Do not crop, reframe, rotate, flip, swirl, distort, stretch, squeeze, add text, logos, or watermarks, or change image size unless explicitly requested by the matching category. Preserve the original aspect ratio. "
        "If a request is vague or conflicts with another request, make the smallest change that satisfies the explicit requests and preserve everything else. "
        "Apply all valid requests together in one coherent, natural result. "
        + " ".join(prompt_parts)
    )


def apply_ai_edits(local_image_path, settings):
    prompt = build_ai_prompt(settings)
    model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2")

    client = OpenAI()
    with open(local_image_path, "rb") as image_file:
        response = client.images.edit(
            model=model,
            image=image_file,
            prompt=prompt,
        )

    image_base64 = response.data[0].b64_json
    return base64.b64decode(image_base64)
