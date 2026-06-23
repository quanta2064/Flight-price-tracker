import streamlit as st
import sqlite3
import pandas as pd

# Set up page styling
st.set_page_config(page_title="Flight Price Tracker", page_icon="✈️", layout="wide")

st.title("✈️ Flight Price Historical Dashboard")
st.markdown("Track price fluctuations, trends, and historical minimums over time.")

# 1. Fetch data from SQLite into a Pandas DataFrame
def load_data():
    conn = sqlite3.connect("prices.db")
    # Read the data straight into a dataframe
    query = "SELECT origin, destination, price, date_checked FROM prices ORDER BY date_checked ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

df = load_data()

# Check if we actually have data to display
if df.empty:
    st.warning("No data found in the database yet. Run your tracker script first!")
else:
    # 2. Key Metrics Display (Top Row)
    latest_price = df['price'].iloc[-1]
    lowest_price = df['price'].min()
    total_checks = len(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Latest Scraped Price", value=f"₹{latest_price:,.2f}")
    with col2:
        st.metric(label="Historical Lowest Price", value=f"₹{lowest_price:,.2f}")
    with col3:
        st.metric(label="Total Tracking Days", value=total_checks)

    st.markdown("---")

    # 3. Interactive Route Filter
    # Creates a unique list of routes like ["KTM -> TYO"]
    df['route'] = df['origin'] + " → " + df['destination']
    unique_routes = df['route'].unique()
    selected_route = st.selectbox("Select Route to View:", unique_routes)

    # Filter data based on selection
    filtered_df = df[df['route'] == selected_route]

    # 4. Data Visualization Chart
    st.subheader(f"📈 Price Trend over Time: {selected_route}")
    
    # Streamlit natively draws a clean interactive line chart
    st.line_chart(data=filtered_df, x='date_checked', y='price', use_container_width=True)

    # 5. Show Raw Data Table
    st.subheader("📋 Historical Logs")
    st.dataframe(filtered_df[['date_checked', 'price']].sort_values(by='date_checked', ascending=False), use_container_width=True)