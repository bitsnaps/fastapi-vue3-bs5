import os
# from phi.assistant import Assistant
# from phi.llm.openai import OpenAIChat
# from phi.tools.duckduckgo import DuckDuckGo
# from phi.tools.shell import ShellTools
from agno.agent import Agent
from agno.models.groq import Groq
# from agno.tools.csv_toolkit import CsvTools
from agno.tools.shell import ShellTools
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

load_dotenv()
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')

# assistant = Assistant(llm=OpenAIChat(model=DEFAULT_MODEL, max_tokens=4000, temperature=.2), 
# tools=[DuckDuckGo(), ShellTools()], show_tool_calls=False, read_chat_history=True)
# assistant.cli_app(markdown=False)


# Set up your agent with tools and instructions
agent = Agent(
    model=Groq(id=DEFAULT_MODEL, max_tokens=4000, temperature=.2),
    tools=[
        # CsvTools(csvs=[your_csv_file])
        DuckDuckGoTools(), ShellTools()
        ],
    markdown=False,
    show_tool_calls=True,
    read_chat_history=True,
    # instructions=[
    #     "First always get the list of files",
    #     "Then check the columns in the file",
    #     "Then run the query to answer the question",
    # ],
)

# Start the CLI app
agent.cli_app(stream=False)