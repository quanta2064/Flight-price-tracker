import sqlite3


def create_database():
    conn = sqlite3.connect("prices.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS prices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        price REAL NOT NULL,
        date_checked TEXT NOT NULL
    )
    """)

    conn.commit()
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