import pathlib
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import fastapi.exceptions
from starlette.staticfiles import StaticFiles
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Import the new router
from api.auth_router import router as auth_router

# Define the FastAPI app
app = FastAPI(title="Gemini Fullstack with Auth")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: In production, change "*" to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# --- Your Frontend Serving Logic (No changes needed here) ---

def create_frontend_router(build_dir="../../frontend/dist"):
    build_path = pathlib.Path(__file__).parent.parent.parent / build_dir
    static_files_path = build_path / "assets"

    if not build_path.is_dir() or not (build_path / "index.html").is_file():
        print(f"WARN: Frontend build directory not found at {build_path}.")
        from starlette.routing import Route
        async def dummy_frontend(request):
            return Response("Frontend not built.", media_type="text/plain", status_code=503)
        return Route("/{path:path}", endpoint=dummy_frontend)

    react = FastAPI(openapi_url="")
    react.mount("/assets", StaticFiles(directory=static_files_path), name="static_assets")

    @react.get("/{path:path}")
    async def handle_catch_all(request: Request, path: str):
        fp = build_path / path
        if not fp.exists() or not fp.is_file():
            fp = build_path / "index.html"
        return fastapi.responses.FileResponse(fp)
    return react

# Mount the frontend. It is important to mount it after the API routers.
app.mount("/", create_frontend_router(), name="frontend")