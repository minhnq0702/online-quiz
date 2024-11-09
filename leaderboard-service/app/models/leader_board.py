from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.repo import db


class LeaderBoard(BaseModel):
    """
    Leaderboard entry for user/quiz
    """
    id: Optional[db.PyObjectId] = Field(alias="_id", default=None)
    # id: ObjectId = Field(alias="_id", default=None)
    quiz_id: int = Field(...)
    username: str = Field(...)
    score: float = Field(0.0)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders = {ObjectId: str},
    extra = 'ignore',
    use_enum_values = True
    )
        
