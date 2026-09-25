import os

from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
import fitz


SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".pdf"}


class OCRProcessor:
    def __init__(self, language="eng"):
        self.language = language

    def preprocess_image(self, image):
        image = image.convert("L")
        image = ImageEnhance.Contrast(image).enhance(1.8)
        image = image.filter(ImageFilter.SHARPEN)
        return image

    def image_to_text(self, image):
        image = self.preprocess_image(image)
        return pytesseract.image_to_string(
            image,
            lang=self.language
        )

    def pdf_to_text(self, file_path):
        document = fitz.open(file_path)
        all_text = []

        for page in document:
            pix = page.get_pixmap()

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            all_text.append(
                self.image_to_text(image)
            )

        document.close()

        return "\n".join(all_text)

    def process(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = os.path.splitext(
            file_path
        )[1].lower()

        if extension not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension == ".pdf":
            text = self.pdf_to_text(file_path)
        else:
            image = Image.open(file_path)
            text = self.image_to_text(image)

        return {
            "file_name": os.path.basename(file_path),
            "file_type": extension,
            "text": text.strip()
        }
