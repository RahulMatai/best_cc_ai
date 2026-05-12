import pandas as pd
import json
import os
from groq import Groq
from dotenv import load_dotenv
import time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SKIP_LIST = [
    "Card Name", "HDFC Core Credit cards", "HDFC Co-Branded Credit cards",
    "HDFC Business Credit cards", "Axis Bank", "AU SF Bank",
    "***updating this block…......***"
]

FIX_MAP = {
    "SBI Cahback": "SBI Cashback",
    "SBI SBI Elite": "SBI Elite",
    "Mayura": "IDFC Mayura",
    "Ashva": "IDFC Ashva",
    "wealth": "IDFC Wealth",
    "Select": "IDFC Select",
    "classic": "IDFC Classic",
    "Millennia": "IDFC Millennia",
    "WOW": "IDFC WOW",
    "SWYP": "IDFC SWYP",
    "Power +": "IDFC Power+",
    "Rupay platinum": "IndusInd Rupay Platinum",
    "EazyDiner Signature": "IndusInd EazyDiner Signature",
    "Pinnacle": "IndusInd Pinnacle",
    "Tiger": "IndusInd Tiger",
    "MARQUEE": "YES Marquee",
    "RESERV": "YES Reserv",
    "Elite +": "YES Elite+",
    "ACE": "YES ACE",
    "Myntra": "Kotak Myntra",
    "IndiGo 6E Rewards XL": "Kotak IndiGo 6E Rewards XL",
    "IndianOil": "Kotak IndianOil",
    "League platinum": "Kotak League Platinum",
    "Zen Signature": "Kotak Zen Signature",
    "Privy league Signature": "Kotak Privy League Signature",
    "white Reserve": "Kotak White Reserve",
    "White": "Kotak White",
    "Celesta": "Federal Celesta",
    "Imperio": "Federal Imperio",
    "Signet": "Federal Signet",
    "World Safari": "RBL World Safari",
    "Shoprite": "RBL Shoprite",
    "IndianOil RBL XTRA": "RBL IndianOil XTRA",
    "HSBC Ptemier": "HSBC Premier",
}

def load_cards():
    df = pd.read_excel(
        "data/847834961-CCR.xlsx",
        sheet_name="Credit Card Database",
        header=None
    )
    return df

def get_card_names(df):
    cards = []
    seen = set()
    for i, row in df.iterrows():
        val = row[1]
        if not isinstance(val, str):
            continue
        val = val.strip()
        if not val or val in SKIP_LIST or len(val) > 60:
            continue
        val = FIX_MAP.get(val, val)
        if val in seen:
            continue
        seen.add(val)
        cards.append(val)
    return cards

def extract_card_data(df, card_name):
    for i, row in df.iterrows():
        val = row[1]
        if not isinstance(val, str):
            continue
        # Apply fix map before comparing
        cleaned = FIX_MAP.get(val.strip(), val.strip())
        if cleaned == card_name:
            return {
                "card_name": card_name,
                "joining_fee": str(row[2]).strip() if pd.notna(row[2]) else "N/A",
                "annual_fee": str(row[3]).strip() if pd.notna(row[3]) else "N/A",
                "fee_waiver": str(row[4]).strip() if pd.notna(row[4]) else "N/A",
                "reward_type": str(row[5]).strip() if pd.notna(row[5]) else "N/A",
                "key_benefits": str(row[6]).strip() if pd.notna(row[6]) else "N/A",
                "reward_caps": str(row[7]).strip() if pd.notna(row[7]) else "N/A",
                "lounge_domestic": str(row[22]).strip() if pd.notna(row[22]) else "N/A",
                "lounge_international": str(row[23]).strip() if pd.notna(row[23]) else "N/A",
                "best_for": str(row[26]).strip() if pd.notna(row[26]) else "N/A",
                "comments": str(row[29]).strip() if pd.notna(row[29]) else "N/A",
            }
    return None

def add_premium_flag(card_data):
    try:
        fee = float(str(card_data["annual_fee"]).replace(",", "").strip())
        if fee == 0:
            card_data["is_premium"] = False
        elif fee <= 2000:
            card_data["is_premium"] = False
        elif fee <= 8000:
            card_data["is_premium"] = True
        else:
            card_data["is_premium"] = "Super Premium"
    except:
        card_data["is_premium"] = False
    return card_data

def generate_use_cases(card_data):
    prompt = f"""
You are an Indian credit card expert helping regular users.

Here is data for {card_data['card_name']} credit card:
- Annual Fee: ₹{card_data['annual_fee']}
- Reward Type: {card_data['reward_type']}
- Key Benefits: {card_data['key_benefits']}
- Reward Caps: {card_data['reward_caps']}
- Best For: {card_data['best_for']}
- Expert Comment: {card_data['comments']}

Write a response in exactly this JSON format:
{{
    "when_to_use": "2-3 specific situations when user should swipe this card",
    "when_to_avoid": "2-3 specific situations when user should NOT use this card",
    "max_savings_tip": "one line tip to get maximum benefit from this card"
}}

Be specific with platform names like Swiggy, Amazon, Zomato etc.
Return only JSON, no explanation.
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    raw = response.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except:
        return {"when_to_use": raw, "when_to_avoid": "N/A", "max_savings_tip": "N/A"}



def process_all_cards():
    df= load_cards()
    cards = get_card_names(df)
    print(f"Starting to process {len(cards)} cards...")
    # Load existing progress if file exists
    output_file = "data/cards.json"
    if os.path.exists(output_file):
        with open(output_file, "r") as f:
            processed_cards = json.load(f)
        already_done = [c["card_name"] for c in processed_cards]
        print(f"Found {len(already_done)} already processed, skipping those...")
    else:
        processed_cards = []
        already_done = []
    for i, card_name in enumerate(cards):
        if card_name in already_done:
            print(f"Skipping {card_name} — already processed")
            continue
        
        print(f"Processing {i+1}/{len(cards)}: {card_name}")
        card_data = extract_card_data(df, card_name)
        card_data = add_premium_flag(card_data)
        use_cases = generate_use_cases(card_data)
        card_data["use_cases"] = use_cases
        processed_cards.append(card_data)
        with open(output_file, "w") as f:
            json.dump(processed_cards, f, indent=2)
            time.sleep(2)
            print(f"✅ Done: {card_name}")


if __name__ == "__main__":
    process_all_cards()