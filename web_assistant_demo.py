import os
from pathlib import Path
from web_assistant import WebAssistant
from dotenv import load_dotenv
from phi.tools.shell import ShellTools
from phi.tools.file import FileTools
from phi.llm.openai import OpenAIChat

load_dotenv()


DEFAULT_MODEL = os.getenv('DEFAULT_MODEL') or 'gpt-4o-mini'

cwd = Path(__file__).parent.resolve()
working_dir = cwd.joinpath("working_dir")
if not working_dir.exists():
    working_dir.mkdir(exist_ok=True, parents=True)

llm=OpenAIChat(model=DEFAULT_MODEL, max_tokens=8000, temperature=.2)

agent = WebAssistant(
    description="You help write a full web site using web technologies.",
           instructions=[
                "When you recieved an input from the user do the following:\n"
                " - First **THINK** before writing any code.\n"
                " - Breakdown it into small manageable steps which you can do using the right tools.\n"
                " - Define for every step what tool(s) you need to use.\n"
                "After that, use the right tool to do every step as planned.",
                "Do not output any information about what you have to do, just perform your task.",
                "Do not run any script that run the app at the end.",
                "Do not run any script that run the app at the end.",
                f"**IMPORTANT**: All your created files must be saved into this directory :{working_dir}",
                # f"**IMPORTANT**: Save a summary file to output all the steps you took to accomplish your task into :{working_dir}summary.md",
    ],
    llm=llm,
    show_tool_calls=True,
    tools=[ShellTools, FileTools(base_dir=working_dir)],
    debug_mode=True
)

result = agent.run('Build a landing page for AI Agent development startup using Tailwind CSS.')
# result = agent.run('Build an agency website for AI development using React and Tailwind CSS.')
# result = agent.run(f"Continue by building the agency website for AI development using React and Tailwind CSS which you can find in the {working_dir}")
# result = agent.run('Build a web api to display the crypto princing in USD.')
# print the output the result or stream it if it's a dict type
if isinstance(result, dict):
    print(result)
else:
    for delta in result:
        print(delta, end='', flush=True)

