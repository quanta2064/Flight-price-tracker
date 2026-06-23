import os
from datetime import datetime
from database import create_database, save_price, get_historical_min, get_tracked_routes, add_route
# Connect directly to your dynamic pricing simulation engine
from fetch_price import get_current_price 

def send_telegram_alert(origin, destination, price, previous_low):
    import requests
    from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
    
    message = (
        f"🚨 <b>New Cheapest Flight Found!</b> 🚨\n\n"
        f"✈️ <b>Route:</b> {origin} → {destination}\n"
        f"💰 <b>New Low:</b> ₹{price:,.2f}\n"
        f"📉 <b>Previous Low:</b> ₹{previous_low:,.2f}"
    )
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram alert sent successfully!")
        else:
            print(f"Failed to send Telegram alert: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending alert: {e}")

def main():
    create_database()
    
    # Track profiles configuration
    add_route("KTM", "TYO")
    add_route("KTM", "DEL")
    add_route("KTM", "SIN")
    
    routes_to_track = get_tracked_routes()
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Loaded routes from tracking profile: {routes_to_track}")
    
    for origin, destination in routes_to_track:
        print(f"\nProcessing Route: {origin} ➔ {destination}")
        
        # Pull the randomized market price from your engine
        current_price = get_current_price(origin, destination)
        
        if current_price is None:
            print(f"Skipping {origin} -> {destination} due to an error.")
            continue
            
        historical_low = get_historical_min(origin, destination)
        
        if historical_low is None:
            print(f"First entry for {origin} -> {destination}. Saving baseline price: ₹{current_price:,.2f}")
            save_price(origin, destination, current_price, today_date)
        elif current_price < historical_low:
            print(f"🚨 ALERT! Price drop on {origin} -> {destination}! Was ₹{historical_low:,.2f}, now ₹{current_price:,.2f}!")
            send_telegram_alert(origin, destination, current_price, historical_low)
            save_price(origin, destination, current_price, today_date)
        else:
            print(f"No drop for {origin} -> {destination}. Current: ₹{current_price:,.2f} | Low: ₹{historical_low:,.2f}")
            save_price(origin, destination, current_price, today_date)

if __name__ == "__main__":
    main()