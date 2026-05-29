from typing import List
import fitz


class PDFLoaderAndExtractor:
    """Utility class for loading and processing PDF files."""

    @staticmethod
    def load_extract_pdf(file_path: str) -> List[dict[str, str]]:
        with fitz.open(file_path) as document:
            pages = []

            for page_num, page in enumerate(document):
                text = page.get_text()

                if not text.strip():
                    continue

                pages.append(
                    {
                        "index": str(page_num + 1),
                        "type": "page",
                        "text": text
                    }
                )

        return pages
