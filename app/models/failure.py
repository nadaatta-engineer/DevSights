from pydantic import BaseModel
from app.models.commit import CommitInfo

class FailureLog(BaseModel):
    build_id : str
    error_log : str
    recent_commit : CommitInfo