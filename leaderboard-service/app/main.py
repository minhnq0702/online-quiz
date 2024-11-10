import asyncio
import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from app.external.kafka import consume_messages, init_consumer_client
from app.repo.db import close_db_client, init_db_client
from app.routes.api_leaderboard import router as leaderboard_route

_logger = logging.getLogger("uvicorn")

load_dotenv("app/.env")


@asynccontextmanager
async def lifespan(_app: FastAPI):
    """
    App lifespan init and close connection

    Args:
        _app (FastAPI):
    """
    await init_db_client(_app)

    # FIXME: We can adjust the number of consumers based on the number of users joining the quiz AND the number of Kafka partitions.
    # !Ensure that each event containing an individual user's score uses the same user_id key to keep it in the same partition.
    consumer_client = init_consumer_client()

    asyncio.create_task(consume_messages(
        consumer_client, _app.state.mongodb.get_collection("leaderboard")))
    yield
    await close_db_client(_app)

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(leaderboard_route, prefix="/leaderboard")
