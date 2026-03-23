import os, sys, subprocess, random, time, json
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
from phi.tools.spider import SpiderTools
from phi.tools.website import WebsiteTools
from phi.storage.assistant.sqllite import SqlAssistantStorage
from phi.vectordb.chroma import ChromaDb
from plan_schema import Task, MissionPlan
from dataclass_wizard import fromdict
import dataclasses

load_dotenv()

db_file = "./ai.db"
cwd = Path(__file__).parent.resolve()
working_dir = cwd.joinpath("working_dir")
if not working_dir.exists():
    working_dir.mkdir(exist_ok=True, parents=True)

debug_mode = False

# Set up SQL storage for the assistant's data
storage = SqlAssistantStorage(table_name="questions", db_file=db_file)
storage.create()  # Create the storage if it doesn't exist

# Knowledge Base
knowledge_base = JSONKnowledgeBase(
    #urls=["https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    path=f"{working_dir}/data",
    vector_db=ChromaDb(collection="my_knowledge_base01"),
)

# Comment out after first run if: recreate=False
knowledge_base.load(recreate=True)

DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')

llm=OpenAIChat(model=DEFAULT_MODEL, max_tokens=4000, temperature=.5)
llm_classifier=OpenAIChat(model=DEFAULT_MODEL, max_tokens=500, temperature=.2)
llm_planner=OpenAIChat(model=DEFAULT_MODEL, max_tokens=8000, temperature=.2)
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
    tools=[DuckDuckGo(fixed_max_results=5, search=True), SerpApiTools(search_youtube=False)],# search for news with: news=True
    # This setting tells the LLM to format messages in markdown
    add_datetime_to_instructions=True,
    debug_mode=debug_mode,
)

def delay_calls(seconds: int=3) -> str:
    """Use this function to introduce a some delay to avoid throttling.

    Args:
        :param seconds: The number of seconds to delay. Default is 3.
    
    Returns:
        The message of waiting time.
    """
    time.sleep(seconds)
    return 'Waiting for {} seconds...'.format(seconds)


classifier = Assistant(
            description="""You are a AI agent that is capable of classifying any task based on its level of complexity.
            Your goal is to read the user's question or mission and determine if it is a SIMPLE or COMPLEX task according to the provided schema.
            """,
            instructions=[
                "When the user sends a message, first **THINK DEEPLY** and determine if:\n"
                " - It is a QUESTION that you can answer or a SIMPLE task which you can do, then just do it.\n"
                " - It is a COMPLEX task, then you need to provide a plan to do it.\n"
                # " - You need to ask clarifying the question\n",
            ],
            llm=llm_classifier,
            output_model=Task,
            # storage=storage,
            # knowledge_base=knowledge_base,
            debug_mode=debug_mode
        )

planner = Assistant(
            description="""You are a super powerful AI agent that is helpful and capable of managing complex tasks.
            Your goal is to take seriously user's task then break it down into simplest sub-tasks in the best possible way.
            """,
            instructions=[
                "When the user sends a message, first **THINK DEEPLY** and determine if:\n"
                # " - It is a QUESTION that you can answer or a SIMPLE task which you can do, then just do it.\n"
                # " - It is a COMPLEX task, then you need to provide a plan to do it.\n"
                # " - You need to use a tool that is available to you\n"
                " - You need to search the knowledge base before answer any question\n"
                " - You need to ask clarifying the question\n",
                # "If the user asks about a topic which you don't know, then first **ALWAYS** search your knowledge base using the `search_knowledge_base` tool.\n",
                "If you don't find relevant information in your knowledge base delegate the task to 'Research Assistant' to find more information\n",
                # "If the user asks to summarize the conversation or if you need to reference your chat history with the user, use the `get_chat_history` tool.\n",
                "If the users message is unclear, ask clarifying questions to get more information from the user.\n",
                # "Start your response by classifying the task type if it is SIMPLE or COMPLEX.\n",
                # "The plan of the complex should define the name of the agent assigned for each task.\n",
                # "Here is the of available assistant: 'python_assistant', 'writer_assistant', 'research_assistant'.\n",
            ],
            llm=llm_planner,
            output_model=MissionPlan,
            # storage=storage,
            # knowledge_base=knowledge_base,
            # tool_calls=True,  # Enable function calls for searching knowledge base and chat history
            # use_tools=True,
            # show_tool_calls=True,
            # search_knowledge=True,
            # tools=[delay_calls], #, execute_mission],
            debug_mode=debug_mode
        )

