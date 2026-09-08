import base64
from io import BytesIO

import litserve as ls
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image


MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"


class ImageEditAPI(ls.LitAPI):
    def setup(self, device):
        data_type = torch.float16 if str(device).startswith("cuda") else torch.float32
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
            MODEL_ID,
            torch_dtype=data_type,
            safety_checker=None,
        ).to(device)

    def decode_request(self, request):
        image_data = base64.b64decode(request["image"])
        image = Image.open(BytesIO(image_data)).convert("RGB")
        return image, request.get("prompt", "")

    def predict(self, inputs):
        image, prompt = inputs
        with torch.inference_mode():
            result = self.pipe(
                prompt=prompt,
                image=image,
                strength=1.0,
                guidance_scale=7.5,
                num_inference_steps=20,
            )
        return result.images[0]

    def encode_response(self, image):
        output = BytesIO()
        image.save(output, format="PNG")
        return {"image": base64.b64encode(output.getvalue()).decode("utf-8")}


if __name__ == "__main__":
    server = ls.LitServer(ImageEditAPI(), accelerator="auto")
    server.run(port=8000)
