from fastapi import FastAPI
from pydantic import BaseModel
import json
import os
from groq import Groq
from dotenv import load_dotenv
import uvicorn

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def load_cards():
    with open("data/cards.json") as f:
        return json.load(f)

# GET all cards
@app.get("/cards")
def get_cards():
    return load_cards()

# GET single card
@app.get("/cards/{card_name}")
def get_card(card_name: str):
    cards = load_cards()
    for card in cards:
        if card["card_name"].lower() == card_name.lower():
            return card
    return {"error": "Card not found"}

# GET recommend by category
@app.get("/recommend/{category}")
def recommend(category: str):
    cards = load_cards()
    relevant = [c for c in cards if category.lower() in c.get("best_for", "").lower()]
    return relevant

# POST chat
class ChatRequest(BaseModel):
    question: str
    cards: list[str]

@app.post("/chat")
def chat(request: ChatRequest):
    all_cards = load_cards()
    user_cards = [c for c in all_cards if c["card_name"] in request.cards]
    
    context = json.dumps(user_cards, indent=2)
    
    prompt = f"""
You are an Indian credit card expert.
User has these cards: {context}
User question: {request.question}
Give a specific, actionable answer in 3-4 lines.
Tell them exactly which card to use and why.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return {"answer": response.choices[0].message.content.strip()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)