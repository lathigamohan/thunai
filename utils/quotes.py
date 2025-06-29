"""
Finla - Daily Motivational Quotes Module
Provides Tamil and English quotes from Thirukkural, Warren Buffett, and AI-generated wisdom
"""

import random
from datetime import datetime
from typing import Dict, List, Optional

class QuoteManager:
    """Manages daily motivational quotes for financial wisdom"""
    
    def __init__(self):
        """Initialize quote collections"""
        
        # Thirukkural quotes (751, 753, 754 and related financial wisdom)
        self.thirukkural_quotes = [
            {
                'text': 'Wealth unused is not wealth at all.',
                'tamil': 'செல்வத்துள் செல்வம் செவிக்கு செல்வம்',
                'author': 'Thirukkural 751',
                'translation': 'Among wealth, the wealth that comes to the ear (knowledge) is true wealth',
                'category': 'wisdom'
            },
            {
                'text': 'The best investment is in knowledge and wisdom.',
                'tamil': 'கல்வி கரையில் கற்பித்துக் கொண்டிருப்பது',
                'author': 'Thirukkural 753',
                'translation': 'Education is the shore where wisdom is taught and learned',
                'category': 'education'
            },
            {
                'text': 'Saving today ensures prosperity tomorrow.',
                'tamil': 'இன்று சேர்த்த செல்வம் நாளை துன்பம் தீர்க்கும்',
                'author': 'Thirukkural 754',
                'translation': 'Wealth saved today will solve tomorrow\'s troubles',
                'category': 'savings'
            },
            {
                'text': 'Spend wisely, for money spent is money gone.',
                'tamil': 'ஒழுக்கத்துடன் செலவிடு, அதுவே செல்வத்தின் வழி',
                'author': 'Thirukkural - Inspired',
                'translation': 'Spend with discipline, that is the path of wealth',
                'category': 'spending'
            },
            {
                'text': 'Debt is the enemy of peace and prosperity.',
                'tamil': 'கடன் என்பது மனநிம்மதியின் எதிரி',
                'author': 'Thirukkural - Inspired',
                'translation': 'Debt is the enemy of mental peace',
                'category': 'debt'
            }
        ]
        
        # Warren Buffett quotes
        self.buffett_quotes = [
            {
                'text': 'Do not save what is left after spending, but spend what is left after saving.',
                'tamil': None,
                'author': 'Warren Buffett',
                'category': 'savings'
            },
            {
                'text': 'Price is what you pay. Value is what you get.',
                'tamil': None,
                'author': 'Warren Buffett',
                'category': 'value'
            },
            {
                'text': 'Someone\'s sitting in the shade today because someone planted a tree a long time ago.',
                'tamil': None,
                'author': 'Warren Buffett',
                'category': 'investment'
            },
            {
                'text': 'Risk comes from not knowing what you\'re doing.',
                'tamil': None,
                'author': 'Warren Buffett',
                'category': 'knowledge'
            },
            {
                'text': 'It\'s far better to buy a wonderful company at a fair price than a fair company at a wonderful price.',
                'tamil': None,
                'author': 'Warren Buffett',
                'category': 'investment'
            }
        ]
        
        # AI-generated financial wisdom quotes
        self.ai_quotes = [
            {
                'text': 'Track your expenses like you track your heartbeat - consistently and with purpose.',
                'tamil': 'உங்கள் செலவுகளை உங்கள் இதயத் துடிப்பு போல கவனமாக கண்காணியுங்கள்',
                'author': 'Finla Wisdom',
                'category': 'tracking'
            },
            {
                'text': 'Small expenses, when ignored, become big regrets.',
                'tamil': 'சிறிய செலவுகள் அலட்சியம் செய்யப்பட்டால் பெரிய வருத்தமாக மாறும்',
                'author': 'Finla Wisdom',
                'category': 'mindfulness'
            },
            {
                'text': 'Your future self will thank you for the money you save today.',
                'tamil': 'இன்று நீங்கள் சேமிக்கும் பணத்திற்கு உங்கள் எதிர்கால நீங்கள் நன்றி சொல்வீர்கள்',
                'author': 'Finla Wisdom',
                'category': 'future'
            },
            {
                'text': 'Budgeting is not about limiting yourself, it\'s about making the things that excite you possible.',
                'tamil': 'பட்ஜெட் என்பது உங்களை கட்டுப்படுத்துவது அல்ல, உங்களை உற்சாகப்படுத்தும் விஷயங்களை சாத்தியமாக்குவது',
                'author': 'Finla Wisdom',
                'category': 'budgeting'
            },
            {
                'text': 'Every rupee saved is a step towards financial freedom.',
                'tamil': 'சேமிக்கப்படும் ஒவ்வொரு ரூபாயும் நிதி சுதந்திரத்தின் நோக்கி ஒரு அடி',
                'author': 'Finla Wisdom',
                'category': 'freedom'
            },
            {
                'text': 'Discipline in spending today creates abundance tomorrow.',
                'tamil': 'இன்றைய செலவில் கடைபிடிக்கும் ஒழுக்கம் நாளை வளத்தை உருவாக்கும்',
                'author': 'Finla Wisdom',
                'category': 'discipline'
            }
        ]
        
        # Motivational quotes for different financial situations
        self.situational_quotes = {
            'low_balance': [
                {
                    'text': 'Every financial comeback starts with a single saved rupee.',
                    'tamil': 'ஒவ்வொரு நிதி மீள்வரவும் ஒரு ரூபாய் சேமிப்பில் தொடங்குகிறது',
                    'author': 'Finla Motivation',
                    'category': 'comeback'
                }
            ],
            'high_spending': [
                {
                    'text': 'Pause before you purchase. Your future self depends on it.',
                    'tamil': 'வாங்குவதற்கு முன் நிறுத்துங்கள். உங்கள் எதிர்காலம் அதை சார்ந்துள்ளது',
                    'author': 'Finla Motivation',
                    'category': 'mindful_spending'
                }
            ],
            'good_savings': [
                {
                    'text': 'Your discipline today is building your dreams for tomorrow.',
                    'tamil': 'இன்றைய உங்கள் ஒழுக்கம் நாளைய கனவுகளை உருவாக்குகிறது',
                    'author': 'Finla Motivation',
                    'category': 'success'
                }
            ]
        }
        
        # Combine all quote collections
        self.all_quotes = (
            self.thirukkural_quotes + 
            self.buffett_quotes + 
            self.ai_quotes
        )
        
        # Initialize random seed based on date for daily consistency
        self._set_daily_seed()
    
    def _set_daily_seed(self):
        """Set random seed based on current date for consistent daily quotes"""
        today = datetime.now()
        date_seed = today.year * 10000 + today.month * 100 + today.day
        random.seed(date_seed)
    
    def get_daily_quote(self, situation: Optional[str] = None) -> Dict:
        """
        Get the quote of the day
        
        Args:
            situation (str, optional): Financial situation for targeted quotes
            
        Returns:
            Dict: Quote information with text, tamil, author, and category
        """
        # Reset seed for consistency
        self._set_daily_seed()
        
        # If situation is provided, try to get relevant quote
        if situation and situation in self.situational_quotes:
            quotes_pool = self.situational_quotes[situation] + self.all_quotes
        else:
            quotes_pool = self.all_quotes
        
        # Select quote based on day of year to ensure variety
        day_of_year = datetime.now().timetuple().tm_yday
        quote_index = day_of_year % len(quotes_pool)
        
        selected_quote = quotes_pool[quote_index].copy()
        
        # Add additional metadata
        selected_quote['date'] = datetime.now().strftime('%Y-%m-%d')
        selected_quote['day_of_year'] = day_of_year
        
        return selected_quote
    
    def get_quote_by_category(self, category: str) -> Dict:
        """Get a random quote from specific category"""
        category_quotes = [q for q in self.all_quotes if q['category'] == category]
        
        if not category_quotes:
            return self.get_daily_quote()
        
        return random.choice(category_quotes)
    
    def get_random_quote(self) -> Dict:
        """Get a completely random quote"""
        return random.choice(self.all_quotes)
    
    def get_thirukkural_quote(self) -> Dict:
        """Get a random Thirukkural quote"""
        return random.choice(self.thirukkural_quotes)
    
    def get_buffett_quote(self) -> Dict:
        """Get a random Warren Buffett quote"""
        return random.choice(self.buffett_quotes)
    
    def get_ai_quote(self) -> Dict:
        """Get a random AI-generated quote"""
        return random.choice(self.ai_quotes)
    
    def get_quotes_by_author(self, author: str) -> List[Dict]:
        """Get all quotes by specific author"""
        return [q for q in self.all_quotes if author.lower() in q['author'].lower()]
    
    def get_available_categories(self) -> List[str]:
        """Get list of all available quote categories"""
        categories = set()
        for quote in self.all_quotes:
            categories.add(quote['category'])
        return sorted(list(categories))
    
    def get_weekly_quotes(self) -> List[Dict]:
        """Get 7 quotes for the week"""
        # Ensure we have enough variety
        weekly_quotes = []
        used_indices = set()
        
        for day in range(7):
            # Calculate index for each day of the week
            today = datetime.now()
            target_date = today + timedelta(days=day)
            day_seed = target_date.year * 10000 + target_date.month * 100 + target_date.day
            
            # Use modulo to select quote, avoid repeats
            attempts = 0
            while attempts < len(self.all_quotes):
                quote_index = (day_seed + attempts) % len(self.all_quotes)
                if quote_index not in used_indices:
                    used_indices.add(quote_index)
                    quote = self.all_quotes[quote_index].copy()
                    quote['date'] = target_date.strftime('%Y-%m-%d')
                    quote['day_name'] = target_date.strftime('%A')
                    weekly_quotes.append(quote)
                    break
                attempts += 1
        
        return weekly_quotes
    
    def search_quotes(self, keyword: str) -> List[Dict]:
        """Search quotes by keyword in text or translation"""
        keyword = keyword.lower()
        matching_quotes = []
        
        for quote in self.all_quotes:
            if (keyword in quote['text'].lower() or 
                (quote.get('tamil') and keyword in quote['tamil'].lower()) or
                (quote.get('translation') and keyword in quote['translation'].lower()) or
                keyword in quote['category'].lower() or
                keyword in quote['author'].lower()):
                matching_quotes.append(quote)
        
        return matching_quotes

