from docx import Document
from typing import List


class DocxLoaderAndExtractor:
    """Utility class for loading and processing DOCX files."""
    
    @staticmethod
    def load_extract_docx(path_file: str) -> List[dict[str, str]]:
        document = Document(path_file)
        pages = []

        for index, paragraph in enumerate(document.paragraphs):
            text = paragraph.text

            if not text.strip():
                continue

            pages.append(
                {
                    "index": str(index + 1),
                    "type": "paragraph",
                    "text": text
                }
            )

        return pages
