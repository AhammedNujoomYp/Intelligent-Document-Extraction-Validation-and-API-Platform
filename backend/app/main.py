from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.database import Base, engine
from app.api.routes.documents import router as documents_router


# ---------------------------------------------------------
# Database
# ---------------------------------------------------------

Base.metadata.create_all(bind=engine)


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-powered Financial Document Intelligence API",
)


# ---------------------------------------------------------
# Static Files
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(
        directory=settings.frontend_static_dir
    ),
    name="static",
)


# ---------------------------------------------------------
# Templates
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=settings.frontend_templates_dir
)


# ---------------------------------------------------------
# API Routes
# ---------------------------------------------------------

app.include_router(documents_router)


# ---------------------------------------------------------
# Frontend - Dashboard
# ---------------------------------------------------------

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request
        },
    )


# ---------------------------------------------------------
# Frontend - Result Page
# ---------------------------------------------------------

@app.get("/result.html")
def result_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="result.html",
        context={
            "request": request
        },
    )


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get(
    f"{settings.api_prefix}/health",
    tags=["Health"],
)
def health_check():
    return {
        "status": "ok"
    }