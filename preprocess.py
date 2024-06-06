import os
import pandas as pd
from datetime import datetime, timezone
import uuid

def preprocess_timestamp():
    
    def format_current_time():
        current_time = datetime.now(timezone.utc)  # Get current time in UTC
        formatted_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + '+0530'  # Format to desired milliseconds and timezone
        return formatted_time

    def modify_datetime(value, col_name):
        try:
            if pd.isna(value) or value.strip() in ['nan', '']:
                probable_null_columns = ['last_updated_at','completed_at']
                if col_name in probable_null_columns:
                    return format_current_time()
                else:
                    return ""  # Return empty string for other columns if the value is empty
            else:
                parts = value.split()
                if len(parts) == 3:  # Check if the date-time string has timezone information
                    datetime_str = f"{parts[0]}T{parts[1]}"
                    return datetime_str + parts[2]
                else:  # If timezone information is missing, assume it's +0530
                    return value + '+0530'
        except:
            return ""  # Return empty string if any error occurs

    def help(file_path, list_of_probable_columns, store_path):
        df = pd.read_csv(file_path)
        for col in list_of_probable_columns:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: modify_datetime(x, col))
        df.to_csv(store_path, index=False)  # Do not specify na_rep, this will not print "NULL" values

    list_of_probable_columns = [
        'source_updated_at', 'created_at', 'last_updated_at', 
        'last_source_updated_at', 'supply_activity_item_log_created_at', 
        'event_generated_at', 'completed_at', 'started_at','supply_activity_log_created_at'
    ]
    
    folder_path = 'db'
    for root, directories, files in os.walk(folder_path):
        for filename in files:
            # Construct the full file path
            file_path = os.path.join(root, filename)
            os.makedirs('processed_db', exist_ok=True)
            store_path = os.path.join('processed_db', filename)
            help(file_path, list_of_probable_columns, store_path)

def process_null_values():
    def generate_uuid(value):
        return uuid.uuid1()
    supply_activity_item_error_log_file_path = 'processed_db/supply_activity_item_error_log.csv'
    item_error_log_df = pd.read_csv(supply_activity_item_error_log_file_path)
    item_error_log_df['supply_summary_id'] = item_error_log_df['supply_summary_id'].apply(generate_uuid) 
    item_error_log_df.to_csv(supply_activity_item_error_log_file_path, index=False)

def delete_old_files():
    folder_path = 'processed_db'
    for root, directories, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            os.remove(file_path)

# Delete old processed files
delete_old_files()

# Preprocess Data in CSV files
preprocess_timestamp()

# Process Null Values in CSV files
process_null_values()
