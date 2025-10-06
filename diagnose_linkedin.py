import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

access_token = config['linkedin']['access_token']

print("\n=== LinkedIn Token Diagnostic ===\n")

# Test 1: Try userinfo endpoint (OpenID)
print("Test 1: GET /v2/userinfo (OpenID)")
headers = {
    'Authorization': f'Bearer {access_token}',
    'X-Restli-Protocol-Version': '2.0.0'
}
response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✓ Sub (ID): {data.get('sub')}")
    print(f"✓ Name: {data.get('name')}")
    print(f"✓ Email: {data.get('email')}")
else:
    print(f"✗ Error: {response.text}\n")

# Test 2: Try to get profile with r_liteprofile
print("\nTest 2: GET /v2/me (requires r_liteprofile)")
response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"✓ Your ID: {data.get('id')}")
    print(f"✓ Name: {data.get('localizedFirstName')} {data.get('localizedLastName')}")
else:
    print(f"✗ Error: {response.text}\n")

# Test 3: Introspect token
print("\nTest 3: Token introspection")
print(f"Token length: {len(access_token)}")
print(f"Token starts with: {access_token[:20]}...")
print(f"Configured person_id: {config['linkedin']['person_id']}")

print("\n=== Recommendation ===")
print("If all tests fail, your token doesn't have the right scopes.")
print("You need to regenerate with BOTH 'r_liteprofile' AND 'w_member_social'")
print("OR use 'openid' + 'w_member_social' scopes together.\n")
