from typing import List, Optional
from pydantic import BaseModel, Field
from phi.utils.enum import ExtendedEnum
from dataclasses import dataclass

# Youn can grab the list of values from: TaskType.values_list()
class TaskType(str, ExtendedEnum):
    SIMPLE = "SIMPLE"
    COMPLEX = "COMPLEX"

# Youn can grab the list of values from: AssistantType.values_list()
class AssistantType(str, ExtendedEnum):
    PYTHON = "Python Assistant"
    WEB = "Web Assistant"
    WRITER = "Writer Assistant"
    RESEARCHER = "Research Assistant"

# Youn can grab the list of values from: RequiredTool.values_list()
class RequiredTool(str, ExtendedEnum):
    DUCKDUCKGO = "DuckDuckGo"
    SERPAPI = "SerpApi"
    YAHOOFINANCE = "YahooFinance"
    PYTHONCODING = "PythonCoding"
    SHELLEXECUTION = "ShellExecution"
    FILEIO = "FileIO"
    SPIDER = "SpiderScraper"
    WEBSITE = "WebsiteParser"

@dataclass
class Task(BaseModel):
    name: str = Field(..., description="Name of the task")
    description: str = Field(..., description="Description of the task")
    # taskType: str = Field(..., description="The type of task is either SIMPLE or COMPLEX")
    taskType: TaskType = Field(..., description=f"The type of task is either {TaskType.values_list()}")
    assignedAssistant: AssistantType = Field(..., description=f"The AI assistant assigned to do this task from this list: {AssistantType.values_list()}")
    prompt: str = Field(..., description="The prompt for the AI assistant to be use for this task with step by step detailed instructions.")
    # requiredTools: str = Field(..., description="The tools required to do this task from this list: DuckDuckGo, SerpApi, YahooFinance, PythonCoding, ShellExecution, FileIO")
    requiredTools: Optional[List[RequiredTool]] = Field(..., description=f"The tools required by the AI assitant to do this task from this list: {RequiredTool.values_list()}")
    temperature: str = Field(..., description="The best float value required for the LLM in order to do this task")

    def get_prompt(self):
        return self.prompt or self.name

@dataclass
class MissionPlan(BaseModel):
    title: str = Field(..., description="Give a title to this mission")
    tasks: List[Task] = Field(..., description="List of tasks to complete this mission")
