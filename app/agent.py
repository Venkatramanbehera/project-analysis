from github import Github
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from .github_tool import get_github_project_info
import os

load_dotenv()

llm = ChatOpenAI(
    temperature=0, 
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

tools = [
    Tool(
        name="GitHubProjectInfo",
        func=get_github_project_info,
        description="""
            Use this tool to get GitHub project data from either a classic repo project
            or a user-level GitHub Projects v2 dashboard (URL format: https://github.com/users/<username>/projects/<number>).
            Pass the full GitHub project or repo URL as input.
        """
    )
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)