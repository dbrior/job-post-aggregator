import streamlit as st
import psycopg2
import pandas as pd
import os

# Database connection function
def get_db_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")
    return psycopg2.connect(DATABASE_URL)

# Fetch all data from the table
def fetch_table_data(table_name):
    conn = get_db_connection()
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Config
st.set_page_config(page_title="Job Listings", layout="centered")

# Streamlit UI
st.title("Job Listings")
TABLE_NAME = 'listings'
try:
    df = fetch_table_data(TABLE_NAME)
    
    # Get unique firms with prettified names
    firms = sorted(df['firm'].unique())
    prettified_firms = {firm: firm.replace('_', ' ').title() for firm in firms}
    
    # Multi-select filter with default "All" text
    selected_firms = st.multiselect("Filter by Firm:", list(prettified_firms.values()), default=[], placeholder="All")
    
    # Apply filter only if firms are selected
    if selected_firms:
        selected_firm_keys = [key for key, value in prettified_firms.items() if value in selected_firms]
        df = df[df['firm'].isin(selected_firm_keys)]
    
    st.write(f"{len(df)} job postings:")
    
    for _, row in df.iterrows():
        col1, col2 = st.columns([1.2,1], vertical_alignment="center")
        with col1:
            st.markdown(
                f"<div style='text-align: left; font-size: 1.5em'><a href='{row['url']}' target='_blank'>{row['title'].replace('\n', ' - ')}</a></div>",
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(f"<div style='text-align: right;'>{row['firm'].replace('_', ' ').title()}</div>", unsafe_allow_html=True)
        
        st.text(row['location'].split('\n')[0].replace('unknown_location', 'Unknown Location'))
        st.markdown("<hr style='margin-top: 10px; margin-bottom: 10px;'>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"Error loading data: {e}")
