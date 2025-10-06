# Deploy to Render.com (Free 24/7 Hosting)

## Why Render?
- ✅ 750 hours/month free (enough for 24/7 bot)
- ✅ No credit card required
- ✅ Auto-restarts if crash
- ✅ Deploy from GitHub in 2 minutes
- ✅ Perfect for your 24 posts/week schedule

## Step 1: Push to GitHub

1. Create a new GitHub repository
2. Push your code:
```bash
cd C:\Users\akdav\Desktop\bot_poster
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/bot_poster.git
git push -u origin main
```

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (free)
3. Authorize Render to access your repos

## Step 3: Deploy Background Worker

1. Click "New +" → "Background Worker"
2. Connect your `bot_poster` repository
3. Configure:
   - **Name:** social-media-bot
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python scheduler.py`
   - **Instance Type:** Free

## Step 4: Add Environment Variables

Click "Environment" tab and add these:

```
TWITTER_API_KEY = z4Pzk3g5bRfcg1zSGTFOLaZV4
TWITTER_API_SECRET = f86X9lQ1ebagK0FRInZWocyPBG63hiadLIJN9EMiNpQeY5zDd5
TWITTER_ACCESS_TOKEN = 1618354708896223232-SHsDVsGizT2N0pr6iuuQ2Qq4WwEI2v
TWITTER_ACCESS_TOKEN_SECRET = k0FGMxl1a65KSvxymwS86pQsuJsD38apgkzew1Y3BZ8vP
TWITTER_BEARER_TOKEN = AAAAAAAAAAAAAAAAAAAAAOXNzwEAAAAAv%2FFs7mVa0ouKWn3nX5GkDHcfdao%3DCXzNJa2srhhGdRuuJA0i4vpBd90jKawtlZ9jLWgjfYVWogQWla
LINKEDIN_ACCESS_TOKEN = AQUo4zSoc8cS-S5gyLzmv4gjkj9MALFLPTEFPHAnfNURbGFDjJvJFjpuSAMKm2X_RjIh7yKcc-o72SX0ocesb_5YI1-mqjfacxebtOAaAo8qe3SiUrDrIvur2ABj1P8nIBYP-z0Lvke8H_3XU4FKwbYnXN3ZqlBOHaGN9glrwaUV1YU5-WG0yG4SbH2SpHjp_dRwxVq8vYJ0mNb8QSUlPftxIPZyJ9Fq40hSdKM9yONFNCaW4fx9skSTTcZA3QG3zQ0tcWCoCLXcQ1XMyQttEEGrGmzBqjcNwRAjUw51vRsLf1TnmO4_aQJCD4TbGvOw-PFpbT6_PbeYE2OOrzfa4UcQiKCCvA
LINKEDIN_PERSON_ID = 1370602947
GEMINI_API_KEY = AIzaSyDvvzLZ1AGeMrWBfPZUt4mgI-svbP7X03k
```

## Step 5: Deploy

1. Click "Create Background Worker"
2. Wait 2-3 minutes for build
3. Check logs - you should see:
   ```
   🤖 Scheduler started - 24 posts per week (3-4 per day)
   📅 Schedule (WAT - West Africa Time):
   ...
   ```

## Step 6: Monitor

- **Logs:** Click "Logs" tab to see posts in real-time
- **Metrics:** Check "Metrics" for uptime
- **Manual Deploy:** Click "Manual Deploy" to restart

## Troubleshooting

**Bot sleeps after 15 min:**
Render free tier may sleep. Solution:
1. Go to https://cron-job.org (free)
2. Create account
3. Add job: Ping `https://social-media-bot.onrender.com` every 10 minutes
4. This keeps bot awake

**Import errors:**
Check logs. If missing packages, add to `requirements.txt` and redeploy.

**Wrong timezone:**
Scheduler uses system time. Times in config are WAT (UTC+1).

## Cost

- **Free tier:** 750 hours/month
- **Your usage:** 720 hours/month (24/7)
- **Remaining:** 30 hours buffer
- **Cost:** $0/month ✅

## Upgrade (Optional)

If you need more reliability:
- **Starter plan:** $7/month
- No sleep mode
- Better performance
- Priority support

## Alternative: Keep Running Locally

If you prefer, just run on your PC:
```bash
python scheduler.py
```
Keep terminal open 24/7. Bot posts automatically.
