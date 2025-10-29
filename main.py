from fastapi import FastAPI
from routers import preprocess_router, visualize_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Data Analyzer API")

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(preprocess_router.router, prefix="/api/preprocess", tags=["Preprocessing"])
app.include_router(visualize_router.router, prefix="/api/visualize", tags=["Visualization"])

@app.get("/")
def home():
    return {"message": "Welcome to AI Data Analyzer API!"}
