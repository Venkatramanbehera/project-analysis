from fastapi import FastAPI
from .schemas import GitHubQuery
from .agent import agent

app = FastAPI()

@app.post("/query-github")
def query_github(data: GitHubQuery):
    prompt = f"Repo: {data.repo_url}\nQuestion: {data.query}"
    result = agent.run(prompt)
    return {"response": result}