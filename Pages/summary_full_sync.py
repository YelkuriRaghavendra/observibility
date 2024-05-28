import streamlit as st
import pandas as pd
import datetime
import sys
import os
from psycopg2 import sql
import calendar

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:/Users/yelku/Desktop/OPERATIONAL VISIBILITY')))
from Data_Base_Connection import fetch_data

def get_sync_summary(selected_date):
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
    result = fetch_data(query, (selected_date,))
    return result.iloc[0] if not result.empty else None

def main_page():
    st.title("FULL SYNC SUMMARY")

    # Initialize session state variables if not already set
    if 'selected_date' not in st.session_state:
        st.session_state['selected_date'] = datetime.date.today()

    selected_date = st.session_state['selected_date']
    selected_date_str = selected_date.strftime('%Y-%m-%d')
    selected_day_str = selected_date.strftime('%A')
    formatted_date_str = f"{selected_date.day} {calendar.month_name[selected_date.month]}, {selected_date.year}"

    st.markdown(f"<h2 class='large-font'>{formatted_date_str}  {selected_day_str}</h1>", unsafe_allow_html=True)

    def update_date():
        st.session_state['selected_date'] = st.session_state['date_input']

    if st.button('📅 Change Date', key='calendar_button'):
        st.date_input('Select a date', key='date_input', value=selected_date, on_change=update_date)

    # Fetch sync summary
    sync_summary = get_sync_summary(selected_date)
    
    if sync_summary is not None:
        total_syncs = int(sync_summary['total_syncs'])
        success_syncs = int(sync_summary['success_syncs'])
        failed_syncs = int(sync_summary['failed_syncs'])
    else:
        total_syncs = success_syncs = failed_syncs = 0

    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    if col1.button(f"Total Syncs: {total_syncs}", key='total_syncs'):
        st.session_state['page'] = 'total_syncs'
        st.rerun()

    if col2.button(f"Successful Syncs: {success_syncs}", key='success_syncs'):
        st.session_state['page'] = 'success_syncs'
        st.rerun()
    
    if col3.button(f"Failed Syncs: {failed_syncs}", key='failed_syncs'):
        st.session_state['page'] = 'failed_syncs'
        st.rerun()

def detailed_page(metric):
    st.title(f"Details for {metric.replace('_', ' ').capitalize()}")

    selected_date = st.session_state['selected_date']
    
    if metric == 'total_syncs':
        st.write(f"Total Syncs on {selected_date}: {st.session_state.get('total_syncs',0)}")
    elif metric == 'success_syncs':
        st.write(f"Successful Syncs on {selected_date}: {st.session_state.get('success_syncs',5)}")
    elif metric == 'failed_syncs':
        st.write(f"Failed Syncs on {selected_date}: {st.session_state.get('failed_syncs',10)}")
    
    if st.button('Go Back'):
        st.session_state['page'] = 'main'
        st.experimental_rerun()

def main():
    page = st.session_state.get('page', 'main')
    
    if page == 'main':
        main_page()
    elif page in ['total_syncs', 'success_syncs', 'failed_syncs']:
        detailed_page(page)

if __name__ == "__main__":
    main()
