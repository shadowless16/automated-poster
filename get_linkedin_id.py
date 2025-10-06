import requests
import json

# Quick script to get your LinkedIn Person ID

with open('config.json', 'r') as f:
    config = json.load(f)

access_token = config['linkedin']['access_token']

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

response = requests.get('https://api.linkedin.com/v2/me', headers=headers)

if response.status_code == 200:
    data = response.json()
    person_id = data.get('id')
    print(f"\n✓ Your LinkedIn Person ID: {person_id}\n")
    print("Add this to config.json under linkedin.person_id")
    
    # Auto-update config
    config['linkedin']['person_id'] = person_id
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    print("✓ Config updated automatically!\n")
else:
    print(f"✗ Error: {response.status_code}")
    print(response.text)
