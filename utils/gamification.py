"""
Finla - Gamification and User Engagement Module
Handles streaks, karma points, achievements, and user motivation systems
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

class GamificationManager:
    """Manages user engagement through streaks, karma points, and achievements"""
    
    def __init__(self):
        """Initialize gamification system"""
        self.data_dir = 'data'
        self.user_stats_file = os.path.join(self.data_dir, 'user_stats.json')
        self.transactions_file = os.path.join(self.data_dir, 'transactions.csv')
        
        # Achievement definitions
        self.achievements = {
            'first_transaction': {
                'name': 'First Step',
                'description': 'Added your first transaction',
                'icon': '🎯',
                'points': 50,
                'type': 'milestone'
            },
            'streak_5': {
                'name': 'Consistent Tracker',
                'description': 'Maintained 5-day tracking streak',
                'icon': '🔥',
                'points': 100,
                'type': 'streak'
            },
            'streak_10': {
                'name': 'Dedicated Tracker',
                'description': 'Maintained 10-day tracking streak',
                'icon': '⚡',
                'points': 200,
                'type': 'streak'
            },
            'streak_30': {
                'name': 'Habit Master',
                'description': 'Maintained 30-day tracking streak',
                'icon': '🏆',
                'points': 500,
                'type': 'streak'
            },
            'saver_100': {
                'name': 'Smart Saver',
                'description': 'Stayed under budget for a week',
                'icon': '💰',
                'points': 150,
                'type': 'financial'
            },
            'category_master': {
                'name': 'Category Master',
                'description': 'Transactions in all 5+ categories',
                'icon': '📊',
                'points': 100,
                'type': 'diversity'
            },
            'mindful_spender': {
                'name': 'Mindful Spender',
                'description': 'Average transaction under ₹100 for a week',
                'icon': '🧘',
                'points': 120,
                'type': 'mindfulness'
            },
            'goal_achiever': {
                'name': 'Goal Achiever',
                'description': 'Completed your first savings goal',
                'icon': '🎯',
                'points': 300,
                'type': 'goal'
            },
            'hundred_transactions': {
                'name': 'Century Club',
                'description': 'Recorded 100 transactions',
                'icon': '💯',
                'points': 250,
                'type': 'milestone'
            }
        }
        
        # Karma point system
        self.karma_rules = {
            'transaction_logged': 5,
            'under_budget_day': 10,
            'goal_progress': 15,
            'streak_bonus': 20,
            'mindful_spending': 8,
            'category_diversity': 12
        }
    
    def get_user_stats(self) -> Dict:
        """Get current user statistics"""
        try:
            if os.path.exists(self.user_stats_file):
                with open(self.user_stats_file, 'r') as f:
                    stats = json.load(f)
            else:
                stats = self._create_default_stats()
                self._save_user_stats(stats)
            
            # Ensure all required fields exist
            default_stats = self._create_default_stats()
            for key, value in default_stats.items():
                if key not in stats:
                    stats[key] = value
            
            return stats
            
        except Exception as e:
            print(f"Error loading user stats: {e}")
            return self._create_default_stats()
    
    def _create_default_stats(self) -> Dict:
        """Create default user statistics"""
        return {
            'streak': 0,
            'max_streak': 0,
            'last_entry_date': '',
            'karma_points': 0,
            'total_transactions': 0,
            'achievements': [],
            'level': 1,
            'experience_points': 0,
            'streak_freeze_count': 3,  # Streak protection tokens
            'weekly_goals_completed': 0,
            'monthly_goals_completed': 0,
            'total_karma_earned': 0,
            'best_saving_week': 0,
            'categories_used': [],
            'first_transaction_date': '',
            'last_achievement_date': ''
        }
    
    def _save_user_stats(self, stats: Dict) -> bool:
        """Save user statistics to file"""
        try:
            with open(self.user_stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving user stats: {e}")
            return False
    
    def update_streak(self) -> Dict:
        """Update user's tracking streak"""
        stats = self.get_user_stats()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Check if there's a transaction today
        has_transaction_today = self._has_transaction_today()
        
        if has_transaction_today:
            last_entry = stats.get('last_entry_date', '')
            
            if last_entry:
                last_date = datetime.strptime(last_entry, '%Y-%m-%d')
                current_date = datetime.strptime(today, '%Y-%m-%d')
                days_diff = (current_date - last_date).days
                
                if days_diff == 1:
                    # Consecutive day - continue streak
                    stats['streak'] += 1
                elif days_diff == 0:
                    # Same day - no change to streak
                    pass
                else:
                    # Gap in days - check if can use streak freeze
                    if days_diff <= 2 and stats.get('streak_freeze_count', 0) > 0:
                        # Use streak freeze
                        stats['streak_freeze_count'] -= 1
                        # Keep current streak
                    else:
                        # Reset streak
                        stats['streak'] = 1
            else:
                # First transaction ever
                stats['streak'] = 1
                stats['first_transaction_date'] = today
            
            # Update max streak
            if stats['streak'] > stats.get('max_streak', 0):
                stats['max_streak'] = stats['streak']
            
            # Update last entry date
            stats['last_entry_date'] = today
            
            # Award streak achievements
            new_achievements = self._check_streak_achievements(stats)
            
            # Add karma points for maintaining streak
            if stats['streak'] >= 5:
                karma_earned = self.karma_rules['streak_bonus']
                stats['karma_points'] += karma_earned
                stats['total_karma_earned'] += karma_earned
        
        # Save updated stats
        self._save_user_stats(stats)
        
        return {
            'streak': stats['streak'],
            'max_streak': stats['max_streak'],
            'new_achievements': new_achievements if has_transaction_today else [],
            'streak_freeze_count': stats.get('streak_freeze_count', 0)
        }
    
    def update_karma_points(self, category: str, amount: float) -> int:
        """Update karma points based on transaction"""
        stats = self.get_user_stats()
        karma_earned = 0
        
        # Base karma for logging transaction
        karma_earned += self.karma_rules['transaction_logged']
        
        # Bonus for mindful spending (small amounts)
        if amount <= 100:
            karma_earned += self.karma_rules['mindful_spending']
        
        # Category diversity bonus
        if category not in stats.get('categories_used', []):
            karma_earned += self.karma_rules['category_diversity']
            categories_used = stats.get('categories_used', [])
            categories_used.append(category)
            stats['categories_used'] = categories_used
        
        # Update stats
        stats['karma_points'] += karma_earned
        stats['total_karma_earned'] += karma_earned
        stats['total_transactions'] += 1
        
        # Update level based on karma points
        stats['level'] = self._calculate_level(stats['karma_points'])
        
        # Check for new achievements
        new_achievements = self._check_transaction_achievements(stats, category, amount)
        
        self._save_user_stats(stats)
        
        return karma_earned
    
    def _has_transaction_today(self) -> bool:
        """Check if user has logged any transaction today"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        try:
            import csv
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if row.get('date', '') == today:
                            return True
        except Exception as e:
            print(f"Error checking today's transactions: {e}")
        
        return False
    
    def _check_streak_achievements(self, stats: Dict) -> List[Dict]:
        """Check and award streak-based achievements"""
        new_achievements = []
        current_streak = stats['streak']
        existing_achievements = set(stats.get('achievements', []))
        
        # Check streak milestones
        streak_milestones = [5, 10, 30]
        for milestone in streak_milestones:
            achievement_id = f'streak_{milestone}'
            if current_streak >= milestone and achievement_id not in existing_achievements:
                achievement = self.achievements[achievement_id].copy()
                achievement['earned_date'] = datetime.now().strftime('%Y-%m-%d')
                achievement['id'] = achievement_id
                
                new_achievements.append(achievement)
                stats['achievements'].append(achievement_id)
                stats['karma_points'] += achievement['points']
                stats['total_karma_earned'] += achievement['points']
        
        return new_achievements
    
    def _check_transaction_achievements(self, stats: Dict, category: str, amount: float) -> List[Dict]:
        """Check and award transaction-based achievements"""
        new_achievements = []
        existing_achievements = set(stats.get('achievements', []))
        
        # First transaction achievement
        if stats['total_transactions'] == 1 and 'first_transaction' not in existing_achievements:
            achievement = self.achievements['first_transaction'].copy()
            achievement['earned_date'] = datetime.now().strftime('%Y-%m-%d')
            achievement['id'] = 'first_transaction'
            
            new_achievements.append(achievement)
            stats['achievements'].append('first_transaction')
        
        # Century club achievement
        if stats['total_transactions'] >= 100 and 'hundred_transactions' not in existing_achievements:
            achievement = self.achievements['hundred_transactions'].copy()
            achievement['earned_date'] = datetime.now().strftime('%Y-%m-%d')
            achievement['id'] = 'hundred_transactions'
            
            new_achievements.append(achievement)
            stats['achievements'].append('hundred_transactions')
        
        # Category master achievement
        if len(stats.get('categories_used', [])) >= 5 and 'category_master' not in existing_achievements:
            achievement = self.achievements['category_master'].copy()
            achievement['earned_date'] = datetime.now().strftime('%Y-%m-%d')
            achievement['id'] = 'category_master'
            
            new_achievements.append(achievement)
            stats['achievements'].append('category_master')
        
        return new_achievements
    
    def _calculate_level(self, karma_points: int) -> int:
        """Calculate user level based on karma points"""
        # Level progression: 100 points per level initially, then increasing
        if karma_points < 100:
            return 1
        elif karma_points < 300:
            return 2
        elif karma_points < 600:
            return 3
        elif karma_points < 1000:
            return 4
        elif karma_points < 1500:
            return 5
        else:
            # Higher levels need more points
            return min(5 + (karma_points - 1500) // 500, 20)
    
    def get_level_progress(self) -> Dict:
        """Get current level and progress to next level"""
        stats = self.get_user_stats()
        current_level = stats['level']
        karma_points = stats['karma_points']
        
        # Calculate points needed for next level
        level_thresholds = [0, 100, 300, 600, 1000, 1500]
        
        if current_level < len(level_thresholds):
            current_threshold = level_thresholds[current_level - 1] if current_level > 1 else 0
            next_threshold = level_thresholds[current_level] if current_level < len(level_thresholds) else level_thresholds[-1] + (current_level - len(level_thresholds) + 1) * 500
        else:
            current_threshold = 1500 + (current_level - 6) * 500
            next_threshold = current_threshold + 500
        
        progress = karma_points - current_threshold
        needed = next_threshold - karma_points
        progress_percentage = (progress / (next_threshold - current_threshold)) * 100
        
        return {
            'current_level': current_level,
            'karma_points': karma_points,
            'points_in_level': progress,
            'points_to_next': max(needed, 0),
            'progress_percentage': min(progress_percentage, 100),
            'next_level': current_level + 1
        }
    
    def get_achievements(self, earned_only: bool = False) -> List[Dict]:
        """Get list of achievements"""
        stats = self.get_user_stats()
        earned_achievements = set(stats.get('achievements', []))
        
        achievements_list = []
        for achievement_id, achievement_data in self.achievements.items():
            achievement = achievement_data.copy()
            achievement['id'] = achievement_id
            achievement['earned'] = achievement_id in earned_achievements
            
            if not earned_only or achievement['earned']:
                achievements_list.append(achievement)
        
        # Sort by earned status and points
        achievements_list.sort(key=lambda x: (not x['earned'], -x['points']))
        
        return achievements_list
    
    def get_weekly_summary(self) -> Dict:
        """Get weekly gamification summary"""
        stats = self.get_user_stats()
        
        # Calculate this week's activity
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        
        weekly_transactions = 0
        weekly_karma = 0
        
        try:
            import csv
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        date_str = row.get('date', '')
                        if date_str:
                            transaction_date = datetime.strptime(date_str, '%Y-%m-%d')
                            if transaction_date >= week_start:
                                weekly_transactions += 1
                                weekly_karma += 5  # Base karma per transaction
        except Exception as e:
            print(f"Error calculating weekly summary: {e}")
        
        return {
            'weekly_transactions': weekly_transactions,
            'weekly_karma': weekly_karma,
            'current_streak': stats['streak'],
            'max_streak': stats['max_streak'],
            'achievements_this_week': self._get_recent_achievements(7),
            'level': stats['level'],
            'streak_freeze_available': stats.get('streak_freeze_count', 0)
        }
    
    def _get_recent_achievements(self, days: int) -> List[Dict]:
        """Get achievements earned in the last N days"""
        # This would require storing achievement dates, which we can add later
        # For now, return empty list
        return []
    
    def use_streak_freeze(self) -> bool:
        """Use a streak freeze token"""
        stats = self.get_user_stats()
        
        if stats.get('streak_freeze_count', 0) > 0:
            stats['streak_freeze_count'] -= 1
            self._save_user_stats(stats)
            return True
        
        return False
    
    def get_leaderboard_data(self) -> Dict:
        """Get user's leaderboard position (single user for now)"""
        stats = self.get_user_stats()
        
        return {
            'rank': 1,  # Always rank 1 for single user
            'total_users': 1,
            'karma_points': stats['karma_points'],
            'level': stats['level'],
            'streak': stats['streak'],
            'achievements_count': len(stats.get('achievements', [])),
            'percentile': 100  # Top 100% (only user)
        }

