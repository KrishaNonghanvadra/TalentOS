from typing import Dict, Optional

from pydantic import BaseModel


class GitHubAnalysisResponse(BaseModel):
    username: str
    name: Optional[str]
    public_repositories: int
    languages: Dict[str, int]