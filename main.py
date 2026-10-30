import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq

load_dotenv(override=True)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fine for a test only
    allow_methods=["*"],
    allow_headers=["*"],
)

client = Groq(api_key=os.environ["GROQ_API_KEY"])
MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/test")
def test():
    @app.get("/test")
def test():
    url = "https://api.open-meteo.com/v1/forecast?latitude=23.34&longitude=85.31&current=temperature_2m,wind_speed_10m,weather_code"
    resp = requests.get(url, timeout=10)
    data = resp.json()
    if resp.status_code != 200 or "current" not in data:
        return {"weather_error": resp.status_code, "details": data}
    weather = data["current"]
    r = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": f"Describe this weather in one friendly sentence: {weather}"}],
    )
    return {"weather": weather, "ai": r.choices[0].message.content}