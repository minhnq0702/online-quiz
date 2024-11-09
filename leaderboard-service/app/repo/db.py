import logging
import os
from typing import Annotated

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BeforeValidator

_logger = logging.getLogger("uvicorn")

PyObjectId = Annotated[str, BeforeValidator(str)]


async def init_db_client(app: FastAPI):
    """
    Initialize the MongoDB client and attach it to the FastAPI app instance.
    Raises:
        Exception: If there is a problem connecting to the MongoDB cluster.
    """
    mongo_url = os.environ["MONGO_URL"]
    mongo_dbname = os.environ["MONGO_DBNAME"]
    client = AsyncIOMotorClient(mongo_url)
    app.state.mongodb_client = client

    db = client.get_database(mongo_dbname)
    app.state.mongodb = db


    ping_response = await app.state.mongodb.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    _logger.info("MongoDB connected.")


async def close_db_client(app: FastAPI):
    """
    Close DB connection

    Args:
        app (FastAPI): _description_
    """
    app.state.mongodb_client.close()
