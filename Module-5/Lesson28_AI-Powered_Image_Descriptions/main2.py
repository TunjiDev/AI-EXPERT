import google.generativeai as genai
from typing import Optional

class GeminiCaptioner:
    """A class to handle image captioning using Google Generative AI (Gemini)."""

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def caption_image(self, image_source: str = "input.png") -> Optional[str]:
        """
        Generates a caption for an image using Gemini.
        Args:
            image_source (str): Path to the image file.
        Returns:
            Optional[str]: The generated caption.
        """
        try:
            with open(image_source, "rb") as f:
                image_bytes = f.read()
        except FileNotFoundError:
            print(f"[Error] Image file '{image_source}' not found.")
            return None
        except Exception as e:
            print(f"[Error] Unable to open image file. Details: {e}")
            return None

        try:
            # Send image to Gemini for captioning
            response = self.model.generate_content([
                {"mime_type": "image/png", "data": image_bytes},
                "Generate a short descriptive caption for this image."
            ])

            return response.text.strip() if response.text else "No caption found"
        except Exception as e:
            print(f"[Error] Gemini API request failed: {e}")
            return None


def main():
    GEMINI_API_KEY = "AIzaSyAGsjEmn-ImWCykbCDMsQTzQktl2aN6Kl4"  # replace with your real key
    captioner = GeminiCaptioner(api_key=GEMINI_API_KEY, model_name="gemini-1.5-flash")

    image_path = "test.jpg"
    caption = captioner.caption_image(image_path)

    if caption:
        print(f"Image: {image_path}\nCaption: {caption}")


if __name__ == "__main__":
    main()
