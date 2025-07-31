"""Backend application entry point"""

from fastapi import FastAPI, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware import cors
from contextlib import asynccontextmanager
from backend.storage.database import db_init, close_db
# import routers
from backend.api.v1.routers import users

app_router = APIRouter(prefix="/api/v1", tags=["v1"])

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    db_init()
    yield
    close_db()

app = FastAPI(lifespan=lifespan)
app_router.include_router(users.user_router)
app.include_router(app_router)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    """Root endpoint"""
    return JSONResponse(content={"message": "Backend is running!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
