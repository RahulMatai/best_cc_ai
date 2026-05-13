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

# ── Load all sheets ───────────────────────────────────────────
def load_cards():
    df_main = pd.read_excel(
        "data/847834961-CCR.xlsx",
        sheet_name="Credit Card Database",
        header=None
    )
    df_quick = pd.read_excel(
        "data/847834961-CCR.xlsx",
        sheet_name="Quick Report",
        header=None
    )
    df_sheet1 = pd.read_excel(
        "data/847834961-CCR.xlsx",
        sheet_name="Sheet1",
        header=None
    )
    return df_main, df_quick, df_sheet1

# ── Get clean card names ──────────────────────────────────────
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

# ── Extract from Credit Card Database sheet ───────────────────
def extract_card_data(df, card_name):
    for i, row in df.iterrows():
        val = row[1]
        if not isinstance(val, str):
            continue
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

# ── Extract from Quick Report sheet ──────────────────────────
def extract_quick_report(df_quick, card_name):
    for i, row in df_quick.iterrows():
        val = row[0]
        if not isinstance(val, str):
            continue
        if val.strip().lower() == card_name.strip().lower():
            return {
                "annual_fee_gst": str(row[1]).strip() if pd.notna(row[1]) else "N/A",
                "fee_waiver_lakh": str(row[2]).strip() if pd.notna(row[2]) else "N/A",
                "base_rate_pct": str(row[3]).strip() if pd.notna(row[3]) else "N/A",
                "travel_pct": str(row[4]).strip() if pd.notna(row[4]) else "N/A",
                "online_specific_pct": str(row[5]).strip() if pd.notna(row[5]) else "N/A",
                "online_pct": str(row[6]).strip() if pd.notna(row[6]) else "N/A",
                "online_txn_pct": str(row[7]).strip() if pd.notna(row[7]) else "N/A",
                "offline_pct": str(row[8]).strip() if pd.notna(row[8]) else "N/A",
                "utility_pct": str(row[9]).strip() if pd.notna(row[9]) else "N/A",
                "govt_tax_pct": str(row[10]).strip() if pd.notna(row[10]) else "N/A",
                "rent_pct": str(row[11]).strip() if pd.notna(row[11]) else "N/A",
                "wallet_pct": str(row[12]).strip() if pd.notna(row[12]) else "N/A",
                "education_pct": str(row[13]).strip() if pd.notna(row[13]) else "N/A",
                "insurance_pct": str(row[14]).strip() if pd.notna(row[14]) else "N/A",
                "fuel_pct": str(row[16]).strip() if pd.notna(row[16]) else "N/A",
                "dining_pct": str(row[17]).strip() if pd.notna(row[17]) else "N/A",
                "grocery_offline_pct": str(row[18]).strip() if pd.notna(row[18]) else "N/A",
                "grocery_online_pct": str(row[19]).strip() if pd.notna(row[19]) else "N/A",
                "upi_pct": str(row[20]).strip() if pd.notna(row[20]) else "N/A",
                "intl_offline_pct": str(row[21]).strip() if pd.notna(row[21]) else "N/A",
                "intl_online_pct": str(row[22]).strip() if pd.notna(row[22]) else "N/A",
                "forex_markup_pct": str(row[23]).strip() if pd.notna(row[23]) else "N/A",
                "lounge_domestic_qtr": str(row[24]).strip() if pd.notna(row[24]) else "0",
                "lounge_intl_yr": str(row[25]).strip() if pd.notna(row[25]) else "0",
                "lounge_railway_qtr": str(row[26]).strip() if pd.notna(row[26]) else "0",
            }
    return {}

