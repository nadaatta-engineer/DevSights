from pydantic import BaseModel

class CommitInfo(BaseModel):
    commit_id : str
    author : str
    commit_message : str
    changed_lines : list[str] 