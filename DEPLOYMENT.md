# PythonAnywhere Deployment Guide

## Prerequisites
- PythonAnywhere account (free tier works)
- Your config.json with API credentials

## Step 1: Upload Files

1. Go to https://www.pythonanywhere.com/user/AkDavid19/
2. Click "Files" tab
3. Create directory: `/home/AkDavid19/bot_poster`
4. Upload these files:
   - bot.py
   - ai_content_generator.py
   - scheduler.py
   - config.json
   - requirements.txt

## Step 2: Install Dependencies

1. Click "Consoles" tab
2. Start a Bash console
3. Run:
```bash
cd ~/bot_poster
pip install --user -r requirements.txt
```

## Step 3: Test the Bot

```bash
cd ~/bot_poster
python bot.py
```

If it works, you'll see generated posts.

## Step 4: Setup Scheduled Task (FREE TIER)

**IMPORTANT:** Free tier only allows 1 scheduled task that runs ONCE and exits.
The `schedule` library with `while True` loop will NOT work - it gets killed after timeout.

**Solution:** Use `daily_post.py` that runs once per execution.

1. Click "Tasks" tab
2. Create a new scheduled task
3. Set time: `08:00` UTC (= 09:00 WAT)
4. Command: `python3 /home/AkDavid19/bot_poster/daily_post.py`

This posts once per day at your chosen time.

## Step 5: For Multiple Daily Posts (PAID TIER ONLY)

If you upgrade to Hacker plan ($5/mo):

1. Click "Tasks" tab
2. Create multiple scheduled tasks:
   - `06:30 UTC` → `python3 ~/bot_poster/bot.py --post` (engagement)
   - `11:00 UTC` → `python3 ~/bot_poster/bot.py --post` (thread)
   - `17:30 UTC` → `python3 ~/bot_poster/bot.py --post` (learning)

OR use "Always-on task" to run scheduler.py continuously

## Environment Variables (Recommended)

Instead of config.json, use environment variables:

1. Go to "Files" → "Edit .bashrc"
2. Add:
```bash
export TWITTER_API_KEY="your_key"
export TWITTER_API_SECRET="your_secret"
# ... etc
```

3. Update bot.py to read from os.environ

## Troubleshooting

**Import errors:**
```bash
pip install --user google-generativeai requests requests-oauthlib schedule
```

**Permission errors:**
```bash
chmod +x scheduler.py
```

**Timezone issues:**
PythonAnywhere uses UTC. Adjust your schedule times accordingly.
WAT = UTC+1, so 07:30 WAT = 06:30 UTC

## Free Tier Limitations

- ❌ 1 scheduled task only (1 post per day max)
- ❌ No always-on tasks (scheduler.py won't work)
- ❌ Tasks timeout after ~5-10 minutes
- ❌ `while True` loops get killed

**Free Tier Reality:** You can only post once per day automatically.

**Paid Tier ($5/mo) Benefits:**
- ✅ Multiple scheduled tasks (8 posts per week)
- ✅ Always-on tasks (run scheduler.py 24/7)
- ✅ No timeouts
- ✅ Full automation