# ── Extract from Sheet1 (exclusions) ─────────────────────────
def extract_exclusions_data(df_sheet1, card_name):
    reverse_fix = {v: k for k, v in FIX_MAP.items()}
    original_name = reverse_fix.get(card_name, card_name)
    for i, row in df_sheet1.iterrows():
        val = row[1]
        if not isinstance(val, str):
            continue
        if val.strip() == original_name or val.strip() == card_name:
            return {
                "excluded_categories": str(row[2]).strip() if pd.notna(row[2]) else "N/A",
                "annual_fee_waiver_note": str(row[3]).strip() if pd.notna(row[3]) else "N/A",
                "other_exclusions": str(row[4]).strip() if pd.notna(row[4]) else "N/A",
                "rent_surcharge": str(row[5]).strip() if pd.notna(row[5]) else "N/A",
                "education_fee": str(row[6]).strip() if pd.notna(row[6]) else "N/A",
                "wallet_load_fee": str(row[7]).strip() if pd.notna(row[7]) else "N/A",
                "utility_fee": str(row[8]).strip() if pd.notna(row[8]) else "N/A",
                "fuel_fee": str(row[9]).strip() if pd.notna(row[9]) else "N/A",
            }
    return {}

# ── Premium flag ──────────────────────────────────────────────
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

def fix_percentages(card_data):
    pct_fields = [
        "base_rate_pct", "travel_pct", "online_specific_pct",
        "online_pct", "online_txn_pct", "offline_pct",
        "utility_pct", "govt_tax_pct", "rent_pct", "wallet_pct",
        "education_pct", "insurance_pct", "fuel_pct", "dining_pct",
        "grocery_offline_pct", "grocery_online_pct", "upi_pct",
        "intl_offline_pct", "intl_online_pct", "forex_markup_pct"
    ]
    for field in pct_fields:
        val = card_data.get(field, "N/A")
        try:
            num = float(val)
            # Values less than 1 are ratios — multiply by 100
            if abs(num) < 1 and num != 0:
                card_data[field] = str(round(num * 100, 2))
        except:
            pass
    return card_data

