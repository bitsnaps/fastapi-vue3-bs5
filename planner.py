import os, json
from dotenv import load_dotenv
#from phi.assistant import Assistant
from phi.agent import Agent, RunResponse
#from phi.llm.openai import OpenAIChat
from phi.model.groq import Groq # pip install groq
from plan_schema import MissionPlan
from dataclass_wizard import fromdict

load_dotenv()


DEFAULT_MODEL = os.getenv('DEFAULT_MODEL')

# Old API
#llm=OpenAIChat(model=DEFAULT_MODEL, max_tokens=8000, temperature=0)

llm=Groq(id=DEFAULT_MODEL, max_tokens=4000, temperature=0.1)

# class Character(BaseModel):
#     name: str = Field(..., description="Name of the character")
#     role: str = Field(..., description="Role of the character in the movie")

# class MovieScript(BaseModel):
#     setting: str = Field(..., description="Provide a nice setting for a blockbuster movie.")
#     ending: str = Field(..., description="Ending of the movie. If not available, provide a happy ending.")
#     genre: str = Field(..., description="Genre of the movie. If not available, select action, thriller or romantic comedy.")
#     name: str = Field(..., description="Give a name to this movie")
#     characters: List[Character] = Field(..., description="List of characters for this movie.")
#     storyline: str = Field(..., description="3 sentence storyline for the movie. Make it exciting!")


# movie_assistant = Assistant(
#     description="You help write movie scripts.",
#     output_model=MovieScript,
#     llm=llm
# )

# result = movie_assistant.run("New York")


project_agent = Agent(
    name="Planner Agent",
    role="Create a well structured plan to complete a given mission in well formatted output break it down by tasks.",
    description="You help write a plan for any given mission.",
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
    #output_model=MissionPlan,
    response_model=MissionPlan,
    model=llm,
    #add_datetime_to_instructions=True
)

response: RunResponse = project_agent.run("Write a book about SQL") # not every time ends with MissionPlan type


# response = project_Agent.run("Create an ERP system.")
# response = project_Agent.run("Write a book about Data Science")
# response = project_Agent.run("Write a book about Machine Learning")
# response = project_Agent.run("Create an eCommerce platform")


result = response.content
# Check if "result" is a valid JSON
def is_valid_json(json_str):
    try:
        return json.loads(str(json_str))
    except json.JSONDecodeError:
        return False

result = is_valid_json(result)
if result:
    print(result)

print(f"result type: {type(result)}")

is_typed = isinstance(result, MissionPlan)
print(f"is Mission Typed?: {is_typed}") # should be True

if not is_typed:
    result = fromdict(MissionPlan, str(result))

print("\n")

i = 0
try:
    print(f"Mission: {result.title}")
    for task in result.tasks:
        i += 1
        print(f"{i}) [{task.name}]: {task.description}.")
        print(f"Temperature: {task.temperature}")
        print(f"Type: {task.taskType}")
        print(f"Tools: {task.requiredTools}")
        print(f"Assigned to: {task.assignedAssistant}")
        print(f"Prompt: {task.prompt}")
        print()
except Exception as e:
    print(e)

