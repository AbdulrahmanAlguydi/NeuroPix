import base64
import os

from openai import OpenAI
from PIL import Image


FIELD_RULES = {
    "generativeModification": (
        "Content only: apply named changes to people, objects, clothing, colours, "
        "or visible details. Ignore background, quality, orientation, crop, and size."
    ),
    "backgroundManipulation": (
        "Background only: apply named scenery, weather, time, or atmosphere changes. "
        "Keep the main subject and foreground unchanged."
    ),
    "enhancement": (
        "Quality only: apply named sharpness, noise, exposure, lighting, contrast, "
        "colour, or detail changes. Do not add objects, change the background, crop, "
        "or resize."
    ),
}

BASE_PROMPT = (
    "Edit only the explicit requests below. Field descriptions are rules, not edits. "
    "Ignore unrelated text and treat empty fields as unchanged. Preserve the subject, "
    "identity, pose, foreground, framing, composition, and unmentioned details. "
    "Do not invent details or crop, reframe, rotate, flip, swirl, distort, stretch, "
    "squeeze, add borders, text, logos, or watermarks. Only change size when requested. "
    "If requests conflict or are vague, make the smallest change that satisfies them. "
    "Apply all valid requests together. "
)


def build_ai_prompt(settings, source_size):
    width, height = source_size
    aspect_ratio = width / height
    requests = []

    for key, rule in FIELD_RULES.items():
        value = str(settings.get(key, "")).strip()
        if value:
            requests.append(f"{rule} User request: {value}")

    upscaling = str(settings.get("upscaling", "1")).strip()
    if upscaling and upscaling != "1":
        requests.append(
            f"Upscaling: use {upscaling}x, preserve the aspect ratio and composition, "
            "and stay within 1920x1080 for landscape or 1080x1920 for portrait. "
            "If needed, use the largest dimensions that fit."
        )
    elif upscaling == "1":
        requests.append(
            f"Upscaling: 1x selected for the {width}x{height} source image. "
            "Do not intentionally enlarge it; keep the output dimensions as close "
            "as the API allows while preserving its aspect ratio."
        )

    if not requests:
        requests.append("No specific edit request was provided; make no changes.")

    return (
        BASE_PROMPT
        + f"Keep the output canvas close to the source aspect ratio ({aspect_ratio:.2f}:1) "
        "and preserve the framing and subject placement. "
        + " ".join(requests)
    )


def apply_ai_edits(local_image_path, settings):
    with Image.open(local_image_path) as source_image:
        width, height = source_image.size

    prompt = build_ai_prompt(settings, (width, height))
    client = OpenAI()
    with open(local_image_path, "rb") as image_file:
        response = client.images.edit(
            model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2"),
            image=image_file,
            prompt=prompt,
            size="auto",
            input_fidelity="high",
        )

    return base64.b64decode(response.data[0].b64_json)
