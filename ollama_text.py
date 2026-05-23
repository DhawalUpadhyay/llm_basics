import os
from dotenv import load_dotenv
# from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # can be anything
)
message = "Hello, GPT! This is my first ever message to you! Hi!"

messages = [{"role": "user", "content": message}]


response = client.chat.completions.create(
    model="llama3.2",
    messages=messages
)

print(response.choices[0].message.content)
