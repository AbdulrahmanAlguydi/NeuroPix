from PIL import Image, ImageEnhance, ImageFilter, ImageOps


def apply_standard_edits(image, settings):
    """
    Applies the Standard Edits settings (from the workspace sliders) to a
    PIL Image and returns a new, edited PIL Image.
    """
    # Read all the settings, using the same default values as the sliders
    # on the frontend so a missing field just means "no change".
    crop_width_percent = float(settings.get("cropWidth", 100))
    crop_height_percent = float(settings.get("cropHeight", 100))
    rotation_degrees = int(settings.get("rotation", 0))
    brightness_percent = float(settings.get("brightness", 100))
    contrast_percent = float(settings.get("contrast", 100))
    exposure_percent = float(settings.get("exposure", 0))
    saturation_percent = float(settings.get("saturation", 100))
    blur_amount = float(settings.get("blur", 0))
    sharpness_percent = float(settings.get("sharpness", 0))
    grayscale_percent = float(settings.get("grayscale", 0))

    # Work in RGB so the filters below behave the same for JPG and PNG.
    edited = image.convert("RGB")

    # 1. Rotate first, so the crop below uses the already-rotated image.
    if rotation_degrees:
        edited = edited.rotate(-rotation_degrees, expand=True)

    # 2. Crop to the requested percentage of width/height, centered.
    original_width, original_height = edited.size
    new_width = max(1, int(original_width * crop_width_percent / 100))
    new_height = max(1, int(original_height * crop_height_percent / 100))
    left = (original_width - new_width) // 2
    top = (original_height - new_height) // 2
    edited = edited.crop((left, top, left + new_width, top + new_height))

    # 3. Brightness and exposure both make the image lighter or darker,
    #    so we combine them into a single brightness factor.
    brightness_factor = (brightness_percent / 100) * (1 + exposure_percent / 100)
    edited = ImageEnhance.Brightness(edited).enhance(brightness_factor)

    # 4. Contrast.
    edited = ImageEnhance.Contrast(edited).enhance(contrast_percent / 100)

    # 5. Saturation (color intensity).
    edited = ImageEnhance.Color(edited).enhance(saturation_percent / 100)

    # 6. Blur.
    if blur_amount > 0:
        edited = edited.filter(ImageFilter.GaussianBlur(radius=blur_amount))

    # 7. Sharpness.
    if sharpness_percent > 0:
        sharpness_factor = 1 + (sharpness_percent / 100)
        edited = ImageEnhance.Sharpness(edited).enhance(sharpness_factor)

    # 8. Grayscale, blended by percentage so e.g. 50% gives a partial
    #    black-and-white look instead of an all-or-nothing switch.
    if grayscale_percent > 0:
        gray_version = ImageOps.grayscale(edited).convert("RGB")
        edited = Image.blend(edited, gray_version, grayscale_percent / 100)

    return edited