agent = Assistant(
            description="""You are a super powerful AI agent that is helpful and capable of managing complex tasks.
            Your goal is to help the user or answer his questions in the best possible way.
            """,
            instructions=[
                "When the user sends a message, first **think** and determine if:\n"
                " - The task is SIMPLE and you can do it, so do not delegate it to any Ai assistant\n"
                " - You can answer the question or do the task, then just do it\n"
                " - You cannot answer the question or you are not able to do the task, then delegate it to an AI assistant\n"
                " - You need to use a tool that is available to you\n"
                " - You need to search the knowledge base before answer any question\n"
                " - You need to delegate the task to a team member assistant\n"
                " - You need to ask clarifying the question\n",
                "If the user asks about a topic, first **ALWAYS** search your knowledge base using the `search_knowledge_base` tool.\n",
                "If the users message is unclear, ask clarifying questions to get more information.\n",
                "Carefully read the information you have gathered from assistants or tools and provide a clear and concise answer to the user.\n",
                "Do not tell the user about what you have to do, just perform your task.\n",
                "Each call to assistant or tool usage will cost a hit to the API endpoint, so make sure to delay calls using the `delay_calls` tool before calling any assistant in order to avoid API throttling.\n"
                "Write every response from assistants into your knowledge base for future reference.\n"
                "You can delegate tasks to an AI Assistant in your team depending of their role and the tools available to them.\n"
            ],
            llm=llm,
            storage=storage,
            team=[python_assistant, writer_assistant, research_assistant],#, planer_agent],  # if you add a "team" you won't be able to use the "output_model"
            show_tool_calls=False,
            # knowledge_base=knowledge_base,
            # tool_calls=True,  # Enable function calls for searching knowledge base and chat history
            # use_tools=True,
            # show_tool_calls=True,
            # search_knowledge=True,
            tools=[FileTools(working_dir), delay_calls], # execute_mission],
            debug_mode=debug_mode
        )

# r = agent.run('5+6=?', stream=False)
# print(r)
# sys.exit(0)

# result = classifier.run('Tell me a joke') # SIMPLE
# result = planner.run('Tell me a joke')
# result = planner.run('5+6=?')
# result = classifier.run('Write a short story') # COMPLEX
# result = planner.run('Write a short story') # COMPLEX
# result = classifier.run('Write a book about SQL.') # COMPLEX
result = planner.run('Write a book about SQL standards.', stream=False) # taskType='COMPLEX'
# result = planner.run('Write a book about Data Science with code examples.', stream=False) # taskType='COMPLEX'
# result = classifier.run('Write a full ebook about Data Science', stream=False) # taskType='COMPLEX'
# result = classifier.run('Build an eCommerce website similar to WooCommerce.', stream=False) # taskType='COMPLEX'
# result = classifier.run('Build a CRM using FastAPI, Vue3 and Bootstrap5.', stream=False) # taskType='COMPLEX'
# result = agent.run('What is happening now in Lebanon?', stream=False) # taskType='COMPLEX' tasks=['Search knowledge base for recent information about Lebanon.', 'If no information is found, consider searching external news sources for updates on the current situation in Lebanon.', 'Provide a summary of the findings to the user.']
# result = agent.run('Tell me a joke', stream=False) # taskType='SIMPLE' tasks=["Here's one: Why couldn't the bicycle stand up by itself? Because it was two-tired."]
# result = agent.run('Build an entire book about Data Science.', stream=True) # taskType='COMPLEX' tasks=['Search the ...
# result = agent.run('Write a book about SQL.', stream=False) # taskType='COMPLEX' tasks=['Determine the scope and target audience ...

