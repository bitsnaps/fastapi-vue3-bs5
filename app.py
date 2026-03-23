import os, sys
import subprocess
from typing import (List, Any)
from dotenv import load_dotenv
from phi.assistant import Assistant
from phi.assistant.python import PythonAssistant
from phi.llm.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.file.local.csv import CsvFile
from phi.tools.shell import ShellTools

load_dotenv()

# os.environ["OPENAI_API_KEY"] = os.environ.get("GROQ_API_KEY")
# os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"

def get_user_name():
    """Use this function to find user's name.

    Returns:
        str: The name of the user.
    """    
    return os.getenv('USER')

def execute_code(code: str) -> str:
    """Use this function to execute code on this machine.

    Args:
        code: The commande with arguments to execute.
    
    Returns:
        The output of the command.
    """
    process = subprocess.Popen(code, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr:
        return f"Error: {stderr.decode()}"
    return stdout.decode()

class CoderAgent(PythonAssistant):
    def __init__(self):
        pass

class Agent(Assistant):

    default_model: str = 'llama-3.1-70b-versatile' #'llama3-groq-70b-8192-tool-use-preview'
    system_prompt: str = """You are a super agent capable of managing complex tasks.
    You are able and allowed to execute python code and read its output.
    """
    max_tokens: int = 4000
    temperature: float = 0.7

    def __init__(self, llm=None):
        super().__init__()
        if llm is None:
            self.llm = OpenAIChat(model=self.default_model, max_tokens=self.max_tokens, temperature=self.temperature)

    def ask(self, show_tool_calls=False, max_tokens=3000, temperature=0.7, tools=[DuckDuckGo()], message=None):
        if message is None or message.strip() == '':
            print('You must provide a message.')
            return
        assistant = Assistant(
            system_prompt=self.system_prompt,
            show_tool_calls=show_tool_calls,
            llm=self.llm,
            tools=tools,
            debug_mode=False,
            run_id=None)
        answer = assistant.run(message, stream=False)
        return answer
    
    def execute(self, files=[], pip_install=False, show_tool_calls=False, markdown=False, message=None): # files=[CsvFile(path="...csv", description="...")]
        if message is None or len(message.strip())==0:
            print('You must provide a message.')
            return
        
        python_assistant = PythonAssistant(
            add_to_system_prompt=f"We are running on: {sys.platform} machine.\n",
            llm=self.llm,
            files=files,
            pip_install=pip_install,
            show_tool_calls=show_tool_calls,
        )
        return self.run(message, stream=False)
    
    def cli(self, markdown=True):
        self.cli_app(markdown=markdown)


if __name__=='__main__':
    # Use online search
    # print(Agent().ask(message='How find the current OS using python?')) # import sys; print(sys.platform)
    # print(Agent().ask(tools=[DuckDuckGo()], message='What is happenning now in Algeria?'))
    # Use ShellTools
    # print(Agent().ask(tools=[ShellTools()], message='What OS we are running here?'))
    # Execute shell code
    # print(Agent().ask(tools=[ShellTools()], message='How many files in the current directory?'))
    # print(Agent().ask(tools=[ShellTools()], message='How many directories are there in the current directory?'))
    # print(Agent().ask(tools=[get_user_name], message='Hello Assistant!', max_tokens=10, temperature=0.1))
    # print(Agent().ask(tools=[execute_code], message='list files in the current directory.'))
    # Execute python code
    # it runs: "bash -c history > history.txt" which won't work
    # print(Agent().execute(message='Create a file named history.txt and store the output of history command to it.'))
    # print(Agent().execute(message='What OS are we running here?'))
    # print(Agent().execute(message='How much free memory do we have left in this machine?'))
    print(Agent().execute(message='How much free disk space do we have left in this machine?'))
