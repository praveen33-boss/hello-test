import os
import requests
from dotenv import load_dotenv
from groq import Groq

load_dotenv(override=True)

# Part 1: ask the LLM something
client = Groq(api_key=os.environ["GROQ_API_KEY"])
resp = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[{"role": "user", "content": "Say hello in one short sentence."}],
)
print("LLM says:", resp.choices[0].message.content)

# Part 2: get live weather from a free public API (no key needed)
url = "https://api.open-meteo.com/v1/forecast?latitude=23.34&longitude=85.31&current_weather=true"
data = requests.get(url, timeout=10).json()
print("Live weather in Ranchi:", data["current_weather"])