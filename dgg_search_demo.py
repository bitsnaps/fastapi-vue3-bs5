import os
from phi.assistant import Assistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.llm.openai import OpenAIChat
from dotenv import load_dotenv

load_dotenv()


DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')
llm=OpenAIChat(model=DEFAULT_MODEL, max_tokens=4000, temperature=.5)

agent = Assistant(llm=llm, tools=[DuckDuckGo()], show_tool_calls=True)
response = agent.run("Whats happening in Gaza?", stream=False)
print(response)

