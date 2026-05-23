import os
from dotenv import load_dotenv
# from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # can be anything
)

system_message = "You are a helpful assistant named Dhawal. You need to reply rude to any of user query. You need to reply but in a rude way."

history = [{"role": "system", "content": system_message}]

def messages_for(user_input):
    history.append({"role": "user", "content": user_input})
    return history

user_input = input("You: ")
while user_input.lower() not in ["exit", "quit"]:
    response = client.chat.completions.create(
        model="llama3.2",
        messages=messages_for(user_input)
    )
    response_message = response.choices[0].message.content
    history.append({"role": "assistant", "content": response_message})
    print(f"Dhawal: {response_message}")
    user_input = input("You: ")

# response = client.chat.completions.create(
#     model="llama3.2",
#     messages=[
#         {
#             "role": "system",
#             "content": "You are a helpful assistant."
#         },
#         {
#             "role": "user",
#             "content": "Explain FastAPI in simple words."
#         }
#     ]
# )

# print(response.choices[0].message.content)