# Global gamification manager instance
_gamification_manager = GamificationManager()

def update_streak() -> Dict:
    """Update user's tracking streak"""
    return _gamification_manager.update_streak()

def update_karma_points(category: str, amount: float) -> int:
    """Update karma points for a transaction"""
    return _gamification_manager.update_karma_points(category, amount)

def get_user_stats() -> Dict:
    """Get current user statistics"""
    return _gamification_manager.get_user_stats()

def get_level_progress() -> Dict:
    """Get level progress information"""
    return _gamification_manager.get_level_progress()

def get_achievements(earned_only: bool = False) -> List[Dict]:
    """Get list of achievements"""
    return _gamification_manager.get_achievements(earned_only)

def get_weekly_summary() -> Dict:
    """Get weekly gamification summary"""
    return _gamification_manager.get_weekly_summary()

def use_streak_freeze() -> bool:
    """Use a streak freeze token"""
    return _gamification_manager.use_streak_freeze()

def get_leaderboard_data() -> Dict:
    """Get leaderboard data"""
    return _gamification_manager.get_leaderboard_data()

# Test function
def test_gamification():
    """Test gamification functionality"""
    print("🎮 Testing Gamification System")
    print("-" * 40)
    
    # Test user stats
    stats = get_user_stats()
    print(f"Current Level: {stats['level']}")
    print(f"Karma Points: {stats['karma_points']}")
    print(f"Current Streak: {stats['streak']}")
    
    # Test level progress
    progress = get_level_progress()
    print(f"Progress to Level {progress['next_level']}: {progress['progress_percentage']:.1f}%")
    
    # Test achievements
    achievements = get_achievements()
    earned_count = sum(1 for a in achievements if a['earned'])
    print(f"Achievements: {earned_count}/{len(achievements)} earned")
    
    # Test weekly summary
    weekly = get_weekly_summary()
    print(f"Weekly Transactions: {weekly['weekly_transactions']}")

if __name__ == "__main__":
    test_gamification()
