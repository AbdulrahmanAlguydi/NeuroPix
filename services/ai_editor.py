import base64
from math import ceil
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
        "colour, or detail changes. Do not add objects, change the background, or "
        "alter the composition."
    ),
}

BASE_PROMPT = (
    # Shared instructions keep unrelated text from changing other image properties.
    "Edit only the explicit requests below. Field descriptions are rules, not edits. "
    "Ignore unrelated text and treat empty fields as unchanged. Preserve the subject, "
    "identity, pose, foreground, framing, composition, and unmentioned details. "
    "Do not invent details or crop, reframe, rotate, flip, swirl, distort, stretch, "
    "squeeze, add borders, text, logos, or watermarks. "
    "If requests conflict or are vague, make the smallest change that satisfies them. "
    "Apply all valid requests together. "
)

MIN_CUSTOM_PIXELS = 655_360


def calculate_output_size(source_size, upscaling):
    """Return an OpenAI image size based on the source and selected scale."""
    width, height = source_size
    scale = float(upscaling)
    if scale < 1:
        scale = 1

    requested_width = width * scale
    requested_height = height * scale

    if width >= height:
        max_width, max_height = 1920, 1080
    else:
        max_width, max_height = 1080, 1920

    # The API requires at least 655,360 pixels for a custom size.
    pixel_count = requested_width * requested_height
    needs_minimum_size = pixel_count < MIN_CUSTOM_PIXELS
    if needs_minimum_size:
        minimum_scale = (MIN_CUSTOM_PIXELS / pixel_count) ** 0.5
        requested_width *= minimum_scale
        requested_height *= minimum_scale

    # Reduce both dimensions together when the request is above the 1080p cap.
    width_scale = max_width / requested_width
    height_scale = max_height / requested_height
    if width_scale < height_scale:
        limit_scale = width_scale
    else:
        limit_scale = height_scale

    if limit_scale > 1:
        limit_scale = 1
    else:
        requested_width *= limit_scale
        requested_height *= limit_scale

    if needs_minimum_size:
        # Round small images up so rounding does not drop below the minimum.
        requested_width = max(16, ceil(requested_width / 16) * 16)
        requested_height = max(16, ceil(requested_height / 16) * 16)
    else:
        requested_width = max(16, round(requested_width / 16) * 16)
        requested_height = max(16, round(requested_height / 16) * 16)

    # Rounding can push one edge over the cap, so adjust the other edge too.
    if requested_width > max_width:
        requested_width = (max_width // 16) * 16
        requested_height = round(requested_width * height / width / 16) * 16
    if requested_height > max_height:
        requested_height = (max_height // 16) * 16
        requested_width = round(requested_height * width / height / 16) * 16

    return f"{requested_width}x{requested_height}"


def build_ai_prompt(settings, source_size):
    # Keep the visual composition aligned with the source image.
    width, height = source_size
    aspect_ratio = width / height
    requests = []

    for key, rule in FIELD_RULES.items():
        # Empty fields are skipped so they do not add accidental instructions.
        value = str(settings.get(key, "")).strip()
        if value:
            requests.append(f"{rule} User request: {value}")

    if not requests:
        requests.append("No specific edit request was provided; make no changes.")

    return (
        BASE_PROMPT
        + f"Preserve the source aspect ratio ({aspect_ratio:.2f}:1), framing, "
        "and subject placement. "
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
    output_size = calculate_output_size(
        (width, height), settings.get("upscaling", "1")
    )

    # The API key is read by the OpenAI client from OPENAI_API_KEY in .env.
    client = OpenAI()
    with open(local_image_path, "rb") as image_file:
        response = client.images.edit(
            model=os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2.5-sunburst"),
            image=image_file,
            prompt=prompt,
            quality="xhigh",
            size=output_size,
        )

    return base64.b64decode(response.data[0].b64_json)
