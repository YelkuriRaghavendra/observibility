import streamlit as st
import pandas as pd
import datetime
import sys
import os
from psycopg2 import sql
import calendar

from Pages.full_sync_details.node_viz import detailed_page
from db_init import fetch_data

@st.cache_resource
def get_sync_summary(selected_date):
    query = sql.SQL("""
        SELECT 
            DATE(supply_activity_log_created_at) AS sync_date,
            COUNT(*) AS total_syncs,
            SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) AS success_syncs,
            SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed_syncs,
            SUM (CASE WHEN status = 'STARTED' THEN 1 ELSE 0 END) AS started_syncs
        FROM 
            supply_node_full_sync_summary
        WHERE 
            DATE(supply_activity_log_created_at) = %s
        GROUP BY 
            sync_date
        ORDER BY 
            sync_date;
    """)
    result = fetch_data(query, (selected_date,))
    return result.iloc[0] if not result.empty else None

def main_page():
    st.title("FULL SYNC SUMMARY")

    # Initialize session state variables if not already set
    if 'selected_date' not in st.session_state:
        st.session_state['selected_date'] = datetime.date.today()

    selected_date = st.session_state['selected_date']
    # selected_date_str = selected_date.strftime('%Y-%m-%d')
    selected_day_str = selected_date.strftime('%A')
    formatted_date_str = f"{selected_date.day} {calendar.month_name[selected_date.month]}, {selected_date.year}"

    def update_date():
        st.session_state['selected_date'] = st.session_state['date_input']

    st.markdown(f"<h2 class='large-font'>{formatted_date_str}  {selected_day_str}</h1>", unsafe_allow_html=True)

    if st.button('📅 Change Date', key='calendar_button'):
        st.date_input('Select a date', key='date_input', value=selected_date, on_change=update_date)


    # Fetch sync summary
    sync_summary = get_sync_summary(selected_date)
    
    if sync_summary is not None:
        total_syncs = int(sync_summary['total_syncs'])
        success_syncs = int(sync_summary['success_syncs'])
        failed_syncs = int(sync_summary['failed_syncs'])
        started_syncs = int(sync_summary['started_syncs'])
    else:
        total_syncs = success_syncs = failed_syncs= started_syncs = 0

    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button(f"Total Syncs: {total_syncs}", key='total_syncs',use_container_width=150):
        st.session_state['page'] = 'total_syncs'
        st.rerun()

    if col2.button(f"Successful Syncs: {success_syncs}", key='success_syncs',use_container_width=150):
        st.session_state['page'] = 'success_syncs'
        st.rerun()
    
    if col3.button(f"Failed Syncs: {failed_syncs}", key='failed_syncs',use_container_width=150):
        st.session_state['page'] = 'failed_syncs'
        st.rerun()
    
    if col4.button(f"Started Syncs: {started_syncs}", key='started_syncs',use_container_width=150):
        st.session_state['page'] = 'started_syncs'
        st.rerun()


def main():
    page = st.session_state.get('page', 'main')
    
    if page == 'main':
        main_page()
    elif page in ['total_syncs', 'success_syncs', 'failed_syncs','started_syncs']:
        detailed_page(page)

if __name__ == "__main__":
    main()
