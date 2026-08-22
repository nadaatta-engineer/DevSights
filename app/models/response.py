from typing import Optional
from pydantic import BaseModel
from app.models.commit import CommitInfo

class RootCause(BaseModel):
    responsible_commit : CommitInfo
    suspected_line : str
    reason : str
    solution : str
    is_code_fix : bool
    recommended_code : Optional[str] = None #it may not exist
    
class RemediationResponse(BaseModel):
    success : bool
    pr_url : Optional[str] = None #it may not exist
    message : str