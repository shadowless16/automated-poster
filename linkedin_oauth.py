import requests
import json
from urllib.parse import urlencode

print("\n=== LinkedIn OAuth Helper ===\n")

# For many apps, requesting r_liteprofile or openid requires the "Sign In with LinkedIn"
# product to be enabled. If your app doesn't have Sign-In, request only the
# posting scope w_member_social. Since the access token is used primarily for
# posting and you already have a person_id in config.json, we request only
# w_member_social by default.

client_id = input("Enter your LinkedIn Client ID: ").strip()
redirect_uri = "http://localhost:8000/callback"

# Step 1: Authorization URL (no client_secret needed yet)
params = {
    'response_type': 'code',
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': 'openid profile w_member_social'
}

auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"

print(f"\n1. Open this URL in your browser:\n{auth_url}\n")
print("2. Authorize the app")
print("3. Copy the 'code' parameter from the redirect URL\n")

code = input("Enter the authorization code: ").strip()

# Step 2: Exchange code for token (now we need client_secret)
client_secret = input("Enter your LinkedIn Client Secret (will not be shown): ").strip()
token_url = "https://www.linkedin.com/oauth/v2/accessToken"
token_data = {
    'grant_type': 'authorization_code',
    'code': code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret
}

response = requests.post(token_url, data=token_data)

if response.status_code == 200:
    token_info = response.json()
    access_token = token_info.get('access_token')
    if not access_token:
        print("\n✗ No access token received:", token_info)
    else:
        print(f"\n✓ Access Token obtained. (token length: {len(access_token)})\n")

        # Update config
        with open('config.json', 'r') as f:
            config = json.load(f)

        config.setdefault('linkedin', {})['access_token'] = access_token

        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)

        print("✓ Config updated! You can now run the bot with: python bot.py --post\n")
else:
    try:
        print(f"\n✗ Error ({response.status_code}): {response.text}")
    except Exception:
        print("\n✗ Unknown error while exchanging code for token.")
