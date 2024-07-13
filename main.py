import os
import sys
import subprocess
from openai import OpenAI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from phi.assistant import Assistant
from phi.llm.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"],
                base_url=os.environ["OPENAI_BASE_URL"])
SUPPORTED_MODELS = [
    "llama3-70b-8192",
    "mixtral-8x7b-32768",  # largest window context
    "llama3-8b-8192",
    "gemma-7b-it",
    "gemma2-9b-it"
]
MODEL_NAME = SUPPORTED_MODELS[0]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def generate_completion(message: str, use_agents: bool,
                              stream_response: bool):
    answer = None
    if use_agents:
        assistant = Assistant(
            description=
            "You help user finding the best answer to his question.",
            show_tool_calls=False,
            llm=OpenAIChat(model=MODEL_NAME, max_tokens=3000, temperature=0.7),
            tools=[
                DuckDuckGo(),
                YFinanceTools(stock_price=True,
                              analyst_recommendations=True,
                              company_info=True,
                              company_news=True)
            ],
            run_id=None)
        answer = assistant.run(message, stream=False)
    else:
        chat_completion = client.chat.completions.create(
            messages=[{
                "role": "user",
                "content": message,
            }],
            model=MODEL_NAME,
            # temperature=0.7,
            # max_tokens=500,
        )
        print(f"use_agents: {use_agents}, stream_response: {stream_response}")
        answer = chat_completion.choices[0].message.content
    return answer


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/chat")
async def chat_completion(request: Request):
    data = await request.json()
    print(f"Prompt: {data['message']}")
    print(f"****** pass POST: {data}")
    response = await generate_completion(data['message'], data['useAgents'],
                                         data['streamResponse'])
    return response
