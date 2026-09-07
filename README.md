# NeuroPix

NeuroPix is a web-based image editing application for standard and AI-assisted image edits.

Users can create an account, upload JPG or PNG images, apply Standard edits such as cropping, rotation, brightness, contrast, exposure, saturation, blur, sharpness, and grayscale, or send an image to the OpenAI image-editing API. Images are limited to 1080p, keep their aspect ratio during AI upscaling, and can be compared, downloaded, and managed from the Gallery.

The project uses a Flask backend, MySQL for user and image metadata, and Amazon S3 for storing original and processed images.

## Running the project

1. Install the packages:

   ```powershell
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in the local database, S3, Flask, and OpenAI values.

3. Start the Flask server:

   ```powershell
   python app.py
   ```

4. Open `http://127.0.0.1:5000` in a browser.

To run the basic automated checks:

```powershell
python -m pytest -q
```
