"""
Finla - Smart Transaction Categorization Module
Automatically categorizes transactions based on description keywords
"""

import re
from typing import Dict, List, Tuple

class TransactionCategorizer:
    """Smart categorization system for financial transactions"""
    
    def __init__(self):
        """Initialize categorizer with keyword mappings"""
        self.categories = {
            'food': {
                'keywords': [
                    'lunch', 'dinner', 'breakfast', 'meal', 'restaurant', 'hotel', 
                    'biryani', 'pizza', 'burger', 'food', 'eating', 'cafe', 'dhaba',
                    'mess', 'canteen', 'delivery', 'zomato', 'swiggy', 'foodpanda',
                    'mcdonalds', 'kfc', 'dominos', 'subway', 'tiffin', 'paratha',
                    'dosa', 'idli', 'samosa', 'chaat', 'street food'
                ],
                'emoji': '🍔',
                'priority': 1
            },
            'transport': {
                'keywords': [
                    'bus', 'auto', 'taxi', 'uber', 'ola', 'metro', 'train', 'fuel',
                    'petrol', 'diesel', 'travel', 'ticket', 'railway', 'flight',
                    'cab', 'rickshaw', 'transport', 'commute', 'parking', 'toll',
                    'irctc', 'redbus', 'makemytrip', 'goibibo', 'bike', 'car'
                ],
                'emoji': '🚗',
                'priority': 2
            },
            'education': {
                'keywords': [
                    'book', 'course', 'fee', 'tuition', 'study', 'exam', 'college',
                    'school', 'education', 'academy', 'coaching', 'training',
                    'certification', 'library', 'stationery', 'pen', 'notebook',
                    'xerox', 'photocopy', 'udemy', 'coursera', 'byju', 'unacademy'
                ],
                'emoji': '📚',
                'priority': 3
            },
            'snacks': {
                'keywords': [
                    'tea', 'coffee', 'snacks', 'juice', 'water', 'biscuit', 'chips',
                    'chocolate', 'ice cream', 'cold drink', 'soft drink', 'lassi',
                    'smoothie', 'shake', 'popcorn', 'nuts', 'candy', 'sweet',
                    'bakery', 'pastry', 'cake', 'cookies', 'nimbu pani'
                ],
                'emoji': '🧃',
                'priority': 4
            },
            'shopping': {
                'keywords': [
                    'shopping', 'mall', 'store', 'amazon', 'flipkart', 'myntra',
                    'ajio', 'shirt', 'clothes', 'shoes', 'bag', 'mobile', 'laptop',
                    'electronics', 'grocery', 'supermarket', 'market', 'purchase',
                    'buy', 'order', 'delivery', 'online', 'retail', 'brand'
                ],
                'emoji': '🛍️',
                'priority': 5
            },
            'entertainment': {
                'keywords': [
                    'movie', 'cinema', 'theatre', 'film', 'show', 'concert',
                    'game', 'gaming', 'music', 'netflix', 'amazon prime', 'hotstar',
                    'spotify', 'youtube', 'entertainment', 'fun', 'party',
                    'celebration', 'festival', 'event', 'ticket'
                ],
                'emoji': '🎬',
                'priority': 6
            },
            'health': {
                'keywords': [
                    'medicine', 'doctor', 'hospital', 'clinic', 'pharmacy', 'medical',
                    'health', 'checkup', 'treatment', 'surgery', 'dental', 'eye',
                    'prescription', 'tablet', 'injection', 'test', 'lab', 'scan',
                    'apollo', 'fortis', 'max', 'aiims'
                ],
                'emoji': '🏥',
                'priority': 7
            },
            'utilities': {
                'keywords': [
                    'electricity', 'water', 'gas', 'internet', 'phone', 'mobile',
                    'bill', 'recharge', 'broadband', 'wifi', 'airtel', 'jio',
                    'bsnl', 'vodafone', 'utility', 'maintenance', 'rent', 'emi'
                ],
                'emoji': '💡',
                'priority': 8
            },
            'personal_care': {
                'keywords': [
                    'haircut', 'salon', 'parlour', 'spa', 'massage', 'grooming',
                    'cosmetics', 'shampoo', 'soap', 'toothpaste', 'personal',
                    'hygiene', 'beauty', 'skincare', 'makeup'
                ],
                'emoji': '💇',
                'priority': 9
            }
        }
        
        # Compile regex patterns for better performance
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for each category"""
        self.patterns = {}
        for category, data in self.categories.items():
            # Create regex pattern that matches whole words
            pattern = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in data['keywords']) + r')\b'
            self.patterns[category] = re.compile(pattern, re.IGNORECASE)
    
    def categorize(self, description: str, amount: float = 0) -> Tuple[str, float]:
        """
        Categorize a transaction based on description and amount
        
        Args:
            description (str): Transaction description
            amount (float): Transaction amount (can influence categorization)
            
        Returns:
            Tuple[str, float]: (category, confidence_score)
        """
        if not description or not isinstance(description, str):
            return 'others', 0.0
        
        # Clean and normalize description
        clean_desc = self._clean_description(description)
        
        # Find matching categories
        matches = []
        for category, pattern in self.patterns.items():
            match_count = len(pattern.findall(clean_desc))
            if match_count > 0:
                # Calculate confidence based on matches and category priority
                confidence = self._calculate_confidence(
                    category, match_count, clean_desc, amount
                )
                matches.append((category, confidence))
        
        if matches:
            # Sort by confidence and return best match
            matches.sort(key=lambda x: x[1], reverse=True)
            return matches[0]
        
        # Apply amount-based rules if no keyword matches
        category = self._categorize_by_amount(amount)
        return category, 0.3  # Low confidence for amount-based categorization
    
    def _clean_description(self, description: str) -> str:
        """Clean and normalize transaction description"""
        # Convert to lowercase
        clean = description.lower().strip()
        
        # Remove common transaction prefixes/suffixes
        prefixes = ['upi-', 'paytm-', 'gpay-', 'phonepe-', 'payment to', 'paid to']
        for prefix in prefixes:
            if clean.startswith(prefix):
                clean = clean[len(prefix):].strip()
        
        # Remove special characters but keep spaces and hyphens
        clean = re.sub(r'[^\w\s\-]', ' ', clean)
        
        # Remove extra whitespace
        clean = re.sub(r'\s+', ' ', clean)
        
        return clean
    
    def _calculate_confidence(self, category: str, match_count: int, 
                            description: str, amount: float) -> float:
        """Calculate confidence score for a category match"""
        base_confidence = 0.7
        
        # Boost for multiple keyword matches
        match_boost = min(match_count * 0.1, 0.3)
        
        # Category priority boost (higher priority = higher boost)
        priority_boost = (10 - self.categories[category]['priority']) * 0.02
        
        # Amount-based adjustments
        amount_adjustment = self._get_amount_adjustment(category, amount)
        
        # Description length adjustment (longer descriptions often more accurate)
        length_adjustment = min(len(description.split()) * 0.01, 0.1)
        
        confidence = base_confidence + match_boost + priority_boost + amount_adjustment + length_adjustment
        
        return min(confidence, 1.0)  # Cap at 1.0
    
    def _get_amount_adjustment(self, category: str, amount: float) -> float:
        """Adjust confidence based on typical amounts for categories"""
        if amount <= 0:
            return 0
        
        # Typical amount ranges for categories
        typical_ranges = {
            'snacks': (10, 100),
            'food': (50, 500),
            'transport': (20, 200),
            'education': (100, 5000),
            'shopping': (200, 10000),
            'entertainment': (100, 1000),
            'health': (100, 5000),
            'utilities': (500, 5000),
            'personal_care': (100, 2000)
        }
        
        if category in typical_ranges:
            min_amt, max_amt = typical_ranges[category]
            if min_amt <= amount <= max_amt:
                return 0.1  # Boost for typical amount
            elif amount < min_amt * 0.5 or amount > max_amt * 2:
                return -0.1  # Penalty for atypical amount
        
        return 0
    
    def _categorize_by_amount(self, amount: float) -> str:
        """Fallback categorization based on amount patterns"""
        if amount <= 50:
            return 'snacks'
        elif amount <= 200:
            return 'food'
        elif amount <= 500:
            return 'shopping'
        else:
            return 'others'
    
    def get_category_info(self, category: str) -> Dict:
        """Get information about a category"""
        if category in self.categories:
            return {
                'name': category,
                'emoji': self.categories[category]['emoji'],
                'keywords': self.categories[category]['keywords'][:5],  # First 5 keywords
                'priority': self.categories[category]['priority']
            }
        return {
            'name': 'others',
            'emoji': '🔘',
            'keywords': [],
            'priority': 10
        }
    
    def get_all_categories(self) -> List[str]:
        """Get list of all available categories"""
        return list(self.categories.keys()) + ['others']
    
    def suggest_keywords(self, category: str) -> List[str]:
        """Get keyword suggestions for a category"""
        if category in self.categories:
            return self.categories[category]['keywords']
        return []

# Global categorizer instance
_categorizer = TransactionCategorizer()

def categorize_transaction(description: str, amount: float = 0) -> str:
    """
    Main function to categorize a transaction
    
    Args:
        description (str): Transaction description
        amount (float): Transaction amount
        
    Returns:
        str: Category name
    """
    category, confidence = _categorizer.categorize(description, amount)
    return category

def get_category_with_confidence(description: str, amount: float = 0) -> Tuple[str, float]:
    """
    Get category with confidence score
    
    Args:
        description (str): Transaction description
        amount (float): Transaction amount
        
    Returns:
        Tuple[str, float]: (category, confidence_score)
    """
    return _categorizer.categorize(description, amount)

def get_category_info(category: str) -> Dict:
    """Get information about a category"""
    return _categorizer.get_category_info(category)

def get_all_categories() -> List[str]:
    """Get all available categories"""
    return _categorizer.get_all_categories()

# Testing and validation functions
def test_categorizer():
    """Test categorizer with sample transactions"""
    test_cases = [
        ("Lunch at McDonald's", 150, "food"),
        ("Bus fare to office", 25, "transport"),
        ("Coffee with friends", 80, "snacks"),
        ("Python course on Udemy", 2000, "education"),
        ("Movie ticket PVR", 300, "entertainment"),
        ("Medicine from pharmacy", 250, "health"),
        ("Electricity bill payment", 1500, "utilities"),
        ("Shirt from Myntra", 899, "shopping"),
        ("Haircut at salon", 200, "personal_care"),
        ("Random payment", 100, "others")
    ]
    
    print("🧪 Testing Transaction Categorizer")
    print("-" * 50)
    
    correct_predictions = 0
    for description, amount, expected in test_cases:
        predicted, confidence = _categorizer.categorize(description, amount)
        is_correct = predicted == expected
        if is_correct:
            correct_predictions += 1
        
        print(f"Description: {description}")
        print(f"Amount: ₹{amount}")
        print(f"Expected: {expected}, Predicted: {predicted} (Confidence: {confidence:.2f})")
        print(f"✅ Correct" if is_correct else "❌ Incorrect")
        print("-" * 30)
    
    accuracy = (correct_predictions / len(test_cases)) * 100
    print(f"\n📊 Accuracy: {accuracy:.1f}% ({correct_predictions}/{len(test_cases)} correct)")

if __name__ == "__main__":
    test_categorizer()
