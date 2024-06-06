import streamlit as st
from db_init import fetch_data
import pandas as pd

def get_fullsync_count():
    query = """
    SELECT COUNT(*) 
    FROM supply_summary 
    WHERE last_source_update_event = 'FULL_SYNC' 
    AND last_updated_at IS NOT NULL
    AND last_updated_at::timestamptz >= current_date - interval '7 days'
    """
    result = fetch_data(query)
    return result.iloc[0, 0] if not result.empty else 0

def get_mismatch_count():
    query = """
    SELECT COUNT(*) 
    FROM supply_node_full_sync_mismatch_log 
    WHERE created_at::timestamptz >= current_date - interval '7 days'
    """
    result = fetch_data(query)
    return result.iloc[0, 0] if not result.empty else 0

def main():
    st.title("Dashboard")

    # Display metrics
    fullsync_count = get_fullsync_count()
    mismatch_count = get_mismatch_count()

    col1, col2 = st.columns(2)
    col1.metric(label="Fullsync Count", value=fullsync_count)
    col2.metric(label="Mismatch Count", value=mismatch_count)


if __name__ == "__main__":
    main()
