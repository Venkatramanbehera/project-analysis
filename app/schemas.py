from pydantic import BaseModel

class GitHubQuery(BaseModel):
    repo_url: str
    query: str