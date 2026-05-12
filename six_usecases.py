import json

with open('data/cards.json') as f:
    cards = json.load(f)

for card in cards:
    use_cases = card["use_cases"]
    
    if isinstance(use_cases["when_to_use"], str):
        use_cases["when_to_use"] = [use_cases["when_to_use"]]
    
    if isinstance(use_cases["when_to_avoid"], str):
        use_cases["when_to_avoid"] = [use_cases["when_to_avoid"]]
    
    if isinstance(use_cases["max_savings_tip"], list):
        use_cases["max_savings_tip"] = use_cases["max_savings_tip"][0]

with open('data/cards.json', 'w') as f:
    json.dump(cards, f, indent=2)

print(f"✅ Fixed {len(cards)} cards successfully")