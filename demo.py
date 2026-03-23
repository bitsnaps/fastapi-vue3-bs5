import os, sys, subprocess, random, time
from typing import (List, Any, Optional)
from pydantic import BaseModel, Field
from pathlib import Path
from textwrap import dedent
from dotenv import load_dotenv
from phi.llm.openai import OpenAIChat
from phi.knowledge.json import JSONKnowledgeBase
from phi.assistant import Assistant #, AssistantKnowledge
from phi.assistant.python import PythonAssistant
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.serpapi_tools import SerpApiTools
from phi.tools.yfinance import YFinanceTools
from phi.tools.shell import ShellTools
from phi.tools.file import FileTools
from phi.storage.assistant.sqllite import SqlAssistantStorage
from phi.vectordb.chroma import ChromaDb

load_dotenv()

db_file = "./ai.db"
cwd = Path(__file__).parent.resolve()
working_dir = cwd.joinpath("working_dir")
if not working_dir.exists():
    working_dir.mkdir(exist_ok=True, parents=True)

debug_mode = True

# Set up SQL storage for the assistant's data
storage = SqlAssistantStorage(table_name="messages", db_file=db_file)
storage.create()  # Create the storage if it doesn't exist

# Knowledge Base
knowledge_base = JSONKnowledgeBase(
    #urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    path=f"{working_dir}/data",
    vector_db=ChromaDb(collection="my_knowledge_base01"),
)
# Add information to the knowledge base
# knowledge_base.load_text("The sky is blue")

# Comment out after first run if: recreate=False
knowledge_base.load(recreate=True)

DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')

llm=OpenAIChat(model=DEFAULT_MODEL, max_tokens=4000, temperature=.5)
llm_writer=OpenAIChat(model=DEFAULT_MODEL, max_tokens=8000, temperature=.7)
llm_coder=OpenAIChat(model=DEFAULT_MODEL, max_tokens=4000, temperature=.2)
llm_research=OpenAIChat(model=DEFAULT_MODEL, max_tokens=8000, temperature=.2)

# Developer
python_assistant = PythonAssistant(
    name="Python Assistant",
    llm=llm_coder,
    role="Write and run python code without any additional text like 'here is the code' or something like that.",
    tools=[FileTools(base_dir=working_dir)],
    pip_install=True,
    extra_instructions=[
        "You can use the `read_file` tool to read a file, `save_file` to save a file, and `list_files` to list files in the working directory.\n"
        f"You always return information in human readable format as much as possible.\n",
        f"**Remember**: You are running on: {sys.platform} machine.\n",
    ],
    # charting_libraries=["streamlit"],
    base_dir=working_dir,
    debug_mode=debug_mode
)

# Writer
writer_assistant = Assistant(
            name="Writer Assistant",
            role="Write about any given topic in well formatted output.",
            llm=llm_writer,
            description="You are a world class and best eboook seller, you have the ability to write about any given topic.",
            instructions=[
                "Carefully read the instructions before generating the final output.",
                "Make your output is engaging, informative, and well-structured.",
                "Remember: you are writing for the most important company in the world, so the quality of the report is important.",
            ],
            expected_output=dedent(
                """\
            An engaging, informative, and well-structured output in the following format:
            <report_format>
            ## Title

            - **Overview** Brief introduction of the topic.
            - **Importance** Why is this topic significant now?

            ### Section 1
            - **Detail 1**
            - **Detail 2**

            ### Section 2
            - **Detail 1**
            - **Detail 2**

            ## Conclusion
            - **Summary of report:** Recap of the key findings from the report.
            - **Implications:** What these findings mean for the future.

            ## References
            - [Reference 1](Link to Source)
            - [Reference 2](Link to Source)
            </report_format>
            """
            ),
            tools=[],
            # This setting tells the LLM to format messages in markdown
            markdown=True,
            add_datetime_to_instructions=True,
            debug_mode=debug_mode,
        )

# Researcher
research_assistant = Assistant(
    name="Research Assistant",
    role="Search for informations online on any given topic",
    llm=llm_research,
    description="You are an Expert online researcher tasked with finding informations online using the best possbile techniques.",    
    instructions=[
        # "For a given topic, use the `duckduckgo_search` tool to search the internet get the top 5 search results.\n",
        "Given a topic, first generate a list of 3 search terms related to that topic.",
        "For each search term, `search_google` and `duckduckgo_search` and analyze the results."
        "From the results of all searcher, return the 10 most relevant URLs to the topic.",
        "Carefully read the results then extract only relevant informations to the topic then generate a final output.\n",
    ],
    expected_output="Well structured output about the topic in plain text format.",
    # tools=[ExaTools(num_results=5, text_length_limit=1000)],
    tools=[DuckDuckGo(fixed_max_results=5, news=True), SerpApiTools(search_youtube=False)],# search for news with: news=True
    # This setting tells the LLM to format messages in markdown
    add_datetime_to_instructions=True,
    debug_mode=debug_mode,
)

class Task(BaseModel):
    name: str = Field(..., description="Name of the task")
    description: str = Field(..., description="Description of the task")
    assignedAssistant: str = Field(..., description="The AI assistant assigned to do this task")
    taskType: str = Field(..., description="The type of task is either SIMPLE or COMPLEX")
    requiredTools: str = Field(..., description="The tools required to do this task from this list: DuckDuckGo, SerpApi, YahooFinance, PythonCoding, ShellExecution, FileIO")
    temperature: str = Field(..., description="The best float value required for the LLM in order to do this task")

class MissionPlan(BaseModel):
    title: str = Field(..., description="Give a title to this mission")
    tasks: List[Task] = Field(..., description="List of tasks to complete this mission")


