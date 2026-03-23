from g4f.client import Client

client = Client()
response = client.chat.completions.create(
    # model="gpt-3.5-turbo",
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)
print(response.choices[0].message.content)

# Chat UI
# from g4f.gui import run_gui
# run_gui()

# Inference API
# from g4f.api import run_api
# run_api()

# Usage from OpenAI API
# from openai import OpenAI

# client = OpenAI(
#     api_key="",
#     # Change the API base URL to the local interference API
#     base_url="http://localhost:1337/v1"  
# )

# response = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     # model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "write a poem about a tree"}],
#     stream=False
# )

# if isinstance(response, dict):
#     # Not streaming
#     print(response.choices[0].message.content)
# else:
#     # Streaming
#     for token in response:
#         content = token.choices[0].delta.content
#         if content is not None:
#             print(content, end="", flush=True)


# Usage with request library
# import requests

# url = "http://0.0.0.0:1337/v1/chat/completions"
# body = {
#     "model": "gpt-3.5-turbo", 
#     "stream": False,
#     "messages": [
#         {"role": "assistant", "content": "What can you do?"}
#     ]
# }

# json_response = requests.post(url, json=body).json().get('choices', [])

# for choice in json_response:
#     print(choice.get('message', {}).get('content', ''))
# print('done.')