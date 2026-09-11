from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------------
# Project Paths
# ---------------------------------------------------------

# financial-document-intelligence/
# ├── backend/
# │   └── app/
# │       └── core/
# │           └── config.py
# └── frontend/
#
# parents[0] = core
# parents[1] = app
# parents[2] = backend
# parents[3] = financial-document-intelligence

PROJECT_ROOT = Path(__file__).resolve().parents[3]

BACKEND_DIR = PROJECT_ROOT / "backend"

FRONTEND_DIR = PROJECT_ROOT / "frontend"

FRONTEND_TEMPLATES_DIR = FRONTEND_DIR / "templates"

FRONTEND_STATIC_DIR = FRONTEND_DIR / "static"


# ---------------------------------------------------------
# Application Settings
# ---------------------------------------------------------

class Settings(BaseSettings):

    # -----------------------------------------------------
    # Application
    # -----------------------------------------------------

    app_name: str = "Financial Document Intelligence API"

    app_version: str = "1.0.0"

    debug: bool = True


    # -----------------------------------------------------
    # Database
    # -----------------------------------------------------

    database_url: str = "sqlite:///./documents.db"


    # -----------------------------------------------------
    # File Validation
    # -----------------------------------------------------

    max_pages: int = 3

    max_file_size_mb: int = 10

    allowed_extensions: tuple[str, ...] = (
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png",
    )


    # -----------------------------------------------------
    # OCR
    # -----------------------------------------------------

    tesseract_cmd: str = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )


    # -----------------------------------------------------
    # Gemini
    # -----------------------------------------------------

    gemini_api_key: str = ""

    gemini_model: str = "gemini-3.6-flash"


    # -----------------------------------------------------
    # API
    # -----------------------------------------------------

    api_prefix: str = "/api/v1"

    documents_prefix: str = "/documents"


    # -----------------------------------------------------
    # Frontend
    # -----------------------------------------------------

    frontend_dir: Path = FRONTEND_DIR

    frontend_templates_dir: Path = FRONTEND_TEMPLATES_DIR

    frontend_static_dir: Path = FRONTEND_STATIC_DIR


    # -----------------------------------------------------
    # Settings Configuration
    # -----------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# ---------------------------------------------------------
# Settings Instance
# ---------------------------------------------------------

settings = Settings()