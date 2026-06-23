# Flight-price-tracker
A Python-based flight fare tracker that monitors ticket prices, stores historical data, and notifies users of price drops.

# Multi-Route Flight Price Tracker

A modular Python application designed to track flight fare trends across multiple routes, log historical data using an embedded SQLite database, send notifications via Telegram when prices drop, and display data via a Streamlit web dashboard.

## Architecture Overview

* Automation: Designed for scheduled execution to poll data points over time.
* Database Layer: SQLite tracks pricing history and handles historical minimum calculations.
* Notification System: Dispatches HTML-formatted Telegram messages when a new low price is registered.
* User Interface: Streamlit dashboard displaying historical price charts and tracked route tables.

## Setup Instructions

1. Clone the repository:
   git clone https://github.com/YOUR_USERNAME/flight-price-tracker.git

2. Create and activate a virtual environment:
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate

3. Install required packages:
   pip install requests streamlit beautifulsoup4

4. Create a local config.py file in the root directory containing your TELEGRAM_TOKEN and TELEGRAM_CHAT_ID.

5. Run the web interface:
   streamlit run dashboard.py