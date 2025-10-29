from fastapi import FastAPI
from routers import preprocess_router, visualize_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="AI Data Analyzer API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
if not os.path.exists("visuals"):
    os.makedirs("visuals")
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Mount the visuals directory for generated chart images
app.mount("/visuals", StaticFiles(directory="visuals"), name="visuals")

# Routers
app.include_router(preprocess_router.router, prefix="/api/preprocess", tags=["Preprocessing"])
app.include_router(visualize_router.router, prefix="/api/visualize", tags=["Visualization"])

# Serve the frontend HTML file at root
@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main frontend HTML page"""
    frontend_path = os.path.join("frontend", "index.html")
    if os.path.exists(frontend_path):
        with open(frontend_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Error: Frontend file not found</h1>"

@app.get("/api/visuals/list")
def list_visuals():
    """List all saved visualization files"""
    if not os.path.exists("visuals"):
        return {"files": []}

    files = [
        f"/visuals/{f}"  # ✅ Only single /visuals/
        for f in os.listdir("visuals")
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    return {"files": files}


@app.get("/api")
def api_home():
    return {"message": "Welcome to AI Data Analyzer API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)