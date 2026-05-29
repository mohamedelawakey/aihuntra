from .docx_loader import DocxLoaderAndExtractor
from .pdf_loader import PDFLoaderAndExtractor
from .config import Config

from pathlib import Path
import zipfile


class FullText:
    """Extract and validate supported document files."""

    @staticmethod
    def get_document_metadata(file_path: str) -> dict[str, str | int | bool]:
        """Return safe metadata for a document before extraction."""
        path = Path(file_path)
        extension = path.suffix.lower().lstrip(".")

        return {
            "file_name": path.name,
            "file_path": str(path),
            "extension": extension,
            "exists": path.exists(),
            "is_file": path.is_file(),
            "size_bytes": path.stat().st_size if path.exists() and path.is_file() else 0,
            "max_size_bytes": Config.MAX_FILE_SIZE_BYTES,
        }

    @staticmethod
    def validate_document_metadata(file_path: str) -> dict[str, str | int | bool]:
        """Validate extension, existence, size, and basic file signature."""
        metadata = FullText.get_document_metadata(file_path)

        if not metadata["exists"]:
            raise FileNotFoundError(f"File does not exist: {file_path}")

        if not metadata["is_file"]:
            raise ValueError(f"Path is not a file: {file_path}")

        extension = str(metadata["extension"])
        if extension not in Config.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file format: {extension}")

        if int(metadata["size_bytes"]) > Config.MAX_FILE_SIZE_BYTES:
            raise ValueError(
                "File size exceeds the allowed limit: "
                f"{metadata['size_bytes']} bytes > {Config.MAX_FILE_SIZE_BYTES} bytes"
            )

        if int(metadata["size_bytes"]) == 0:
            raise ValueError("File is empty")

        if extension == "pdf" and not FullText._looks_like_pdf(file_path):
            raise ValueError("File extension is PDF but file content does not look like a PDF")

        if extension == "docx" and not FullText._looks_like_docx(file_path):
            raise ValueError("File extension is DOCX but file content does not look like a DOCX")

        return metadata

    @staticmethod
    def extract_document_parts(file_path: str) -> list[dict[str, str]]:
        """Extract document parts from a supported file."""
        metadata = FullText.validate_document_metadata(file_path)
        extension = str(metadata["extension"])

        if extension == "pdf":
            return PDFLoaderAndExtractor.load_extract_pdf(file_path)

        if extension == "docx":
            return DocxLoaderAndExtractor.load_extract_docx(file_path)

        raise ValueError(f"Unsupported file format: {extension}")

    @staticmethod
    def extract_full_text(file_path: str) -> str:
        """Extract one clean full-text string from a supported file."""
        document_parts = FullText.extract_document_parts(file_path)
        return "\n".join(
            part["text"].strip()
            for part in document_parts
            if part.get("text", "").strip()
        )

    @staticmethod
    def extract_document_payload(file_path: str) -> dict[str, object]:
        """Extract metadata, document parts, and full text together."""
        metadata = FullText.validate_document_metadata(file_path)
        document_parts = FullText.extract_document_parts(file_path)
        full_text = "\n".join(
            part["text"].strip()
            for part in document_parts
            if part.get("text", "").strip()
        )

        return {
            "metadata": metadata,
            "document_parts": document_parts,
            "full_text": full_text,
            "parts_count": len(document_parts),
            "characters_count": len(full_text),
        }

    @staticmethod
    def _looks_like_pdf(file_path: str) -> bool:
        with open(file_path, "rb") as file:
            return file.read(4) == b"%PDF"

    @staticmethod
    def _looks_like_docx(file_path: str) -> bool:
        return zipfile.is_zipfile(file_path)
