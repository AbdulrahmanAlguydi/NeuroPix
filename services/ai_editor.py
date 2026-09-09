import base64
import os

import requests
from openai import OpenAI
from PIL import Image


FIELD_RULES = {
    # Each field limits the part of the picture that its text is allowed to change.
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
    # Shared instructions keep unrelated text from changing other image properties.
    "Edit only the explicit requests below. Field descriptions are rules, not edits. "
    "Ignore unrelated text and treat empty fields as unchanged. Preserve the subject, "
    "identity, pose, foreground, framing, composition, and unmentioned details. "
    "Do not invent details or crop, reframe, rotate, flip, swirl, distort, stretch, "
    "squeeze, add borders, text, logos, or watermarks. Only change size when requested. "
    "If requests conflict or are vague, make the smallest change that satisfies them. "
    "Apply all valid requests together. "
)


def build_ai_prompt(settings, source_size):
    # Include the source ratio because the API chooses the final pixel dimensions.
    width, height = source_size
    aspect_ratio = width / height
    requests = []

    for key, rule in FIELD_RULES.items():
        # Empty fields are skipped so they do not add accidental instructions.
        value = str(settings.get(key, "")).strip()
        if value:
            requests.append(f"{rule} User request: {value}")

    upscaling = str(settings.get("upscaling", "1")).strip()
    if upscaling == "1":
        requests.append(
            f"Upscaling: 1x selected for the {width}x{height} source image. "
            "Do not intentionally enlarge it; keep the output dimensions as close "
            "as the API allows while preserving its aspect ratio."
        )
    elif upscaling:
        requests.append(
            f"Upscaling: use {upscaling}x, preserve the aspect ratio and composition, "
            "and stay within 1920x1080 for landscape or 1080x1920 for portrait. "
            "If needed, use the largest dimensions that fit."
        )

    if not requests:
        requests.append("No specific edit request was provided; make no changes.")

    return (
        BASE_PROMPT
        + f"Keep the output canvas close to the source aspect ratio ({aspect_ratio:.2f}:1) "
        "and preserve the framing and subject placement. "
        + " ".join(requests)
    )


def build_local_prompt(settings):
    """Return only the text entered in the AI edit fields."""
    user_requests = []

    for key in FIELD_RULES:
        value = str(settings.get(key, "")).strip()
        if value:
            user_requests.append(value)

    return " ".join(user_requests)


def is_local_model_available():
    """Check whether the configured local model endpoint can be reached."""
    local_model_url = os.getenv("LOCAL_MODEL_URL", "").strip()
    if not local_model_url:
        return False

    try:
        response = requests.get(local_model_url, timeout=3)
    except requests.RequestException:
        return False

    # The model endpoint accepts POST requests, so GET normally returns 405.
    return response.status_code in {200, 405}


def apply_ai_edits(local_image_path, settings):
    provider = str(settings.get("provider", "openai")).strip().lower()
    if provider == "local":
        local_model_url = os.getenv("LOCAL_MODEL_URL", "").strip()
        if not local_model_url:
            raise ValueError("The local AI model is not configured.")

        prompt = build_local_prompt(settings)
        with open(local_image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        response = requests.post(
            local_model_url,
            json={"image": encoded_image, "prompt": prompt},
            timeout=300,
        )
        response.raise_for_status()
        return base64.b64decode(response.json()["image"])

    if provider != "openai":
        raise ValueError("Unknown AI provider.")

    # Read the source size so the OpenAI prompt can mention its ratio.
    with Image.open(local_image_path) as source_image:
        width, height = source_image.size
    prompt = build_ai_prompt(settings, (width, height))

    # The API key is read by the OpenAI client from OPENAI_API_KEY in .env.
    client = OpenAI()
    with open(local_image_path, "rb") as image_file:
        response = client.images.edit(
            model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2"),
            image=image_file,
            prompt=prompt,
            size="auto",
        )

    return base64.b64decode(response.data[0].b64_json)
