insert_queries = {
    'supply_activity_log': """INSERT INTO supply_activity_log (
                                    job_id, event_type, system, event_generated_at, created_at, created_by,business_unit,country_code)
                                  VALUES (
                                    '{job_id}', '{event_type}', '{system}', 
                                    '{event_generated_at}', 
                                    '{created_at}', '{created_by}','{business_unit}','{country_code}');""",
                                    
    'supply_summary': """INSERT INTO supply_summary (
                                id, node_id, item_id, "condition", supply_type, quantity, quantity_unit_of_measure, last_source_update_event, 
                                last_source_updated_at, "version", created_at, created_by, last_updated_at, last_updated_by)
                              VALUES (
                                '{id}', '{node_id}', '{item_id}', '{condition}', '{supply_type}', 
                                '{quantity}', '{quantity_unit_of_measure}', '{last_source_update_event}', 
                                '{last_source_updated_at}', 
                                '{version}', 
                                '{created_at}', '{created_by}', 
                                '{last_updated_at}', '{last_updated_by}');""",
                                
    'demand_order_summary': """INSERT INTO demand_order_summary (
                                        id, channel, order_type, order_id, line_id, item_id, node_id, reference_id, condition, 
                                        quantity, quantity_unit_of_measure, status, version, expires_at, scheduler_id, created_by, 
                                        created_at, last_updated_by, last_updated_at)
                                      VALUES (
                                        '{id}', '{channel}', '{order_type}', '{order_id}', '{line_id}', '{item_id}', 
                                        '{node_id}', '{reference_id}', '{condition}', 
                                        '{quantity}', '{quantity_unit_of_measure}', '{status}', 
                                        '{version}', 
                                        '{expires_at}', '{scheduler_id}', '{created_by}', 
                                        '{created_at}', '{last_updated_by}', 
                                        '{last_updated_at}');""",
                                         
    'inventory_summary': """INSERT INTO inventory_summary (
                                    id, item_id, node_id, condition, supply_type, quantity_in_supply, 
                                    quantity_in_demand, quantity_ats, quantity_unit_of_measure, stock_level, version, created_by, 
                                    created_at, last_updated_by, last_updated_at)
                                  VALUES (
                                    '{id}', '{item_id}', '{node_id}', '{condition}', '{supply_type}', 
                                    '{quantity_in_supply}', 
                                    '{quantity_in_demand}', 
                                    '{quantity_ats}', 
                                    '{quantity_unit_of_measure}', '{stock_level}', 
                                    '{version}', 
                                    '{created_by}', 
                                    '{created_at}', '{last_updated_by}', 
                                    '{last_updated_at}');""",                              
                                    
    'supply_activity_item_log': """INSERT INTO supply_activity_item_log (
                                            id, node_id, item_id, "condition", supply_type, source_update_type, quantity, quantity_unit_of_measure, 
                                            source_system, source_updated_at, created_at, created_by,supply_activity_log_job_id,supply_activity_log_created_at)
                                          VALUES (
                                            '{id}', '{node_id}', '{item_id}', '{condition}', '{supply_type}', '{source_update_type}', 
                                            '{quantity}', '{quantity_unit_of_measure}', '{source_system}', 
                                            '{source_updated_at}', 
                                            '{created_at}', '{created_by}','{supply_activity_log_job_id}','{supply_activity_log_created_at}');""",
    
    'supply_activity_item_error_log': """INSERT INTO supply_activity_item_error_log (
                                                id, supply_summary_id, supply_activity_item_log_id, 
                                                supply_activity_item_log_created_at, error_message, created_at, created_by)
                                              VALUES (
                                                '{id}', '{supply_summary_id}', '{supply_activity_item_log_id}', 
                                                '{supply_activity_item_log_created_at}', 
                                                '{error_message}', 
                                                '{created_at}', '{created_by}');""",
                                                
    'supply_activity_item_ignored_log': """INSERT INTO supply_activity_item_ignored_log (
                                                    id, supply_summary_id, supply_activity_item_log_id, supply_activity_item_log_created_at, 
                                                    ignored_reason, created_at, created_by)
                                                  VALUES (
                                                    '{id}', '{supply_summary_id}', '{supply_activity_item_log_id}', 
                                                    '{supply_activity_item_log_created_at}', 
                                                    '{ignored_reason}', 
                                                    '{created_at}', '{created_by}');""",
                                                    
    'supply_node_full_sync_summary': """INSERT INTO supply_node_full_sync_summary (
                                                id, supply_activity_log_job_id, supply_activity_log_created_at, node_code, status, started_at, 
                                                completed_at, metadata, created_at, created_by, last_updated_at, last_updated_by, file_name, reason)
                                              VALUES (
                                                '{id}', '{supply_activity_log_job_id}', 
                                                '{supply_activity_log_created_at}', '{node_code}', '{status}', 
                                                '{started_at}', 
                                                '{completed_at}', '{metadata}', 
                                                '{created_at}', '{created_by}', 
                                                '{last_updated_at}', '{last_updated_by}','{file_name}','{reason}');""",                                               
                                
    'supply_node_full_sync_mismatch_log': """INSERT INTO supply_node_full_sync_mismatch_log (
                                                    id, mismatch_type, previous_quantity, updated_quantity, 
                                                    supply_activity_item_log_id, supply_activity_item_log_created_at, 
                                                    supply_summary_id, created_at, created_by,previous_quantity_unit_of_measure,updated_quantity_unit_of_measure)
                                                  VALUES (
                                                    '{id}', '{mismatch_type}', 
                                                    '{previous_quantity}', 
                                                    '{updated_quantity}', 
                                                    '{supply_activity_item_log_id}', 
                                                    '{supply_activity_item_log_created_at}', 
                                                    '{supply_summary_id}', 
                                                    '{created_at}', '{created_by}','{previous_quantity_unit_of_measure}','{updated_quantity_unit_of_measure}');""",
                                                    
    'node_lookup':"""INSERT INTO node_lookup (node_id, business_unit, country_code, node_code, node_type, node_name, created_at, last_updated_at)
                 VALUES (
                   '{node_id}','{business_unit}',
                   '{country_code}','{node_code}',
                   '{node_type}','{node_name}',
                   '{created_at}','{last_updated_at}'
                 );"""
    
}