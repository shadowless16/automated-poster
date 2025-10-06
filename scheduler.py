import schedule
import time
from bot import SocialMediaBot
from ai_content_generator import AIContentGenerator

bot = SocialMediaBot()
ai_gen = AIContentGenerator()

def post_content(pillar, platform):
    """Generate and post content for specific pillar and platform"""
    print(f"\n⏰ Posting at {time.strftime('%H:%M')} WAT")
    if platform == 'twitter':
        content, _ = ai_gen.generate_post(pillar=pillar, platform='twitter')
        print(f"\n[{pillar.upper()}] X POST:")
        print(content)
        bot.post_to_twitter(content)
    elif platform == 'linkedin':
        content, _ = ai_gen.generate_post(pillar=pillar, platform='linkedin')
        print(f"\n[{pillar.upper()}] LINKEDIN POST:")
        print(content)
        bot.post_to_linkedin(content)
    elif platform == 'both':
        content, _ = ai_gen.generate_post(pillar=pillar, platform='both')
        print(f"\n[{pillar.upper()}] X POST:")
        print(content['twitter'])
        print(f"\n[{pillar.upper()}] LINKEDIN POST:")
        print(content['linkedin'])
        bot.post_to_twitter(content['twitter'])
        bot.post_to_linkedin(content['linkedin'])

# Schedule based on config.json posting_schedule (24 posts/week)
# Monday (4 posts)
schedule.every().monday.at("07:30").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().monday.at("12:00").do(lambda: post_content('learning_journey', 'twitter'))
schedule.every().monday.at("16:00").do(lambda: post_content('build_in_public', 'twitter'))
schedule.every().monday.at("19:00").do(lambda: post_content('learning_journey', 'linkedin'))

# Tuesday (3 posts)
schedule.every().tuesday.at("08:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().tuesday.at("13:00").do(lambda: post_content('real_talk', 'twitter'))
schedule.every().tuesday.at("17:30").do(lambda: post_content('build_in_public', 'twitter'))

# Wednesday (4 posts)
schedule.every().wednesday.at("07:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().wednesday.at("12:00").do(lambda: post_content('tech_threads', 'twitter'))
schedule.every().wednesday.at("16:30").do(lambda: post_content('learning_journey', 'twitter'))
schedule.every().wednesday.at("19:00").do(lambda: post_content('build_in_public', 'linkedin'))

# Thursday (4 posts)
schedule.every().thursday.at("07:30").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().thursday.at("11:30").do(lambda: post_content('learning_journey', 'twitter'))
schedule.every().thursday.at("15:00").do(lambda: post_content('real_talk', 'twitter'))
schedule.every().thursday.at("18:30").do(lambda: post_content('learning_journey', 'linkedin'))

# Friday (3 posts)
schedule.every().friday.at("08:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().friday.at("12:30").do(lambda: post_content('build_in_public', 'twitter'))
schedule.every().friday.at("16:00").do(lambda: post_content('learning_journey', 'twitter'))

# Saturday (3 posts)
schedule.every().saturday.at("10:00").do(lambda: post_content('real_talk', 'twitter'))
schedule.every().saturday.at("14:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().saturday.at("18:00").do(lambda: post_content('build_in_public', 'linkedin'))

# Sunday (3 posts)
schedule.every().sunday.at("09:00").do(lambda: post_content('engagement_questions', 'twitter'))
schedule.every().sunday.at("13:00").do(lambda: post_content('learning_journey', 'twitter'))
schedule.every().sunday.at("17:00").do(lambda: post_content('real_talk', 'twitter'))

print("🤖 Scheduler started - 24 posts per week (3-4 per day)")
print("📅 Schedule (WAT - West Africa Time):")
print("  Mon: 7:30am, 12pm, 4pm, 7pm (4 posts)")
print("  Tue: 8am, 1pm, 5:30pm (3 posts)")
print("  Wed: 7am, 12pm, 4:30pm, 7pm (4 posts)")
print("  Thu: 7:30am, 11:30am, 3pm, 6:30pm (4 posts)")
print("  Fri: 8am, 12:30pm, 4pm (3 posts)")
print("  Sat: 10am, 2pm, 6pm (3 posts)")
print("  Sun: 9am, 1pm, 5pm (3 posts)")
print("\nPress Ctrl+C to stop.\n")

while True:
    schedule.run_pending()
    time.sleep(60)
