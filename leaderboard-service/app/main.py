import logging

from dotenv import load_dotenv
from fastapi import FastAPI

from app.repo.db import close_db_client, init_db_client
from app.routes.leader_board import router as leaderboard_route

_logger = logging.getLogger("uvicorn")

load_dotenv("app/.env")


async def lifespan(_app: FastAPI):
    """
    App lifespan init and close connection

    Args:
        _app (FastAPI):
    """
    await init_db_client(_app)
    yield
    await close_db_client(_app)

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(leaderboard_route, prefix="/leaderboard")
