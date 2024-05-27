import streamlit as st
import pandas as pd
import datetime
import sys
import os
from psycopg2 import sql
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/yelku/Desktop/OPERATIONAL VISIBILITY')))
from Data_Base_Connection import fetch_data

# Streamlit app
st.title('Supply Node Full Sync Summary')

# Date input from user
selected_date = st.date_input('Select a date', value=datetime.date.today())

# Query to get sync summary for a specific date
query = sql.SQL("""
    SELECT 
        DATE(supply_activity_log_created_at) AS sync_date,
        COUNT(*) AS total_syncs,
        SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) AS success_syncs,
        SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) AS failed_syncs
    FROM 
        supply_node_full_sync_summary
    WHERE 
        DATE(supply_activity_log_created_at) = %s
    GROUP BY 
        sync_date
    ORDER BY 
        sync_date;
""")

# Button to trigger the query
if st.button('Get Sync Summary'):
    sync_summary_df = fetch_data(query, (selected_date,))
    
    if not sync_summary_df.empty:
        sync_summary = sync_summary_df.iloc[0]
        st.write(f"### Sync Summary for {sync_summary['sync_date']}")
        st.metric(label="Total Syncs", value=int(sync_summary['total_syncs']))
        st.metric(label="Successful Syncs", value=int(sync_summary['success_syncs']))
        st.metric(label="Failed Syncs", value=int(sync_summary['failed_syncs']))
    else:
        st.write("No data found for the selected date.")
        
        
