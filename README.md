# AI-Powered Social Media Autoposting Bot

An intelligent bot that uses Gemini AI to generate and autopost authentic content to X (Twitter) and LinkedIn with smart content pillar rotation.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get API Credentials:**

   **For X (Twitter):**
   - Go to https://developer.twitter.com/en/portal/dashboard
   - Create a new app and get your API keys
   - Enable OAuth 1.0a with Read and Write permissions
   - Get: API Key, API Secret, Access Token, Access Token Secret, Bearer Token

   **For LinkedIn:**
   - Go to https://www.linkedin.com/developers/apps
   - Create a new app
   - Request access to "Share on LinkedIn" and "Sign In with LinkedIn" products
   - Get your Access Token (use OAuth 2.0 flow)
   - Get your Person ID from: https://api.linkedin.com/v2/me

3. **Configure credentials:**
   - Edit `config.json` and add your API credentials

## Usage

**Generate and post AI content:**
```bash
python bot.py
```

**Custom pillar or context:**
```python
from bot import SocialMediaBot

bot = SocialMediaBot()
bot.ai_post(pillar='build_in_public', custom_context='Just hit 1000 users')
```

**Run automated scheduler:**
```bash
python scheduler.py
```

The bot intelligently rotates through content pillars:
- 30% Build-in-public updates
- 20% Tech insights
- 20% Personal journey
- 20% Motivation
- 10% Engagement baits

**Test AI generation only:**
```bash
python ai_content_generator.py
```

## Security Note

- Never commit `config.json` with real credentials
- Add `config.json` to `.gitignore`
- Consider using environment variables for production
