from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import router as audit_router

app = FastAPI(
    title="Guardian-RAG API",
    description="Agentic Compliance Engine for Regulatory Audits",
    version="1.0.0"
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"], # React/Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the routes
app.include_router(audit_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Guardian-RAG"}

if __name__ == "__main__":
    import uvicorn
    # Run the server
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)