"""
Flask web server that runs scheduler in background thread.
Keeps Render.com free tier awake by responding to HTTP pings.
"""
from flask import Flask, jsonify
import threading
import schedule
import time
from bot import SocialMediaBot
from ai_content_generator import AIContentGenerator

app = Flask(__name__)
bot = SocialMediaBot()
ai_gen = AIContentGenerator()

def post_content(pillar, platform):
    """Generate and post content"""
    try:
        print(f"\n⏰ Posting at {time.strftime('%H:%M')} WAT")
        if platform == 'twitter':
            content, _ = ai_gen.generate_post(pillar=pillar, platform='twitter')
            print(f"[{pillar.upper()}] X POST: {content[:50]}...")
            bot.post_to_twitter(content)
        elif platform == 'linkedin':
            content, _ = ai_gen.generate_post(pillar=pillar, platform='linkedin')
            print(f"[{pillar.upper()}] LINKEDIN POST: {content[:50]}...")
            bot.post_to_linkedin(content)
        elif platform == 'both':
            content, _ = ai_gen.generate_post(pillar=pillar, platform='both')
            bot.post_to_twitter(content['twitter'])
            bot.post_to_linkedin(content['linkedin'])
    except Exception as e:
        print(f"Error posting: {e}")

# Schedule all posts (24 per week)
schedule.every().monday.at("07:30").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().monday.at("12:00").do(lambda: post_content('learning_journey', 'twitter'))
schedule.every().monday.at("16:00").do(lambda: post_content('build_in_public', 'twitter'))
schedule.every().monday.at("19:00").do(lambda: post_content('learning_journey', 'linkedin'))

schedule.every().tuesday.at("08:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().tuesday.at("13:00").do(lambda: post_content('real_talk', 'twitter'))
schedule.every().tuesday.at("17:30").do(lambda: post_content('build_in_public', 'twitter'))

schedule.every().wednesday.at("07:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().wednesday.at("12:00").do(lambda: post_content('tech_threads', 'twitter'))
schedule.every().wednesday.at("16:30").do(lambda: post_content('learning_journey', 'twitter'))
schedule.every().wednesday.at("19:00").do(lambda: post_content('build_in_public', 'linkedin'))

schedule.every().thursday.at("07:30").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().thursday.at("11:30").do(lambda: post_content('learning_journey', 'twitter'))
schedule.every().thursday.at("15:00").do(lambda: post_content('real_talk', 'twitter'))
schedule.every().thursday.at("18:30").do(lambda: post_content('learning_journey', 'linkedin'))

schedule.every().friday.at("08:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().friday.at("12:30").do(lambda: post_content('build_in_public', 'twitter'))
schedule.every().friday.at("16:00").do(lambda: post_content('learning_journey', 'twitter'))

schedule.every().saturday.at("10:00").do(lambda: post_content('real_talk', 'twitter'))
schedule.every().saturday.at("14:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().saturday.at("18:00").do(lambda: post_content('build_in_public', 'linkedin'))

schedule.every().sunday.at("09:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().sunday.at("13:00").do(lambda: post_content('learning_journey', 'twitter'))
schedule.every().sunday.at("17:00").do(lambda: post_content('real_talk', 'twitter'))

def run_scheduler():
    """Run scheduler in background thread"""
    print("🤖 Scheduler started - 24 posts per week")
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start scheduler in background thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "running",
        "bot": "Social Media Auto-Poster",
        "posts_per_week": 24,
        "message": "Bot is alive and posting!"
    })

@app.route('/health')
def health():
    """Health check for monitoring"""
    return jsonify({"status": "ok"}), 200

@app.route('/status')
def status():
    """Get bot status"""
    return jsonify({
        "scheduler": "running",
        "next_run": str(schedule.next_run()) if schedule.jobs else "No jobs scheduled"
    })

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
