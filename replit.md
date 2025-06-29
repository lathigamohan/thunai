# Finla - Premium Personal Finance Tracker

## Overview

Finla is a sophisticated single-user personal finance web application built with Flask, featuring a premium black and gold theme. The application focuses on expense tracking, bank account management, savings goals, and user engagement through gamification elements. It includes Progressive Web App (PWA) capabilities for mobile installation and offline functionality.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Data Storage**: File-based system using JSON and CSV
  - `banks.json`: Bank account information and UPI app mappings
  - `transactions.csv`: All transaction records
  - `goals.json`: Savings goals data
  - `user_stats.json`: Gamification data (streaks, karma points, achievements)
- **File Structure**: Modular utility system with separate modules for categorization, finance calculations, gamification, and quotes

### Frontend Architecture
- **Styling**: Bootstrap 5 with custom CSS for black and gold theme
- **JavaScript**: Vanilla JS with Chart.js for data visualization
- **Responsive Design**: Mobile-first approach with PWA support
- **Internationalization**: Bilingual support (Tamil and English) for motivational quotes

### PWA Implementation
- **Manifest**: `manifest.json` for app installation metadata
- **Service Worker**: Caching strategy for offline functionality
- **Installation**: Support for mobile and desktop app installation

## Key Components

### Core Modules

#### 1. Transaction Management (`app.py`)
- Manual transaction entry with automatic categorization
- CSV bulk upload functionality
- Transaction validation and processing
- Integration with gamification system for streak tracking

#### 2. Smart Categorization (`utils/categorize.py`)
- Keyword-based automatic expense categorization
- Categories include: food, transport, education, snacks, shopping, bills, entertainment, health, personal, and miscellaneous
- Priority-based categorization system
- Tamil and English keyword support

#### 3. Financial Calculations (`utils/finance.py`)
- Real-time balance calculation for multiple bank accounts
- 50/30/20 budget analysis (needs/wants/savings)
- Low balance alerts and notifications
- Spending pattern analysis

#### 4. Gamification System (`utils/gamification.py`)
- Daily streak tracking for transaction logging
- Karma points system for mindful spending
- Achievement system with milestone rewards
- User level progression
- Streak freeze protection tokens

#### 5. Quote System (`utils/quotes.py`)
- Daily motivational quotes from Thirukkural, Warren Buffett, and AI-generated wisdom
- Bilingual support with Tamil translations
- Category-based quote selection

### User Interface Components

#### Templates
- `base.html`: Common layout with navigation and PWA meta tags
- `index.html`: Dashboard with daily quotes, user stats, and balance overview
- `add_transaction.html`: Manual transaction entry form
- `upload.html`: CSV bulk upload interface
- `banks.html`: Bank account management
- `goals.html`: Savings goals tracking
- `analytics.html`: Financial insights and charts

#### Static Assets
- `style.css`: Premium black and gold theme styling
- `scripts.js`: Client-side functionality and PWA management
- `charts.js`: Chart.js configuration for financial visualizations
- `service-worker.js`: PWA offline functionality

## Data Flow

### Transaction Processing Flow
1. User enters transaction (manual or CSV upload)
2. Transaction gets automatically categorized using keyword matching
3. Bank balance is updated in real-time
4. Gamification system updates streak and karma points
5. Achievement system checks for new milestones
6. Budget analysis is recalculated
7. User stats are persisted to JSON file

### Data Persistence Strategy
- **JSON Files**: Used for structured data (banks, goals, user stats)
- **CSV Files**: Used for transaction records for easy import/export
- **File-based approach**: Chosen for simplicity and Replit compatibility
- **No external database**: Reduces complexity and hosting requirements

## External Dependencies

### Frontend Libraries (CDN)
- Bootstrap 5.3.0: UI framework and responsive design
- Font Awesome 6.4.0: Icon library
- Chart.js: Data visualization and analytics charts
- Google Fonts: Typography (Inter and Noto Sans Tamil)

### Python Dependencies
- Flask: Web framework
- Standard library modules: os, csv, json, datetime, logging
- No external database drivers required

### Third-party Integrations
- **UPI Apps**: Support for GPay, PhonePe, Paytm, and BHIM integration
- **Bank Accounts**: Multi-bank account management
- **No API integrations**: Fully self-contained system

## Deployment Strategy

### Replit Deployment
- **Entry Point**: `main.py` runs the Flask application
- **Port Configuration**: Uses port 5000 with host binding to 0.0.0.0
- **File Persistence**: Data stored in `/data` directory
- **Environment Variables**: `SESSION_SECRET` for Flask session security

### PWA Deployment
- **Manifest Configuration**: Supports installation on mobile and desktop
- **Service Worker**: Provides offline functionality and caching
- **Icon Generation**: SVG-based icons for different sizes
- **Theme Integration**: Matches black and gold color scheme

### Development vs Production
- **Debug Mode**: Enabled in development for detailed error logging
- **Secret Key**: Uses environment variable or fallback for session management
- **Static Assets**: Served directly by Flask in development
- **Data Directory**: Automatically created on first run

## Changelog

```
Changelog:
- June 29, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```