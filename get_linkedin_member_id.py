import json

print("\n=== Get LinkedIn Member ID Manually ===\n")
print("Since your app doesn't have 'Sign In with LinkedIn' approved,")
print("you need to get your member ID manually.\n")

print("Method 1: From LinkedIn Profile URL")
print("-" * 50)
print("1. Go to your LinkedIn profile")
print("2. Look at the URL: linkedin.com/in/YOUR-PROFILE-NAME/")
print("3. Your member ID is in the page source or network requests")
print("\nOR use this Chrome extension:")
print("https://chrome.google.com/webstore/detail/linkedin-member-id-finder\n")

print("Method 2: Use LinkedIn API Explorer")
print("-" * 50)
print("1. Go to: https://www.linkedin.com/developers/tools/oauth")
print("2. Request 'r_liteprofile' scope (if available)")
print("3. Use token to call: https://api.linkedin.com/v2/me")
print("4. The 'id' field is your member ID\n")

print("Method 3: Inspect Network Tab")
print("-" * 50)
print("1. Open LinkedIn in browser")
print("2. Open DevTools (F12) → Network tab")
print("3. Post something on LinkedIn")
print("4. Look for 'ugcPosts' request")
print("5. Check the 'author' field in the request payload\n")

member_id = input("Enter your LinkedIn Member ID: ").strip()

if member_id:
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    config['linkedin']['person_id'] = member_id
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\n✓ Saved member ID: {member_id}")
    print("✓ You can now run: python bot.py\n")
else:
    print("\n✗ No ID entered. Try again when you have it.\n")
