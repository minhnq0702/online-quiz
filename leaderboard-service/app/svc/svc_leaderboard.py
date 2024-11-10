from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo.results import UpdateResult

from app.dto.dto_leader_board import (DtoLeadboardData, DtoUpsertLeaderBoard,
                                      DtoUserRank)
from app.models.leader_board import LeaderBoard


async def update_leaderboard(
    entry: DtoUpsertLeaderBoard,
    leaderboard_col: AsyncIOMotorCollection,
) -> str | None:
    """
    Upsert user/quiz/score into leaderboard
    """
    new_entry: UpdateResult = await leaderboard_col.update_one(
        entry.model_dump(exclude={"score"}),
        {
            "$inc": {"score": entry.score},
        },
        upsert=True,
    )
    return str(new_entry.upserted_id) if new_entry.upserted_id else None


async def get_leaderboard(
    quiz_id: str,
    leaderboard_col:
    AsyncIOMotorCollection,
    limit=10,
    user_id=None
) -> DtoLeadboardData:
    """
    Get top leaderboard
    """
    leaderboard_cursor = (
        leaderboard_col.find(
            {
                "quiz_id": quiz_id,
            }
        ).
        sort("score", -1).
        limit(limit)
    )
    raw_top_ranks = await leaderboard_cursor.to_list(length=10)
    top_ranks = [LeaderBoard(**entry) for entry in raw_top_ranks]
    user_rank = None
    if user_id:
        user_rank = await get_user_rank(quiz_id, user_id, leaderboard_col)
    return DtoLeadboardData(
        top_ranks=top_ranks,
        user_rank=user_rank,
    )


async def get_user_rank(quiz_id: str, user_id: str, leaderboard_col: AsyncIOMotorCollection) -> DtoUserRank:
    """
    # TODO: update user rank to redis right after update scores
    Get current user rank on leaderboard of the quiz
    Returns:
        int: rank of the user on leaderboard
    """
    pipeline = [
        {"$match": {"quiz_id": quiz_id}},
        # {"$sort": {"score": -1}},
        {
            "$setWindowFields": {
                "partitionBy": "$quiz_id",
                "sortBy": {"score": -1},
                "output": {
                    "rank": {
                        "$documentNumber": {}
                    }
                }
            }
        },
        {"$match": {"user_id": user_id}}
    ]

    result = await leaderboard_col.aggregate(pipeline).to_list(1)

    return DtoUserRank(
        rank=result[0].get("rank", 0) if result else 0,
        score=result[0].get("score", 0) if result else 0.0,
    )
