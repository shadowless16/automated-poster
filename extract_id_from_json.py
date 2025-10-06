import json

# Your member ID from the successful post
member_id = "1370602947"

# Update config
with open('config.json', 'r') as f:
    config = json.load(f)

config['linkedin']['person_id'] = member_id

with open('config.json', 'w') as f:
    json.dump(config, f, indent=2)

print(f"\n✓ LinkedIn Person ID set to: {member_id}")
print("✓ Config updated successfully!")
print("\nYou can now run: python bot.py\n")
