import json
import logging
import os
import traceback
from typing import TypedDict

from aiokafka import AIOKafkaConsumer
from motor.motor_asyncio import AsyncIOMotorCollection

from app.dto.dto_leader_board import DtoUpsertLeaderBoard
from app.svc.svc_leaderboard import update_leaderboard

_logger = logging.getLogger("uvicorn")


class EventScore(TypedDict):
    """
    Kafka Event schema for updating score from Answer service
    """
    quiz_id: str
    user_id: str
    score: float


def init_consumer_client():
    consumer = AIOKafkaConsumer(
        'score_updates',
        bootstrap_servers=os.environ["KAFKA_BROKER_URL"],
        group_id="leaderboard_service",
    )
    return consumer


async def consume_messages(consumer: AIOKafkaConsumer, leaderboard_col: AsyncIOMotorCollection):
    """
    Consume user score from kafka
    """
    await consumer.start()
    try:
        async for message in consumer:
            try:
                val = message.value
                if val is None:
                    continue
                scored_answer: EventScore = json.loads(val.decode())
                entry: DtoUpsertLeaderBoard = DtoUpsertLeaderBoard(
                    quiz_id=str(scored_answer["quiz_id"]),
                    user_id=str(scored_answer["user_id"]),
                    score=scored_answer["score"],
                )
                await update_leaderboard(entry, leaderboard_col)
            except Exception as e:
                _logger.error(f"update score from kafka failed {e} at {traceback.format_exc()}")
            else:
                _logger.info(f"update score for {entry.user_id} successfully")
    finally:
        await consumer.stop()
