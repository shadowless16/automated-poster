# LinkedIn API Setup Guide

## Step 1: Request Product Access

1. Go to: https://www.linkedin.com/developers/apps
2. Click on your app
3. Go to "Products" tab
4. Request access to:
   - **"Share on LinkedIn"** (required for posting)
   - **"Sign In with LinkedIn using OpenID Connect"** (required for auth)
5. Wait for approval (usually instant for personal apps)

## Step 2: Get Access Token

### Option A: Quick Token (Testing)

1. Go to: https://www.linkedin.com/developers/tools/oauth
2. Select your app
3. Check scope: `w_member_social`
4. Click "Request Access Token"
5. Copy token to `config.json`

### Option B: OAuth Flow (Production)

1. Add redirect URL in app settings: `http://localhost:8000/callback`
2. Run: `python linkedin_oauth.py`
3. Follow browser prompts

## Step 3: Test

```bash
python bot.py
```

## Troubleshooting

**Error: "unauthorized_scope_error"**
- Your app needs "Share on LinkedIn" product approved
- Go to Products tab and request access

**Error: "ACCESS_DENIED"**
- Token expired or wrong scope
- Generate new token with `w_member_social` scope