def breakdown_task(task: Any):
    print(f"Type of task: {type(task)}.")
    missionPlan = planner.run(task.prompt or task.name, stream=False)
    if isinstance(missionPlan, str):
        missionPlan = fromdict(MissionPlan, json.loads(missionPlan))
        print(f"Mission (str): {missionPlan.title}")
    else:
        print(f"Mission (obj): {missionPlan.title}")

    print(f"Nbr of sub-tasks: {len(missionPlan.tasks)}")
    return missionPlan

def do_simple_task(prompt: str):
    response = agent.run(prompt, stream=False)
    if (response):
        print(response)

def do_mission(plan: MissionPlan):
    tasks = plan.tasks
    i = 0
    for task in tasks:
        i += 1
        print(f"DOING: {i}) {task.name} ({task.taskType})...", end='')
        if task.taskType=='SIMPLE':
            print(f"I will do: {task.description}...")
            # do_simple_task(task.prompt or task.name)
        else:
            print(f"Break it down before: {task.description}")
            # Let's break it down into sub-tasks
            missionPlan = breakdown_task(task)
            do_complex_task(task)

def do_complex_task(task: Task):
    if task.taskType=='SIMPLE':
        print(f"SIMPLE Task: {task.name}")
        # do_simple_task(task.prompt or task.name)
    else:
        print(f"COMPLEX Task: {task.name}")
        # Let's break it down into sub-tasks
        plan = breakdown_task(task)
        do_mission(plan)
    
    print(f"{task.get_prompt()} ({task.taskType}): {task.description}.")

def dump_to_json(obj: str):    
    with open(f"plan_{time.time()}.json", 'w', encoding='utf-8') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4)

print(f"result:{result}\n")
print(f"result type: {type(result)}\n")

if isinstance(result, str):
    try:
        # We may ned to first cast it to Task to see if it's complex, we then need to create a MissionPlan then break it down...
        result = fromdict(MissionPlan, json.loads(result))
        print(f"result becomes: {type(result)}\n")
        dump_to_json(result)
    except Exception as e:
        print(f"ERROR: {e}")
else:
    dump_to_json(dataclasses.asdict(result))

tasks = result.tasks
print(f"len(tasks): {len(tasks)}")

for task in tasks:
    print(f"Task: {task.name}", end='')
    if task.taskType=='SIMPLE':
        print('SIMPLE')
        do_simple_task(task.get_prompt())
    else:
        print('COMPLEX')
        # We need to create a plan
        missionPlan = breakdown_task(task)
        do_mission(missionPlan)


# tasks = []
# prompts = []
# if isinstance(result, str):
#     result = json.loads(result)
#     tasks = result["tasks"]
#     print(f"Mission: {result['title']}")
#     for task in tasks:
#         if task["taskType"]=='SIMPLE':
#             prompts.append(task["prompt"] or task["name"])
# elif isinstance(result, MissionPlan):
#     tasks = result.tasks
#     print(f"Mission: {result.title}")
#     for task in tasks:
#         if task.taskType=='SIMPLE':
#             prompts.append(task.prompt or task.name)

# print(f"len(tasks): {len(tasks)}")
# if len(tasks) == 1:
#     # print(f"Mission: {result.title}")
#     # print(f"Task: {result.tasks[0].name}")
#     # print(f"Description: {result.tasks[0].description}")
#     # print(f"Temperature: {result.tasks[0].temperature}")

#     print(f"prompt: {prompts[0]}")
#     response = agent.run(prompts[0], stream=False)
#     if (response):
#         print(response)
#     else:
#         print('No response!')

#     # if isinstance(result, dict):
#     #     for delta in result:
#     #         print(delta, end="")
#     # else:
#     #     print(result)
# else:
#     i = 0
#     try:
#         for task in tasks:
#             i += 1
#             print(f"{i}) [{task['name']}]: {task['description']}.")
#             print(f"Temperature: {task['temperature']}")
#             print(f"Type: {task['taskType']}")
#             print(f"Tools: {task['requiredTools']}")
#             print(f"Assigned to: {task['assignedAssistant']}")
#             print(f"Prompt: {task['prompt']}")
#             # perform the actual task (need add: temperature, tools, assignedAssistant...)
#             response = agent.run(task['prompt'], stream=False)
#             if (response):
#                 print(response)
#             else:
#                 print('No response!')
#             print()
#     except Exception as e:
#         print(e)
