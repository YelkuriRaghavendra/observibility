import streamlit as st
from psycopg2 import sql
from db_init import fetch_data

import plotly.express as px

def create_pie_chart(df, column):
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, 'count']
    pie_chart = px.pie(counts, values='count', names=column, title=f'Pie Chart of full syncs')
    return pie_chart


def get_sync_summary_node(selected_date, include_all_statuses,status="all"):
    query = sql.SQL("""
        SELECT *
        FROM 
            supply_node_full_sync_summary
        WHERE 
            DATE(supply_activity_log_created_at) = %s AND (%s OR status = %s)
    """)
    
    params = (selected_date, include_all_statuses,status) 

    result = fetch_data(query, params)
    return result if not result.empty else None

def get_business_summary_syncs(selected_date,include_all_statuses=False,status="all"):
    query = sql.SQL("""
    SELECT 
        t1.*,
        t2.node_id,
        t2.node_name,
        t2.node_type           
    FROM 
        supply_node_full_sync_summary t1
    JOIN 
        node_lookup t2 ON t1.node_code::text = t2.node_code::text
    WHERE 
        DATE(supply_activity_log_created_at) = %s 
        AND (%s OR status = %s)
""")
    
    params = (selected_date, include_all_statuses,status) 

    result = fetch_data(query, params)
    return result if not result.empty else []

def get_job_activity_records(job_activity_id):
    query = sql.SQL("""
        SELECT *
        FROM 
           supply_activity_item_log
        WHERE 
            supply_activity_log_job_id = %s 
    """)
    
    params = (job_activity_id,) 

    result = fetch_data(query, params)
    return result if not result.empty else []

def get_item_count_node(node_name,job_activity_id):
    query = sql.SQL("""
        SELECT *
        FROM supply_node_full_sync_summary t1
        JOIN node_lookup nm ON t1.node_code::text = nm.node_code::text
        JOIN supply_summary t2 ON nm.node_id::text = t2.node_id::text
        WHERE t2.created_at < t1.completed_at
        AND t1.supply_activity_log_job_id = %s AND nm.node_name = %s;
    """)
    
    params = (job_activity_id,node_name,) 

    result = fetch_data(query, params)
    return result if not result.empty else []

def get_mismatch_count_full_sync(activity_log_job_id):
    query = sql.SQL("""
       SELECT j.*, m.mismatch_type, m.updated_quantity
        FROM supply_activity_item_log j
        JOIN supply_node_full_sync_mismatch_log m ON j.id = m.supply_activity_item_log_id
        WHERE j.supply_activity_log_job_id = %s;
    """)
    
    params = (activity_log_job_id,) 

    result = fetch_data(query, params)
    return result if not result.empty else []



