import logging
import os

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

_logger = logging.getLogger("uvicorn")


async def init_db_client(app: FastAPI):
    mongo_url = os.environ["MONGO_URL"]
    mongo_dbname = os.environ["MONGO_DBNAME"]
    app.mongodb_client = AsyncIOMotorClient(mongo_url)
    app.mongodb = app.mongodb_client.get_database(mongo_dbname)

    ping_response = await app.mongodb.command("ping")
    if int(ping_response["ok"]) != 1:
        raise Exception("Problem connecting to database cluster.")
    else:
        _logger.info("Connected to database cluster.")
    _logger.info("MongoDB connected.")


def close_db_client(app: FastAPI):
    app.mongodb_client.close()
