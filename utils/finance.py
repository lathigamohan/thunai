"""
Finla - Financial Calculations and Analysis Module
Handles balance calculations, budget analysis, and financial insights
"""

import json
import csv
import os
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

class FinanceCalculator:
    """Core financial calculations for Finla"""
    
    def __init__(self):
        """Initialize finance calculator"""
        self.data_dir = 'data'
        self.banks_file = os.path.join(self.data_dir, 'banks.json')
        self.transactions_file = os.path.join(self.data_dir, 'transactions.csv')
        self.goals_file = os.path.join(self.data_dir, 'goals.json')
    
    def calculate_bank_balances(self) -> Dict:
        """Calculate current balance for each bank account"""
        try:
            # Load bank initial balances
            with open(self.banks_file, 'r') as f:
                banks = json.load(f)
            
            # Initialize balances with initial amounts
            balances = {}
            for bank_name, bank_info in banks.items():
                balances[bank_name] = float(bank_info.get('initial_balance', 0))
            
            # Load transactions and update balances
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        bank = row.get('bank', '').strip()
                        amount = float(row.get('amount', 0))
                        
                        if bank and bank in balances:
                            balances[bank] -= amount  # Subtract expense
            
            # Calculate total balance
            total_balance = sum(balances.values())
            
            return {
                'banks': balances,
                'total': total_balance
            }
            
        except Exception as e:
            print(f"Error calculating balances: {e}")
            return {'banks': {}, 'total': 0.0}
    
    def check_low_balance_alerts(self) -> List[Dict]:
        """Check for low balance alerts"""
        alerts = []
        
        try:
            # Load bank info
            with open(self.banks_file, 'r') as f:
                banks = json.load(f)
            
            # Get current balances
            balance_info = self.calculate_bank_balances()
            current_balances = balance_info['banks']
            
            # Check each bank against minimum balance
            for bank_name, bank_info in banks.items():
                current_balance = current_balances.get(bank_name, 0)
                min_balance = float(bank_info.get('min_balance', 0))
                
                if current_balance <= min_balance:
                    alerts.append({
                        'bank': bank_name,
                        'current_balance': current_balance,
                        'min_balance': min_balance,
                        'deficit': min_balance - current_balance,
                        'severity': 'critical' if current_balance < 0 else 'warning'
                    })
            
        except Exception as e:
            print(f"Error checking balance alerts: {e}")
        
        return alerts
    
    def calculate_monthly_budget_summary(self, month: Optional[str] = None) -> Dict:
        """Calculate 50/30/20 budget analysis for given month"""
        if not month:
            month = datetime.now().strftime('%Y-%m')
        
        try:
            # Get total income/initial balance for budget calculation
            balance_info = self.calculate_bank_balances()
            total_available = balance_info['total']
            
            # If no balance, use default budget
            if total_available <= 0:
                total_available = 10000  # Default assumption
            
            # Calculate budget allocations (50/30/20 rule)
            needs_budget = total_available * 0.5
            wants_budget = total_available * 0.3
            savings_target = total_available * 0.2
            
            # Calculate actual spending by category
            monthly_spending = self.get_monthly_spending_by_category(month)
            
            # Map categories to budget types
            needs_categories = ['food', 'transport', 'utilities', 'health']
            wants_categories = ['entertainment', 'shopping', 'snacks', 'personal_care']
            
            needs_spent = sum(monthly_spending.get(cat, 0) for cat in needs_categories)
            wants_spent = sum(monthly_spending.get(cat, 0) for cat in wants_categories)
            total_spent = sum(monthly_spending.values())
            
            # Calculate actual savings (remaining balance)
            savings_actual = max(total_available - total_spent, 0)
            
            return {
                'month': month,
                'total_budget': total_available,
                'needs_budget': needs_budget,
                'needs_spent': needs_spent,
                'needs_remaining': needs_budget - needs_spent,
                'wants_budget': wants_budget,
                'wants_spent': wants_spent,
                'wants_remaining': wants_budget - wants_spent,
                'savings_target': savings_target,
                'savings_actual': savings_actual,
                'savings_shortfall': max(savings_target - savings_actual, 0),
                'total_spent': total_spent,
                'budget_health': self._calculate_budget_health(
                    needs_spent, needs_budget, wants_spent, wants_budget
                )
            }
            
        except Exception as e:
            print(f"Error calculating budget summary: {e}")
            return self._get_empty_budget_summary()
    
    def get_monthly_spending_by_category(self, month: str) -> Dict[str, float]:
        """Get spending breakdown by category for a specific month"""
        spending = defaultdict(float)
        
        try:
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        date = row.get('date', '')
                        if date.startswith(month):
                            category = row.get('category', 'others')
                            amount = float(row.get('amount', 0))
                            spending[category] += amount
                            
        except Exception as e:
            print(f"Error getting monthly spending: {e}")
        
        return dict(spending)
    
    def get_spending_insights(self, days: int = 30) -> Dict:
        """Generate spending insights for the last N days"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        insights = {
            'period_days': days,
            'total_spent': 0,
            'daily_average': 0,
            'top_category': None,
            'spending_trend': 'stable',
            'recommendations': []
        }
        
        try:
            daily_spending = defaultdict(float)
            category_spending = defaultdict(float)
            
            if os.path.exists(self.transactions_file):
                with open(self.transactions_file, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        date_str = row.get('date', '')
                        if date_str:
                            date = datetime.strptime(date_str, '%Y-%m-%d')
                            if start_date <= date <= end_date:
                                amount = float(row.get('amount', 0))
                                category = row.get('category', 'others')
                                
                                daily_spending[date_str] += amount
                                category_spending[category] += amount
                                insights['total_spent'] += amount
            
            # Calculate insights
            if insights['total_spent'] > 0:
                insights['daily_average'] = insights['total_spent'] / days
                
                # Find top category
                if category_spending:
                    insights['top_category'] = max(category_spending.items(), key=lambda x: x[1])
                
                # Analyze spending trend
                insights['spending_trend'] = self._analyze_spending_trend(daily_spending)
                
                # Generate recommendations
                insights['recommendations'] = self._generate_recommendations(
                    category_spending, insights['daily_average']
                )
        
        except Exception as e:
            print(f"Error generating insights: {e}")
        
        return insights
    
    def calculate_savings_rate(self, months: int = 3) -> float:
        """Calculate savings rate over the last N months"""
        try:
            # Get spending for last N months
            total_spent = 0
            current_date = datetime.now()
            
            for i in range(months):
                month_date = current_date - timedelta(days=30 * i)
                month_str = month_date.strftime('%Y-%m')
                monthly_spending = self.get_monthly_spending_by_category(month_str)
                total_spent += sum(monthly_spending.values())
            
            # Estimate income (simplified)
            balance_info = self.calculate_bank_balances()
            estimated_monthly_income = balance_info['total'] / months if months > 0 else 0
            total_income = estimated_monthly_income * months
            
            if total_income > 0:
                savings_rate = ((total_income - total_spent) / total_income) * 100
                return max(savings_rate, 0)  # Don't return negative savings rate
            
        except Exception as e:
            print(f"Error calculating savings rate: {e}")
        
        return 0.0
    
    def _calculate_budget_health(self, needs_spent: float, needs_budget: float,
                               wants_spent: float, wants_budget: float) -> str:
        """Calculate overall budget health score"""
        needs_ratio = needs_spent / needs_budget if needs_budget > 0 else 0
        wants_ratio = wants_spent / wants_budget if wants_budget > 0 else 0
        
        if needs_ratio <= 0.8 and wants_ratio <= 0.8:
            return 'excellent'
        elif needs_ratio <= 1.0 and wants_ratio <= 1.0:
            return 'good'
        elif needs_ratio <= 1.2 or wants_ratio <= 1.2:
            return 'fair'
        else:
            return 'poor'
    
    def _analyze_spending_trend(self, daily_spending: Dict[str, float]) -> str:
        """Analyze if spending is increasing, decreasing, or stable"""
        if len(daily_spending) < 7:
            return 'insufficient_data'
        
        # Get last 7 days and previous 7 days
        sorted_dates = sorted(daily_spending.keys())
        recent_week = sorted_dates[-7:]
        previous_week = sorted_dates[-14:-7] if len(sorted_dates) >= 14 else []
        
        if len(previous_week) < 7:
            return 'insufficient_data'
        
        recent_avg = sum(daily_spending[date] for date in recent_week) / 7
        previous_avg = sum(daily_spending[date] for date in previous_week) / 7
        
        if recent_avg > previous_avg * 1.1:
            return 'increasing'
        elif recent_avg < previous_avg * 0.9:
            return 'decreasing'
        else:
            return 'stable'
    
    def _generate_recommendations(self, category_spending: Dict[str, float], 
                                daily_average: float) -> List[str]:
        """Generate spending recommendations based on patterns"""
        recommendations = []
        
        # Find highest spending category
        if category_spending:
            top_category, top_amount = max(category_spending.items(), key=lambda x: x[1])
            
            # Category-specific recommendations
            if top_category == 'food' and top_amount > daily_average * 7:
                recommendations.append("Consider meal planning to reduce food expenses")
            elif top_category == 'transport' and top_amount > daily_average * 5:
                recommendations.append("Look into monthly passes or carpooling options")
            elif top_category == 'entertainment' and top_amount > daily_average * 4:
                recommendations.append("Try free entertainment options like parks or community events")
            elif top_category == 'shopping' and top_amount > daily_average * 10:
                recommendations.append("Implement a 24-hour waiting rule before purchases")
        
        # General recommendations based on daily average
        if daily_average > 500:
            recommendations.append("Your daily spending is quite high. Consider tracking smaller expenses")
        elif daily_average < 100:
            recommendations.append("Great job keeping expenses low! Consider increasing savings rate")
        
        return recommendations
    
    def _get_empty_budget_summary(self) -> Dict:
        """Return empty budget summary for error cases"""
        return {
            'month': datetime.now().strftime('%Y-%m'),
            'total_budget': 0,
            'needs_budget': 0,
            'needs_spent': 0,
            'needs_remaining': 0,
            'wants_budget': 0,
            'wants_spent': 0,
            'wants_remaining': 0,
            'savings_target': 0,
            'savings_actual': 0,
            'savings_shortfall': 0,
            'total_spent': 0,
            'budget_health': 'unknown'
        }

# Global calculator instance
_calculator = FinanceCalculator()

def calculate_balances() -> Dict:
    """Calculate current bank balances"""
    balance_info = _calculator.calculate_bank_balances()
    alerts = _calculator.check_low_balance_alerts()
    
    return {
        **balance_info,
        'alerts': alerts
    }

def check_balance_alerts() -> List[Dict]:
    """Check for low balance alerts"""
    return _calculator.check_low_balance_alerts()

def get_budget_summary(month: Optional[str] = None) -> Dict:
    """Get 50/30/20 budget summary"""
    return _calculator.calculate_monthly_budget_summary(month)

def get_spending_insights(days: int = 30) -> Dict:
    """Get spending insights for last N days"""
    return _calculator.get_spending_insights(days)

def get_savings_rate(months: int = 3) -> float:
    """Get savings rate for last N months"""
    return _calculator.calculate_savings_rate(months)

def get_financial_health_score() -> Dict:
    """Calculate overall financial health score"""
    try:
        balance_info = calculate_balances()
        budget_summary = get_budget_summary()
        savings_rate = get_savings_rate()
        
        # Calculate score based on multiple factors
        score = 0
        factors = []
        
        # Balance factor (30% weight)
        if balance_info['total'] > 10000:
            balance_score = min(balance_info['total'] / 50000 * 30, 30)
        else:
            balance_score = balance_info['total'] / 10000 * 30
        score += balance_score
        factors.append(f"Balance: {balance_score:.1f}/30")
        
        # Budget adherence factor (40% weight)
        budget_health = budget_summary.get('budget_health', 'unknown')
        budget_scores = {'excellent': 40, 'good': 30, 'fair': 20, 'poor': 10, 'unknown': 0}
        budget_score = budget_scores.get(budget_health, 0)
        score += budget_score
        factors.append(f"Budget: {budget_score}/40")
        
        # Savings rate factor (30% weight)
        if savings_rate >= 20:
            savings_score = 30
        elif savings_rate >= 10:
            savings_score = 20
        elif savings_rate >= 5:
            savings_score = 15
        else:
            savings_score = savings_rate
        score += savings_score
        factors.append(f"Savings: {savings_score:.1f}/30")
        
        # Determine grade
        if score >= 80:
            grade = 'A'
            status = 'Excellent'
        elif score >= 60:
            grade = 'B'
            status = 'Good'
        elif score >= 40:
            grade = 'C'
            status = 'Fair'
        else:
            grade = 'D'
            status = 'Needs Improvement'
        
        return {
            'score': round(score, 1),
            'grade': grade,
            'status': status,
            'factors': factors,
            'total_balance': balance_info['total'],
            'budget_health': budget_health,
            'savings_rate': savings_rate
        }
        
    except Exception as e:
        print(f"Error calculating financial health: {e}")
        return {
            'score': 0,
            'grade': 'N/A',
            'status': 'Unable to calculate',
            'factors': [],
            'total_balance': 0,
            'budget_health': 'unknown',
            'savings_rate': 0
        }

if __name__ == "__main__":
    # Test finance calculations
    print("🧮 Testing Finance Calculator")
    print("-" * 40)
    
    balances = calculate_balances()
    print(f"Total Balance: ₹{balances['total']:.2f}")
    
    budget = get_budget_summary()
    print(f"Budget Health: {budget['budget_health']}")
    
    insights = get_spending_insights(30)
    print(f"Daily Average: ₹{insights['daily_average']:.2f}")
    
    health = get_financial_health_score()
    print(f"Financial Health: {health['grade']} ({health['score']}/100)")
