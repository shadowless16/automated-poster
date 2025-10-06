import requests
import json
import argparse
from datetime import datetime
from ai_content_generator import AIContentGenerator

class SocialMediaBot:
    def __init__(self, config_file='config.json'):
        import os
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        else:
            # Load from environment variables (for Render deployment)
            self.config = {
                'twitter': {
                    'api_key': os.environ.get('TWITTER_API_KEY'),
                    'api_secret': os.environ.get('TWITTER_API_SECRET'),
                    'access_token': os.environ.get('TWITTER_ACCESS_TOKEN'),
                    'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET'),
                    'bearer_token': os.environ.get('TWITTER_BEARER_TOKEN')
                },
                'linkedin': {
                    'access_token': os.environ.get('LINKEDIN_ACCESS_TOKEN'),
                    'person_id': os.environ.get('LINKEDIN_PERSON_ID')
                },
                'gemini': {
                    'api_key': os.environ.get('GEMINI_API_KEY'),
                    'model': 'gemini-2.5-flash'
                }
            }
        self._setup_twitter()
        self.ai_generator = AIContentGenerator(config_file)
    
    def _setup_twitter(self):
        try:
            import tweepy
            self.twitter_v2 = tweepy.Client(
                bearer_token=self.config['twitter']['bearer_token'],
                consumer_key=self.config['twitter']['api_key'],
                consumer_secret=self.config['twitter']['api_secret'],
                access_token=self.config['twitter']['access_token'],
                access_token_secret=self.config['twitter']['access_token_secret']
            )
        except ImportError:
            print("⚠ Tweepy not installed. Using direct API calls for X.")
            self.twitter_v2 = None
    
    def post_to_twitter(self, text):
        try:
            if self.twitter_v2:
                response = self.twitter_v2.create_tweet(text=text)
                print(f"✓ Posted to X: {text[:50]}...")
                return response
            else:
                # OAuth 1.0a for posting
                from requests_oauthlib import OAuth1
                
                auth = OAuth1(
                    self.config['twitter']['api_key'],
                    self.config['twitter']['api_secret'],
                    self.config['twitter']['access_token'],
                    self.config['twitter']['access_token_secret']
                )
                
                data = {"text": text}
                response = requests.post(
                    'https://api.twitter.com/2/tweets',
                    auth=auth,
                    json=data
                )
                
                if response.status_code == 201:
                    print(f"✓ Posted to X: {text[:50]}...")
                    return response.json()
                else:
                    print(f"✗ X posting failed: {response.text}")
                    return None
        except Exception as e:
            print(f"✗ X posting failed: {e}")
            return None
    
    def _get_linkedin_member_id(self, access_token):
        # Try multiple methods to get member ID
        headers = {'Authorization': f'Bearer {access_token}'}
        
        # Method 1: Try lite profile
        try:
            response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
            if response.status_code == 200:
                return response.json()['id']
        except:
            pass
        
        # Method 2: Extract from token introspection
        try:
            response = requests.get(
                'https://api.linkedin.com/v2/me',
                headers={**headers, 'X-Restli-Protocol-Version': '2.0.0'}
            )
            if response.status_code == 200:
                return response.json()['id']
        except:
            pass
        
        return None
    
    def post_to_linkedin(self, text):
        try:
            access_token = self.config['linkedin']['access_token']

            headers = {
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }

            # Get user ID from userinfo endpoint
            userinfo_resp = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
            if userinfo_resp.status_code != 200:
                print(f"✗ Failed to get user ID: {userinfo_resp.status_code}")
                return None
            
            user_id = userinfo_resp.json().get('sub')
            if not user_id:
                print("✗ No user ID found in userinfo response")
                return None

            # Use UGC API with user_id from userinfo
            post_data = {
                "author": f"urn:li:person:{user_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
            }
            
            response = requests.post(
                'https://api.linkedin.com/v2/ugcPosts',
                headers=headers,
                json=post_data
            )
            
            if response.status_code == 201:
                print(f"✓ Posted to LinkedIn: {text[:50]}...")
                return response.json()
            else:
                print(f"✗ LinkedIn posting failed ({response.status_code}): {response.text[:200]}")
                return None
        except Exception as e:
            print(f"\u2717 LinkedIn posting failed: {e}")
            return None


def _cli_main():
    parser = argparse.ArgumentParser(description='SocialMediaBot CLI - default dry-run (prints generated content).')
    parser.add_argument('--post', action='store_true', help='Actually post to platforms (uses tokens in config.json)')
    parser.add_argument('--text', type=str, help='Provide custom text to post (overrides AI generation)')
    args = parser.parse_args()

    bot = SocialMediaBot()

    if args.text:
        twitter_text = args.text
        linkedin_text = args.text
        used_pillar = 'custom'
    else:
        content, used_pillar = bot.ai_generator.generate_post(None, None, 'both')
        twitter_text = content.get('twitter')
        linkedin_text = content.get('linkedin')

    print(f"\n[AI Generated - {used_pillar.upper()}]\n")
    print("📱 X POST:")
    print(twitter_text)
    print("\n💼 LINKEDIN POST:")
    print(linkedin_text)

    if args.post:
        print('\n-- Posting to platforms (this will use your configured tokens) --')
        t_res = bot.post_to_twitter(twitter_text)
        l_res = bot.post_to_linkedin(linkedin_text)
        print('\nDone. Results:')
        # For requests.Response show status code; otherwise print raw
        print('Twitter result:', getattr(t_res, 'status_code', t_res))
        print('LinkedIn result:', getattr(l_res, 'status_code', l_res))
    else:
        print('\nDry-run mode: no API calls were made. Re-run with --post to publish.')


if __name__ == '__main__':
    _cli_main()
