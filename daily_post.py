"""
Single execution script for PythonAnywhere free tier scheduled task.
Runs once per day and posts to both platforms.
"""
import random
from bot import SocialMediaBot
from ai_content_generator import AIContentGenerator

bot = SocialMediaBot()
ai_gen = AIContentGenerator()

# Randomly select a pillar for variety
pillars = ['build_in_public', 'learning_journey', 'engagement_questions', 'real_talk']
pillar = random.choice(pillars)

# Generate and post
content, used_pillar = ai_gen.generate_post(pillar=pillar, platform='both')

print(f"\n[{used_pillar.upper()}]")
print(f"\nX POST:\n{content['twitter']}\n")
print(f"LINKEDIN POST:\n{content['linkedin']}\n")

# Post to X (LinkedIn will fail but that's ok)
bot.post_to_twitter(content['twitter'])
bot.post_to_linkedin(content['linkedin'])

print("\n✓ Daily post completed")
