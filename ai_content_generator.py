import google.generativeai as genai
import json
import random
from datetime import datetime

class AIContentGenerator:
    def __init__(self, config_file='config.json'):
        with open(config_file, 'r') as f:
            self.config = json.load(f)
        
        genai.configure(api_key=self.config['gemini']['api_key'])
        self.model = genai.GenerativeModel(self.config['gemini']['model'])
        self.pillars = self.config['content_pillars']
        self.brand_voice = self.config['brand_voice']
        self.stage = self.brand_voice.get('stage', 'Student developer')
        self.tone = self.brand_voice.get('tone', 'Casual and relatable')
        self.themes = self.brand_voice.get('themes', [])
        self.history_file = 'post_history.json'
        self.load_history()
    
    def load_history(self):
        try:
            with open(self.history_file, 'r') as f:
                self.history = json.load(f)
            # Ensure all current pillars exist in pillar_counts
            for p in self.pillars:
                if p not in self.history['pillar_counts']:
                    self.history['pillar_counts'][p] = 0
        except FileNotFoundError:
            self.history = {'posts': [], 'pillar_counts': {p: 0 for p in self.pillars}}
    
    def save_history(self, pillar, content):
        self.history['posts'].append({
            'pillar': pillar,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
        self.history['pillar_counts'][pillar] += 1
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)
    
    def select_pillar(self, platform=None):
        weights = []
        pillars = []
        for pillar, data in self.pillars.items():
            count = self.history['pillar_counts'].get(pillar, 0)
            weight = data['weight'] / (count + 1)
            weights.append(weight)
            pillars.append(pillar)
        return random.choices(pillars, weights=weights)[0]
    
    def generate_post(self, pillar=None, custom_context=None, platform='both'):
        if not pillar:
            pillar = self.select_pillar()
        
        pillar_data = self.pillars[pillar]
        brand_theme = random.choice(self.themes) if self.themes else ''
        
        if platform == 'twitter':
            is_thread = pillar == 'tech_threads'
            prompt = f"""You are a {self.stage} posting on X (Twitter). {self.tone}.

Content Pillar: {pillar.replace('_', ' ').title()}
Theme: {brand_theme}
Example: {pillar_data['examples'][0]}
{f'Context: {custom_context}' if custom_context else ''}

{'THREAD FORMAT - Generate 3-5 connected tweets:' if is_thread else 'Requirements:'}
{'- Start with hook tweet (max 280 chars)' if is_thread else '- Max 280 characters'}
{'- Number each tweet (1/, 2/, 3/)' if is_thread else '- Punchy, direct, relatable'}
{'- Each tweet max 280 chars' if is_thread else '- 1-2 emojis'}
{'- End with CTA or question' if is_thread else '- Sound like a student learning'}
- Use casual language
- Be authentic and honest

Generate ONLY the {'thread' if is_thread else 'post'} text."""
        elif platform == 'linkedin':
            # Vary LinkedIn post length: 1 long per day, rest are mid/short
            from datetime import datetime
            hour = datetime.now().hour
            
            # Long post once per day (evening posts)
            if hour >= 18:
                length = "200-300 words (detailed story or insight)"
            # Mid-length posts
            elif hour >= 12:
                length = "100-150 words (concise but meaningful)"
            # Short posts (morning)
            else:
                length = "50-80 words (quick thought or question)"
            
            prompt = f"""You are a {self.stage} posting on LinkedIn. {self.tone}.

Content Pillar: {pillar.replace('_', ' ').title()}
Theme: {brand_theme}
Example: {pillar_data['examples'][0]}
{f'Context: {custom_context}' if custom_context else ''}

Requirements:
- Length: {length}
- Casual but thoughtful tone
- Share learning, building, or real experiences
- NOT overly professional - sound like a student
- Use line breaks for readability
- End with question or insight
- 2-3 hashtags
- Be relatable and honest
- NO markdown formatting (no *, **, _, etc.)
- Plain text only with emojis

Generate ONLY the post text."""
        else:
            # Generate both - avoid threads for 'both' platform
            temp_pillar = pillar if pillar != 'tech_threads' else 'learning_journey'
            twitter_post = self.generate_post(temp_pillar, custom_context, 'twitter')[0]
            linkedin_post = self.generate_post(temp_pillar, custom_context, 'linkedin')[0]
            return {'twitter': twitter_post, 'linkedin': linkedin_post}, temp_pillar
        
        response = self.model.generate_content(prompt)
        content = response.text.strip()
        
        if platform != 'both':
            self.save_history(pillar, content)
        
        return content, pillar

if __name__ == '__main__':
    generator = AIContentGenerator()
    posts, pillar = generator.generate_post(platform='both')
    print(f"\n[{pillar.upper()}]")
    print(f"\n📱 X:\n{posts['twitter']}\n")
    print(f"💼 LinkedIn:\n{posts['linkedin']}\n")