def delay_calls(seconds: int=3) -> str:
    """Use this function to introduce a some delay to avoid throttling.

    Args:
        :param seconds: The number of seconds to delay. Default is 3.
    
    Returns:
        The message of waiting time.
    """
    time.sleep(seconds)
    return 'Waiting for {} seconds...'.format(seconds)

def execute_mission(missionPlan: MissionPlan) -> int:
    """
        Use this function to execute a tasks.
    
    Args:
        :param missionPlan: The mission plan to execute broken down by tasks.
    
    Returns:
        int: The number of tasks.
    """

    nbrOfTasks = len(missionPlan.tasks)

    print(f"Executing mission with {nbrOfTasks} tasks:")
    i = 0
    for task in missionPlan.tasks:
        i += 1
        print(f"Executing task N°{i}: {task}")
    
    return nbrOfTasks

def plan_mission(mission_description: str) -> MissionPlan:
    """
        Use this function to create a plan for a mission.
    
    Args:
        :param mission_description: The description of the mission.
    
    Returns:
        MissionPlan: The mission plan in structured format.
    """

    planer_agent = Assistant(
            name="Planner Assistant",
            role="Create a well structured plan to complete a given mission in well formatted output break it down by tasks.",
            description="""You are an AI agent expert project planner, you are capable of splitting any mission into small manageable tasks.
            Your goal is to read the mission and split it into small manageable tasks which can be done by AI agents when they are provided with the right tools.
            """,
            instructions=[
                "When you recieved an input do the following:\n"
                " - Breakdown it into small manageable sub-tasks which can be done by AI agents when they are provided with the right tools.\n"
                " - Define for every task what tool(s) need to be provided for each AI agent.\n"
                " - Dot not assign any task to yourself.\n"
                " - Here are the list of the available tools:\n"
                " - DuckDuckGo: Used to performm a search using DuckDuckGo engine.\n"
                " - SerpApiTools: Used to performm a search using Google engine.\n"
                " - YFinanceTools: Yahoo finance to grab informations.\n"
                " - ShellTools: Execute Shell script.\n"
                " - FileTools: Read and write to files on the system.\n"
                "Do not output any information about what you have to do, just perform your task.",
                # "**IMPORTANT**: Save your output to the Plan_[title-of-the-mision].md file.",
            ],        
            output_model=MissionPlan,
            llm=llm,
            # tools=[FileTools(base_dir=working_dir)], # Using "output_model" will prevent from using "tools"
            # add_datetime_to_instructions=True,
            debug_mode=False
        )
    missionPlan = planer_agent.run(mission_description)
    return missionPlan


agent = Assistant(
            description="""You are a super powerful AI agent that is helpful and capable of managing complex tasks.
            Your goal is to help the user or answer his questions in the best possible way.
            """,
            instructions=[
                "When the user sends a message, first **think** and determine if:\n"
                " - It is a question that you can answer directly, so just answer to the question in that case.\n"
                " - It is a SIMPLE task which you can do without delegating to an assistant, so just do it in that case.\n"
                " - It is a COMPLEX task, so use the tool `plan_mission` in order to create a plan.\n"
                " - You need to use a tool that is available to you\n"
                " - You need to search the knowledge base before answer any question\n"
                " - You need to delegate the task to a team member assistant\n"
                " - You need to ask clarifying the question\n",
                "If the user asks about a topic, first **ALWAYS** search your knowledge base using the `search_knowledge_base` tool.\n",
                "If you don't find relevant information in your knowledge base\n",
                "If the user asks to summarize the conversation or if you need to reference your chat history with the user, use the `get_chat_history` tool.\n",
                "If the users message is unclear, ask clarifying questions to get more information.\n",
                "Carefully read the information you have gathered from assistants or tools and provide a clear and concise answer to the user.\n",
                "Do not tell the user about what you have to do, just perform your task.\n",
                "Each call to assistant will cost a hit to the API endpoint, so make sure to delay calls using the `delay_calls` tool before calling any assistant in order to avoid API throttling.\n"
                "Write every response from assistants into your knowledge base for future reference.\n"
                "You can delegate tasks to an AI Assistant in your team depending of their role and the tools available to them.\n",
                "**IMPORTANT**: If the task is COMPLEX like writing entire book or build a full app, use the the `plan_mission` tool to build a plan and **DOT NOT** delegate any other task.\n",
                # "**IMPORTANT**: When you recieve a plan execution use the `execute_mission` tool to execute the plan.",
            ],
            llm=llm,
            storage=storage,
            team=[python_assistant, writer_assistant, research_assistant],#, planer_agent],
            show_tool_calls=False,
            knowledge_base=knowledge_base,
            # tool_calls=True,  # Enable function calls for searching knowledge base and chat history
            # use_tools=True,
            # show_tool_calls=True,
            # search_knowledge=True,
            tools=[FileTools(working_dir), delay_calls, plan_mission], # execute_mission],
            debug_mode=debug_mode
        )

def parse_value(value):
    """Convert string values to appropriate types."""
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    elif value.isdigit():
        return int(value)
    elif value.replace('.', '', 1).isdigit():
        return float(value)
    return value

def parse_args(args):
    if len(args) < 1:
        # print("Error: No prompt provided")
        # sys.exit(1)
        return None, {}
    prompt = args[0]
    kwargs = {}
    for arg in args[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            kwargs[key] = parse_value(value)
        else:
            print(f"Warning: Argument '{arg}' is not in the format key=value and will be ignored")

    return prompt, kwargs

# command line arguments:
prompt, args = parse_args(sys.argv[1:])
answer = None
if prompt is None:
    answer = agent.run('What is happening now in Syria?', stream=False)
else:
    answer = agent.run(prompt, **args)
    if (args.get('stream', True)):
        for message in answer:
            print(message, end='')
        sys.exit(0)

print(answer)
