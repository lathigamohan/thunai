import os
import csv
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from werkzeug.utils import secure_filename
from utils.categorize import categorize_transaction
from utils.finance import calculate_balances, check_balance_alerts, get_budget_summary
from utils.quotes import get_daily_quote
from utils.gamification import update_streak, get_user_stats, update_karma_points

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "finla_secret_key_2025")

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize data files if they don't exist
def init_data_files():
    # Initialize banks.json
    if not os.path.exists('data/banks.json'):
        with open('data/banks.json', 'w') as f:
            json.dump({}, f)
    
    # Initialize transactions.csv
    if not os.path.exists('data/transactions.csv'):
        with open('data/transactions.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'amount', 'description', 'category', 'payment_method', 'bank'])
    
    # Initialize goals.json
    if not os.path.exists('data/goals.json'):
        with open('data/goals.json', 'w') as f:
            json.dump([], f)
    
    # Initialize user_stats.json
    if not os.path.exists('data/user_stats.json'):
        with open('data/user_stats.json', 'w') as f:
            json.dump({
                'streak': 0,
                'last_entry_date': '',
                'karma_points': 0,
                'total_transactions': 0,
                'achievements': []
            }, f)

init_data_files()

@app.route('/')
def index():
    """Home page with daily quote, balance, and visualizations"""
    quote = get_daily_quote()
    balances = calculate_balances()
    alerts = check_balance_alerts()
    budget_summary = get_budget_summary()
    user_stats = get_user_stats()
    
    # Get recent transactions for quick view
    recent_transactions = []
    try:
        with open('data/transactions.csv', 'r') as f:
            reader = csv.DictReader(f)
            transactions = list(reader)
            recent_transactions = sorted(transactions, key=lambda x: x['date'], reverse=True)[:5]
    except Exception as e:
        logging.error(f"Error reading transactions: {e}")
    
    return render_template('index.html', 
                         quote=quote,
                         balances=balances,
                         alerts=alerts,
                         budget_summary=budget_summary,
                         user_stats=user_stats,
                         recent_transactions=recent_transactions)

@app.route('/add_transaction', methods=['GET', 'POST'])
def add_transaction():
    """Add manual transaction entry"""
    if request.method == 'POST':
        try:
            amount = float(request.form['amount'])
            description = request.form['description']
            payment_method = request.form['payment_method']
            date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))
            
            # Get bank info
            with open('data/banks.json', 'r') as f:
                banks = json.load(f)
            
            bank = ''
            if payment_method in banks:
                bank = payment_method
            else:
                # Find linked bank for UPI
                for bank_name, bank_info in banks.items():
                    if bank_info.get('upi_apps') and payment_method in bank_info['upi_apps']:
                        bank = bank_name
                        break
            
            # Categorize transaction
            category = categorize_transaction(description)
            
            # Save transaction
            with open('data/transactions.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([date, amount, description, category, payment_method, bank])
            
            # Update streak and karma points
            update_streak()
            update_karma_points(category, amount)
            
            flash('Transaction added successfully!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            logging.error(f"Error adding transaction: {e}")
            flash('Error adding transaction. Please try again.', 'error')
    
    # Get banks and UPI apps for form
    with open('data/banks.json', 'r') as f:
        banks = json.load(f)
    
    # Get today's date for the form
    today_date = datetime.now().strftime('%Y-%m-%d')
    
    return render_template('add_transaction.html', banks=banks, today_date=today_date)

@app.route('/upload', methods=['GET', 'POST'])
def upload_transactions():
    """Upload CSV file with multiple transactions"""
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and file.filename and str(file.filename).endswith('.csv'):
            try:
                # Read uploaded CSV
                content = file.read().decode('utf-8')
                csv_reader = csv.DictReader(content.splitlines())
                
                transactions_added = 0
                with open('data/transactions.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    
                    for row in csv_reader:
                        amount = float(row.get('amount', 0))
                        description = row.get('description', '')
                        payment_method = row.get('payment_method', '')
                        date = row.get('date', datetime.now().strftime('%Y-%m-%d'))
                        
                        # Get bank for payment method
                        with open('data/banks.json', 'r') as bank_file:
                            banks = json.load(bank_file)
                        
                        bank = ''
                        if payment_method in banks:
                            bank = payment_method
                        else:
                            for bank_name, bank_info in banks.items():
                                if bank_info.get('upi_apps') and payment_method in bank_info['upi_apps']:
                                    bank = bank_name
                                    break
                        
                        category = categorize_transaction(description)
                        writer.writerow([date, amount, description, category, payment_method, bank])
                        transactions_added += 1
                
                update_streak()
                flash(f'{transactions_added} transactions uploaded successfully!', 'success')
                return redirect(url_for('index'))
                
            except Exception as e:
                logging.error(f"Error uploading file: {e}")
                flash('Error processing file. Please check format.', 'error')
        else:
            flash('Please upload a CSV file', 'error')
    
    return render_template('upload.html')

@app.route('/analytics')
def analytics():
    """Analytics dashboard with charts and insights"""
    balances = calculate_balances()
    budget_summary = get_budget_summary()
    
    # Get transaction data for charts
    transactions = []
    try:
        with open('data/transactions.csv', 'r') as f:
            reader = csv.DictReader(f)
            transactions = list(reader)
    except Exception as e:
        logging.error(f"Error reading transactions: {e}")
    
    return render_template('analytics.html', 
                         balances=balances,
                         budget_summary=budget_summary,
                         transactions=transactions)

@app.route('/banks', methods=['GET', 'POST'])
def manage_banks():
    """Manage bank accounts and UPI apps"""
    if request.method == 'POST':
        try:
            bank_name = request.form['bank_name']
            initial_balance = float(request.form['initial_balance'])
            min_balance = float(request.form['min_balance'])
            upi_apps = request.form.getlist('upi_apps')
            
            with open('data/banks.json', 'r') as f:
                banks = json.load(f)
            
            banks[bank_name] = {
                'initial_balance': initial_balance,
                'min_balance': min_balance,
                'upi_apps': upi_apps
            }
            
            with open('data/banks.json', 'w') as f:
                json.dump(banks, f, indent=2)
            
            flash('Bank added successfully!', 'success')
            return redirect(url_for('manage_banks'))
            
        except Exception as e:
            logging.error(f"Error adding bank: {e}")
            flash('Error adding bank. Please try again.', 'error')
    
    with open('data/banks.json', 'r') as f:
        banks = json.load(f)
    
    balances = calculate_balances()
    
    return render_template('banks.html', banks=banks, balances=balances)

@app.route('/goals', methods=['GET', 'POST'])
def manage_goals():
    """Manage savings goals"""
    if request.method == 'POST':
        try:
            goal_name = request.form['goal_name']
            target_amount = float(request.form['target_amount'])
            target_date = request.form['target_date']
            current_amount = float(request.form.get('current_amount', 0))
            
            with open('data/goals.json', 'r') as f:
                goals = json.load(f)
            
            new_goal = {
                'id': len(goals) + 1,
                'name': goal_name,
                'target_amount': target_amount,
                'current_amount': current_amount,
                'target_date': target_date,
                'created_date': datetime.now().strftime('%Y-%m-%d')
            }
            
            goals.append(new_goal)
            
            with open('data/goals.json', 'w') as f:
                json.dump(goals, f, indent=2)
            
            flash('Goal added successfully!', 'success')
            return redirect(url_for('manage_goals'))
            
        except Exception as e:
            logging.error(f"Error adding goal: {e}")
            flash('Error adding goal. Please try again.', 'error')
    
    with open('data/goals.json', 'r') as f:
        goals = json.load(f)
    
    return render_template('goals.html', goals=goals)

@app.route('/api/chart_data')
def chart_data():
    """API endpoint for chart data"""
    try:
        with open('data/transactions.csv', 'r') as f:
            reader = csv.DictReader(f)
            transactions = list(reader)
        
        # Process data for charts
        category_data = {}
        daily_data = {}
        
        for transaction in transactions:
            category = transaction['category']
            amount = float(transaction['amount'])
            date = transaction['date']
            
            # Category totals
            category_data[category] = category_data.get(category, 0) + amount
            
            # Daily totals
            daily_data[date] = daily_data.get(date, 0) + amount
        
        return jsonify({
            'categories': category_data,
            'daily': daily_data
        })
        
    except Exception as e:
        logging.error(f"Error getting chart data: {e}")
        return jsonify({'error': 'Failed to load chart data'})

@app.route('/export_transactions')
def export_transactions():
    """Export transactions as CSV"""
    try:
        return send_file('data/transactions.csv', 
                        as_attachment=True, 
                        download_name=f'finla_transactions_{datetime.now().strftime("%Y%m%d")}.csv')
    except Exception as e:
        logging.error(f"Error exporting transactions: {e}")
        flash('Error exporting transactions', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
