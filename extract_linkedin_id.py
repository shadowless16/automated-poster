import json

print("\n=== Extract LinkedIn Member ID from Network Request ===\n")
print("Since you just posted successfully on LinkedIn:")
print("1. In DevTools Network tab, find any request with 'voyager' or 'graphql'")
print("2. Click on it → Headers tab")
print("3. Look for 'Cookie' header")
print("4. Find 'li_at=' value\n")
print("OR\n")
print("1. Find the POST request you just made")
print("2. Go to Payload/Request tab")
print("3. Copy the entire JSON payload here\n")

print("Paste the request payload (or just the author URN):")
payload = input("> ").strip()

# Try to extract member ID
member_id = None

if "urn:li:person:" in payload or "urn:li:member:" in payload:
    # Extract from URN
    if "urn:li:person:" in payload:
        start = payload.find("urn:li:person:") + 14
        end = payload.find('"', start) if '"' in payload[start:] else len(payload)
        member_id = payload[start:end].split(',')[0].split('}')[0].strip()
    elif "urn:li:member:" in payload:
        start = payload.find("urn:li:member:") + 14
        end = payload.find('"', start) if '"' in payload[start:] else len(payload)
        member_id = payload[start:end].split(',')[0].split('}')[0].strip()

if member_id:
    print(f"\n✓ Found Member ID: {member_id}\n")
    
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    config['linkedin']['person_id'] = member_id
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✓ Saved to config.json!")
    print("✓ Run: python bot.py\n")
else:
    print("\n✗ Could not extract ID. Try this:")
    print("   Right-click on your LinkedIn profile photo → Inspect")
    print("   Look for data-member-id or similar attribute\n")
