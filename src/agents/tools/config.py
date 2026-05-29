class Config:
    """Configuration class for the document processing system."""

    ALLOWED_EXTENSIONS = {
        "pdf",
        "docx"
    }

    MAX_FILE_SIZE_BYTES = 200 * 1024
