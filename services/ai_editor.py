import base64
import os

from openai import OpenAI


def build_ai_prompt(settings):
    prompt_parts = []

    for key, label in (
        ("generativeModification", "Generative modification"),
        ("backgroundManipulation", "Background manipulation"),
        ("enhancement", "Enhancement"),
    ):
        value = str(settings.get(key, "")).strip()
        if value:
            prompt_parts.append(f"{label}: {value}")

    upscaling = str(settings.get("upscaling", "1")).strip()
    if upscaling and upscaling != "1":
        prompt_parts.append(f"Upscale the image by {upscaling}x.")

    if not prompt_parts:
        prompt_parts.append(
            "Improve the image quality while preserving the original subject and composition."
        )

    return (
        "Edit the provided image according to these instructions. "
        + " ".join(prompt_parts)
        + " Preserve the main subject and make the result look natural."
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