# ── Groq use cases ────────────────────────────────────────────
def generate_use_cases(card_data):
    prompt = f"""
You are a friendly Indian credit card expert explaining to a regular Indian person
who has zero knowledge about credit cards and just wants to know where to swipe.

Here is COMPLETE data for {card_data['card_name']}:

FEES:
- Annual Fee: ₹{card_data.get('annual_fee', 'N/A')} (incl GST: ₹{card_data.get('annual_fee_gst', 'N/A')})
- Fee Waiver: Spend ₹{card_data.get('fee_waiver_lakh', 'N/A')} Lakh/year to waive fee

REWARD RATES BY CATEGORY:
- Base Rate: {card_data.get('base_rate_pct', 'N/A')}%
- Travel: {card_data.get('travel_pct', 'N/A')}%
- Online Shopping (specific platforms): {card_data.get('online_specific_pct', 'N/A')}%
- Online Shopping (general): {card_data.get('online_pct', 'N/A')}%
- Offline Transactions: {card_data.get('offline_pct', 'N/A')}%
- Food & Dining: {card_data.get('dining_pct', 'N/A')}%
- Grocery Online: {card_data.get('grocery_online_pct', 'N/A')}%
- Grocery Offline: {card_data.get('grocery_offline_pct', 'N/A')}%
- Fuel: {card_data.get('fuel_pct', 'N/A')}%
- Utility Bills: {card_data.get('utility_pct', 'N/A')}%
- UPI: {card_data.get('upi_pct', 'N/A')}%
- Rent: {card_data.get('rent_pct', 'N/A')}%
- Wallet Load: {card_data.get('wallet_pct', 'N/A')}%
- Education: {card_data.get('education_pct', 'N/A')}%
- Govt/Tax: {card_data.get('govt_tax_pct', 'N/A')}%
- International Online: {card_data.get('intl_online_pct', 'N/A')}%
- Forex Markup: {card_data.get('forex_markup_pct', 'N/A')}%

LOUNGE ACCESS:
- Domestic Airport: {card_data.get('lounge_domestic_qtr', '0')} per quarter
- International Airport: {card_data.get('lounge_intl_yr', '0')} per year
- Railway: {card_data.get('lounge_railway_qtr', '0')} per quarter

SURCHARGES & HIDDEN FEES:
- Rent payment surcharge: {card_data.get('rent_surcharge', 'N/A')}
- Fuel transaction fee: {card_data.get('fuel_fee', 'N/A')}
- Wallet load fee: {card_data.get('wallet_load_fee', 'N/A')}
- Utility payment fee: {card_data.get('utility_fee', 'N/A')}
- Education payment fee: {card_data.get('education_fee', 'N/A')}

KEY BENEFITS: {card_data.get('key_benefits', 'N/A')}
REWARD CAPS: {card_data.get('reward_caps', 'N/A')}
EXCLUDED CATEGORIES: {card_data.get('excluded_categories', 'N/A')}
EXPERT COMMENT: {card_data.get('comments', 'N/A')}

Return ONLY this exact JSON:
{{
    "when_to_use": [
        "Platform/Category — X% back = ₹Y saved per ₹1000",
        "Platform/Category — X% back = ₹Y saved per ₹1000",
        "Platform/Category — X% back = ₹Y saved per ₹1000"
    ],
    "when_to_avoid": [
        "Category — 0% back, never swipe here",
        "Category — X% surcharge eats your rewards"
    ],
    "lounge_benefit": "X domestic + Y international lounge visits free per year",
    "annual_math": "If you spend ₹X/month on [top category], you earn ₹Y/month cashback = ₹Z/year. Annual fee is ₹{card_data.get('annual_fee', 'N/A')}. So net saving = ₹(Z minus fee)/year. Use REALISTIC monthly spend of ₹3000-₹10000 for calculations.",
    Use REALISTIC monthly spend of ₹3000-₹10000 for calculations.",
    "hidden_costs": "Watch out for: list key surcharges in plain English",
    "max_savings_tip": "One specific actionable tip under 20 words"
}}

STRICT RULES:
- For SBI Cashback specifically — it works on ALL online merchants 
  without restriction, mention this clearly
- Use realistic monthly spends: ₹3000-10000 for food, 
  ₹5000-15000 for shopping, ₹2000-5000 for groceries
- Never calculate annual savings more than 10x the annual fee 
  for standard cards
- Always mention 3-4 specific platform names in when_to_use
- Each when_to_use MAX 12 words with exact ₹ amount on ₹1000 spend
- Each when_to_avoid MAX 10 words
- annual_math must have real calculated numbers
- hidden_costs must mention actual fees from the data
- If lounge access is 0, say "No lounge access"
- Return ONLY JSON, nothing else
- If any fee is N/A or 0, skip it in hidden_costs entirely
- hidden_costs should only mention fees that actually exist
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(raw)
    except:
        return {
            "when_to_use": [raw],
            "when_to_avoid": ["N/A"],
            "lounge_benefit": "N/A",
            "annual_math": "N/A",
            "hidden_costs": "N/A",
            "max_savings_tip": "N/A"
        }

# ── Process all 99 cards ──────────────────────────────────────
def process_all_cards():
    df_main, df_quick, df_sheet1 = load_cards()
    cards = get_card_names(df_main)
    print(f"Starting to process {len(cards)} cards...")

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
        card_data = extract_card_data(df_main, card_name)
        if card_data is None:
            print(f"⚠️ Skipping {card_name} — not found in Excel")
            continue
        exclusions = extract_exclusions_data(df_sheet1, card_name)
        quick = extract_quick_report(df_quick, card_name)
        card_data.update(exclusions)
        card_data.update(quick)
        card_data = add_premium_flag(card_data)
        use_cases = generate_use_cases(card_data)
        card_data["use_cases"] = use_cases
        processed_cards.append(card_data)
        with open(output_file, "w") as f:
            json.dump(processed_cards, f, indent=2)
        time.sleep(2)
        print(f"✅ Done: {card_name}")

# ── Main ──────────────────────────────────────────────────────
if __name__ == "__main__":
    process_all_cards()