# Global quote manager instance
_quote_manager = QuoteManager()

def get_daily_quote(situation: Optional[str] = None) -> Dict:
    """Get the daily motivational quote"""
    return _quote_manager.get_daily_quote(situation)

def get_quote_by_category(category: str) -> Dict:
    """Get quote by category"""
    return _quote_manager.get_quote_by_category(category)

def get_random_quote() -> Dict:
    """Get a random quote"""
    return _quote_manager.get_random_quote()

def get_thirukkural_quote() -> Dict:
    """Get a Thirukkural quote"""
    return _quote_manager.get_thirukkural_quote()

def get_buffett_quote() -> Dict:
    """Get a Warren Buffett quote"""
    return _quote_manager.get_buffett_quote()

def get_weekly_quotes() -> List[Dict]:
    """Get quotes for the week"""
    return _quote_manager.get_weekly_quotes()

def search_quotes(keyword: str) -> List[Dict]:
    """Search quotes by keyword"""
    return _quote_manager.search_quotes(keyword)

def get_available_categories() -> List[str]:
    """Get all quote categories"""
    return _quote_manager.get_available_categories()

# Test function
def test_quotes():
    """Test quote functionality"""
    print("🎯 Testing Quote Manager")
    print("-" * 40)
    
    # Test daily quote
    daily = get_daily_quote()
    print("Daily Quote:")
    print(f"  Text: {daily['text']}")
    if daily.get('tamil'):
        print(f"  Tamil: {daily['tamil']}")
    print(f"  Author: {daily['author']}")
    print(f"  Category: {daily['category']}")
    print()
    
    # Test category quotes
    categories = get_available_categories()
    print(f"Available Categories: {', '.join(categories)}")
    print()
    
    # Test search
    search_results = search_quotes('money')
    print(f"Search for 'money': {len(search_results)} results")
    
    # Test weekly quotes
    weekly = get_weekly_quotes()
    print(f"Weekly quotes: {len(weekly)} quotes for the week")

if __name__ == "__main__":
    test_quotes()
