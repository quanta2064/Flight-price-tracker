import sqlite3


def create_database():
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()

    # 1. Our existing prices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        price REAL NOT NULL,
        date_checked TEXT NOT NULL
    )
    """)

    # 2. NEW: The routes table to store what paths we care about
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS routes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        UNIQUE(origin, destination) -- Prevents adding duplicates
    )
    """)

    conn.commit()
    conn.close()

def get_tracked_routes():
    """Returns a list of tuples representing all tracked routes, e.g., [('KTM', 'TYO'), ('KTM', 'DEL')]"""
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT origin, destination FROM routes")
    routes = cursor.fetchall()
    
    conn.close()
    return routes

def add_route(origin, destination):
    """Helper function to easily seed new routes into the database"""
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT OR IGNORE INTO routes (origin, destination) VALUES (?, ?)", (origin, destination))
        conn.commit()
    except Exception as e:
        print(f"Error adding route: {e}")
    finally:
        conn.close()


def save_price(origin, destination, price, date_checked):

    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO prices(origin, destination, price, date_checked)
    VALUES (?, ?, ?, ?)
    """, (origin, destination, price, date_checked))

    conn.commit()
    conn.close()

    print("Price saved successfully!")

def get_historical_min(origin, destination):
    conn = sqlite3.connect("prices.db")
    cursor = conn.cursor()
    
    # SQL query to find the lowest price for a specific route
    cursor.execute("""
        SELECT MIN(price) FROM prices 
        WHERE origin = ? AND destination = ?
    """, (origin, destination,))
    
    # fetchone() returns a tuple like (45000.0,) or (None,) if empty
    result = cursor.fetchone()[0]
    
    conn.close()
    return result