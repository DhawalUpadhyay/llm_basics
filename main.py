import os
from urllib import response
from urllib import response
from dotenv import load_dotenv
from scraper import fetch_website_contents
from openai import OpenAI

# content = fetch_website_contents("https://hairscope.ai/")
# print(content)

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""

def messages_for(website):
    content = fetch_website_contents(website)
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + content}
    ]

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # can be anything
)

def summarize(url):
    response = client.chat.completions.create(
        model="llama3.2",
        messages=messages_for(url)
    )
    return response.choices[0].message.content

print(summarize("https://hairscope.ai/"))