def detailed_page(metric):
    st.title(f"Details for {metric.replace('_', ' ').capitalize()}")

    selected_date = st.session_state['selected_date']

    status = "all" 
    include_all_statuses = False
    if metric=="total_syncs":
        status = "all"
        include_all_statuses = True
    elif metric == "success_syncs":
        status = "COMPLETED"
    elif metric == "failed_syncs":
        status = "FAILED"
    elif metric == "started_syncs":
        status = "STARTED"
    
    # sync_summary = get_sync_summary_node(selected_date,include_all_statuses,status)

   # Initialize session state variables
    if 'selected_node_id' not in st.session_state:
        st.session_state.selected_node_id = None

    if 'selected_job_activity_id' not in st.session_state:
        st.session_state.selected_job_activity_id = None

    if 'display_summary' not in st.session_state:
        st.session_state.display_summary = None

    # Function to display sync summary and select box
    def display_sync_summary(sync_summary, key_prefix):
        if len(sync_summary):
            st.dataframe(sync_summary)
            node_ids = ['None'] + list(sync_summary['node_name'].unique())
            selected_node_id = st.selectbox('Select Node ID', node_ids, key=f'{key_prefix}_node_name_select')
            st.session_state.selected_node_id = selected_node_id if selected_node_id != 'None' else None

            if st.session_state.selected_node_id:
                filtered_data = sync_summary[sync_summary['node_name'] == st.session_state.selected_node_id]
                st.write(f"Data for Node ID: {st.session_state.selected_node_id}")
                st.dataframe(filtered_data)

                # Only show job_activity_id select box if filtered_data is not empty
                job_activity_ids = ['None'] + list(filtered_data['supply_activity_log_job_id'].unique())
                selected_job_activity_id = st.selectbox(
                    'Select Job Activity ID', 
                    job_activity_ids, 
                    key=f'{key_prefix}_job_activity_id_select'
                )
                st.session_state.selected_job_activity_id = selected_job_activity_id if selected_job_activity_id != 'None' else None

                # Only display details if a valid job_activity_id is selected
                if st.session_state.selected_job_activity_id:
                    job_activity_details = get_job_activity_records(st.session_state.selected_job_activity_id)
                    st.write(f"Details for Job Activity ID: {st.session_state.selected_job_activity_id}")

                    count = get_item_count_node(job_activity_id=st.session_state.selected_job_activity_id,node_name=st.session_state.selected_node_id)
                    mismatch = get_mismatch_count_full_sync(st.session_state.selected_job_activity_id)

                    print(count)
                    
                    if (len(mismatch)>0):
                        mismatch_new_additions_count = len( mismatch[(mismatch['mismatch_type'] == 'INSERT')])
                        mismatch_out_of_stock_count = len (mismatch[(mismatch['mismatch_type'] == 'UPDATE') & (mismatch['updated_quantity'] == 0)])
                        mismatch_quantity_changes_count =  len(mismatch[(mismatch['mismatch_type'] == 'UPDATE')]) - mismatch_out_of_stock_count
                        total_mismatch_count = mismatch_quantity_changes_count + mismatch_new_additions_count + mismatch_out_of_stock_count
                    
                    else:
                        mismatch_new_additions_count = 0
                        mismatch_out_of_stock_count =  0
                        mismatch_quantity_changes_count = 0
                        total_mismatch_count = 0
                

                    if len(count)>0:
                        percentage = format (((len(count)*1.0 - total_mismatch_count)/len(count))*100,".2f")
                    else:
                        percentage= 0

                    percent, total, mismatches_new_additions,mismatches_quantity_changes,mismatch_out_of_stock,mismatches_total = st.columns(6)
                    with percent:
                        st.metric(label = "Integrity", value = percentage)
                    with total:
                        st.metric(label = "Total Items", value = len(count))
                    with mismatches_new_additions:
                        st.metric(label="New Additions",value = mismatch_new_additions_count)
                    with mismatches_quantity_changes:
                        st.metric(label="Quantity Changes",value = mismatch_quantity_changes_count)
                    with mismatch_out_of_stock:
                        st.metric(label="Out of Stock",value = mismatch_out_of_stock_count)
                    with mismatches_total:
                        st.metric(label="Total Mismatches",value = total_mismatch_count)
                    # st.write(len(count))
                    
                    st.dataframe(job_activity_details)
        else:
            st.write('There are no syncs in this category')
                
    # Display metrics
    col1, col2, col3 = st.columns(3)

    business_summary_syncs = get_business_summary_syncs(selected_date, include_all_statuses, status)

    def get_particular_business_summary_syncs(business):
        if business_summary_syncs.empty:
            return []
        return business_summary_syncs[business_summary_syncs['node_type'] == business]

    oneP_business_summary_syncs = get_particular_business_summary_syncs('SELLER')
    threeP_business_summary_syncs = get_particular_business_summary_syncs('_3PL')

    if col1.button(f"1P: {len(oneP_business_summary_syncs)}", key='1P'):
        st.session_state.display_summary = '1P'
        st.session_state.oneP_sync_summary = oneP_business_summary_syncs

    if col2.button(f"3P: {len(threeP_business_summary_syncs)}", key='3P'):
        st.session_state.display_summary = '3P'
        st.session_state.threeP_sync_summary = threeP_business_summary_syncs
    
    if col3.button(f"Total: {len(business_summary_syncs)}", key='1P_3P'):
        st.session_state.display_summary = 'total'
        st.session_state.total_sync_summary = business_summary_syncs
    

    # Check session state to display the appropriate summary and select box
    if st.session_state.display_summary == '1P' and 'oneP_sync_summary' in st.session_state:
        st.header("1P Syncs")
        display_sync_summary(st.session_state.oneP_sync_summary, key_prefix='oneP')

    elif st.session_state.display_summary == '3P' and 'threeP_sync_summary' in st.session_state:
        st.header("3P Syncs")
        display_sync_summary(st.session_state.threeP_sync_summary, key_prefix='threeP')

    elif st.session_state.display_summary == 'total' and 'total_sync_summary' in st.session_state:
        st.header("Total")
        display_sync_summary(st.session_state.total_sync_summary, key_prefix='1P_3P')

    # # st.dataframe(sync_summary)
    
    if st.button('Go Back'):
        st.session_state['page'] = 'main'
        st.rerun()