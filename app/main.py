from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import asyncio
from contextlib import asynccontextmanager
from app.core.batch_worker import batch_worker
from app.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(batch_worker())
    yield
    task.cancel()

app = FastAPI(lifespan=lifespan)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)