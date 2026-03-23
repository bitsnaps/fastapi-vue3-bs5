import os
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')
agent = Agent(model=Groq(id=DEFAULT_MODEL))
agent.print_response("Share a quick and healthy breakfast recipe.", stream=True)