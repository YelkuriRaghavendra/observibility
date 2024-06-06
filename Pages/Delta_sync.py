import streamlit as st
from db_init import fetch_data
import pandas as pd

# Function to get distinct node_ids, node_names, and node_types with "STOCKS_UPDATED" events for a selected date
def get_nodes_for_date(selected_date):
    query = """
    SELECT DISTINCT ss.node_id::text, nl.node_name, nl.node_type
    FROM supply_summary ss
    JOIN node_lookup nl ON ss.node_id::text = nl.node_id::text
    WHERE ss.last_source_update_event = 'STOCKS_UPDATED'
    AND DATE(ss.last_source_updated_at) = %s;
    """
    result = fetch_data(query, (selected_date,))
    if not result.empty:
        return result.set_index('node_id').to_dict('index')
    else:
        return {}

# Function to fetch the selected data
def fetch_selected_data(table_name, selected_date, selected_node_ids):
    node_id_placeholders = ', '.join(['%s'] * len(selected_node_ids))
    query = f"""
    SELECT *
    FROM supply_summary
    WHERE last_source_update_event = 'STOCKS_UPDATED'
    AND DATE(last_source_updated_at) = %s
    AND node_id::text IN ({node_id_placeholders});
    """
    params = (selected_date,) + tuple(selected_node_ids)
    result = fetch_data(query, params)
    return result

# Streamlit UI
st.title('DELTA_SYNC')

# Create columns for date and type selection
col1, col2 = st.columns(2)

with col1:
    # Date input
    selected_date = st.date_input("Select a date")

with col2:
    # Type selection
    type_selection = st.selectbox("Select Type", ["1P", "3P"])

# Map type selection to node_type filter
node_type_filter = None
if type_selection == "1P":
    node_type_filter = ("WAREHOUSE", "STORE", "SELLER")
elif type_selection == "3P":
    node_type_filter = ("_3PL",)

if selected_date and node_type_filter:
    # Fetch distinct node_ids and node_names with "STOCKS_UPDATED" events for the selected date and type
    nodes = get_nodes_for_date(selected_date)
    
    if nodes:
        # Filter nodes based on the selected type
        filtered_nodes = {
            node_id: details for node_id, details in nodes.items()
            if details['node_type'] in node_type_filter
        }
        
        if filtered_nodes:
            # Prepare node name options
            node_names = [details['node_name'] for details in filtered_nodes.values()]
            
            # Display a multiselect dropdown to select node names
            selected_node_names = st.multiselect("Select Node Names", node_names)
            
            if selected_node_names:
                # Find the corresponding node_ids for the selected node_names
                selected_node_ids = [
                    node_id for node_id, details in filtered_nodes.items()
                    if details['node_name'] in selected_node_names
                ]
                
                # Fetch and display the selected data
                selected_data = fetch_selected_data("supply_summary", selected_date, selected_node_ids)
                st.write(selected_data)
        else:
            st.write(f"No node names with 'STOCKS_UPDATED' events present for the selected date and type {type_selection}.")
    else:
        st.write(f"No node names with 'STOCKS_UPDATED' events present for the selected date and type {type_selection}.")
