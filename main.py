import os
from openai import OpenAI
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

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


async def generate_completion(prompt: str):
    chat_completion = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": prompt,
        }],
        model=MODEL_NAME,
        # temperature=0.7,
        # max_tokens=500,
    )

    return chat_completion.choices[0].message.content


@app.get("/")
async def root():
    return {"message": "hello"}


@app.post("/chat")
async def chat_completion(request: Request):
    data = await request.json()
    print(f"Prompt: {data['message']}")
    print(f"****** pass POST: {data}")
    response = await generate_completion(data['message'])
    return response
