from io import BytesIO

from fastapi import UploadFile
from pypdf import PdfReader

class PDFService:
    @staticmethod
    async def extract_text_from_pdf(file: UploadFile) -> str:
        if file.content_type != "application/pdf":
            raise ValueError("File harus berformat PDF.")

        file_bytes = await file.read()

        if not file_bytes:
            raise ValueError("File PDF tidak boleh kosong.")

        reader = PdfReader(BytesIO(file_bytes))

        pages_text: list[str] = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text)

        extracted_text = "\n".join(pages_text).strip()

        if not extracted_text:
            raise ValueError("Teks tidak dapat diekstrak dari PDF.")

        return extracted_text