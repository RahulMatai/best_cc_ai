import json
import pandas as pd
from groq import Groq
from dotenv import load_dotenv
from data_processor import (
    load_cards, extract_card_data, extract_exclusions_data,
    extract_quick_report, add_premium_flag, fix_percentages,
    generate_use_cases, FIX_MAP
)
import os
import time

load_dotenv()

BAD_CARDS = [
    "AU Spont", "AU Xcite ultra", "Kotak IndiGo 6E Rewards XL",
    "ICICI AMAZON PAY", "SBI Air india Signature", "HSBC TravelOne"
]

# Load all sheets
df_main, df_quick, df_sheet1 = load_cards()

# Load existing cards.json
with open('data/cards.json') as f:
    cards = json.load(f)

# Reprocess only bad cards
for card_name in BAD_CARDS:
    print(f"Reprocessing: {card_name}")
    card_data = extract_card_data(df_main, card_name)
    if card_data is None:
        print(f"⚠️ Not found: {card_name}")
        continue
    exclusions = extract_exclusions_data(df_sheet1, card_name)
    quick = extract_quick_report(df_quick, card_name)
    card_data.update(exclusions)
    card_data.update(quick)
    card_data = add_premium_flag(card_data)
    card_data = fix_percentages(card_data)
    use_cases = generate_use_cases(card_data)
    card_data["use_cases"] = use_cases

    # Replace in cards list
    for i, c in enumerate(cards):
        if c["card_name"] == card_name:
            cards[i] = card_data
            break

    with open('data/cards.json', 'w') as f:
        json.dump(cards, f, indent=2)
    print(f"✅ Fixed: {card_name}")
    time.sleep(2)

print("\n✅ All done!")