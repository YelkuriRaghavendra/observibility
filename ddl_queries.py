#modifications: removed this column in create command of supply activity item log : adjustment_type varchar(25)
ddl_queries = {
      'create_supply_activity_item_log': """CREATE TABLE supply_activity_item_log (
                                      id uuid NOT NULL,
                                      node_id varchar(255) NOT NULL,
                                      item_id varchar(255) NOT NULL,
                                      condition varchar(25) NOT NULL,
                                      supply_type varchar(25) NOT NULL,
                                      source_update_type varchar(25) NOT NULL,
                                      quantity float8 NOT NULL,
                                      quantity_unit_of_measure varchar(25) NOT NULL,
                                      source_system varchar(255) NOT NULL,
                                      source_updated_at timestamptz NOT NULL,
                                      created_at timestamptz NOT NULL,
                                      created_by varchar(255) NOT NULL,
                                      CONSTRAINT supply_activity_item_log_pk_id_created_at PRIMARY KEY (id, created_at)
                                  );""",

      'create_supply_summary': """ CREATE TABLE supply_summary (
                                      id uuid NOT NULL,
                                      node_id varchar(255) NOT NULL,
                                      item_id varchar(255) NOT NULL,
                                      "condition" varchar(25) NOT NULL,
                                      supply_type varchar(25) NOT NULL,
                                      quantity float8 NOT NULL,
                                      quantity_unit_of_measure varchar(25) NOT NULL,
                                      last_source_update_event varchar(25) NOT NULL,
                                      last_source_updated_at timestamptz NOT NULL,
                                      "version" int8 NOT NULL,
                                      created_at timestamptz NOT NULL,
                                      created_by varchar(255) NOT NULL,
                                      last_updated_at timestamptz NULL,
                                      last_updated_by varchar(255) NULL,
                                      CONSTRAINT supply_summary_pk_id PRIMARY KEY (id)
                                  ); """,
    
      'create_supply_activity_item_ignored_log': """ CREATE TABLE supply_activity_item_ignored_log (
                                                      id uuid NOT NULL,
                                                      supply_summary_id uuid NOT NULL,
                                                      supply_activity_item_log_id uuid NOT NULL,
                                                      supply_activity_item_log_created_at timestamptz NOT NULL,
                                                      ignored_reason varchar(255) NOT NULL,
                                                     created_at timestamptz NOT NULL,
                                                      created_by varchar(255) NOT NULL,
                                                      CONSTRAINT supply_activity_item_ignored_log_pk_id_created_at PRIMARY KEY (id, created_at)
                                                  ); """ ,
                                        
      'alter_supply_summary_unique_constraint': """ ALTER TABLE supply_summary
                                                      ADD CONSTRAINT supply_summary_uk UNIQUE (node_id, item_id, "condition", supply_type);""",

      'create_supply_activity_item_error_log' : """ CREATE TABLE supply_activity_item_error_log (
                                                      id uuid NOT NULL,
                                                      supply_summary_id uuid NULL,
                                                      supply_activity_item_log_id uuid NOT NULL,
                                                      supply_activity_item_log_created_at timestamptz NOT NULL,
                                                      error_message varchar(255) NOT NULL,
                                                      created_at timestamptz NOT NULL,
                                                      created_by varchar(255) NOT NULL,
                                                      CONSTRAINT supply_activity_item_error_log_pk_id_created_at PRIMARY KEY (id, created_at)
                                                  );""" ,
    
      'create_supply_activity_log' : """ CREATE TABLE supply_activity_log (
                                          job_id uuid NOT NULL,
                                          event_type varchar(25) NOT NULL,
                                          system varchar(255) NOT NULL,
                                          event_generated_at timestamptz NOT NULL,
                                          created_at timestamptz NOT NULL,
                                          created_by varchar(255) NOT NULL,
                                          business_unit VARCHAR(255) NOT NULL,
                                          country_code VARCHAR(5) NOT NULL,
                                          CONSTRAINT supply_activity_log_pk_job_id_created_at PRIMARY KEY (job_id, created_at)
                                      );""" ,
    
      
    'create_supply_node_full_sync_summary' : """ CREATE TABLE IF NOT EXISTS supply_node_full_sync_summary (
                                                    id uuid NOT NULL,
                                                    supply_activity_log_job_id uuid NOT NULL,
                                                    supply_activity_log_created_at timestamptz NOT NULL,
                                                    node_code varchar(255) NOT NULL,
                                                    status varchar(25) NOT NULL,
                                                    started_at timestamptz NOT NULL,
                                                    completed_at timestamptz,
                                                    metadata jsonb NOT NULL,
                                                    created_at timestamptz NOT NULL,
                                                    created_by varchar(255) NOT NULL,
                                                    last_updated_at timestamptz,
                                                    last_updated_by varchar(255),
                                                    CONSTRAINT supply_node_full_sync_summary_pk_id_created_at PRIMARY KEY (id, created_at),
                                                    CONSTRAINT supply_node_full_sync_summary_fk_supply_activity_log_job_id_created_at FOREIGN KEY (supply_activity_log_job_id, supply_activity_log_created_at) REFERENCES supply_activity_log (job_id, created_at)
                                                );""" ,

    'create_supply_node_full_sync_mismatch_log': """ CREATE TABLE IF NOT EXISTS supply_node_full_sync_mismatch_log (
                                                          id uuid NOT NULL,
                                                          mismatch_type varchar(25) NOT NULL,
                                                          previous_quantity float8 NOT NULL,
                                                          updated_quantity float8 NOT NULL,
                                                          supply_activity_item_log_id uuid NOT NULL,
                                                          supply_activity_item_log_created_at timestamptz NOT NULL,
                                                          supply_summary_id uuid NOT NULL,
                                                          created_at timestamptz NOT NULL,
                                                          created_by varchar(255) NOT NULL,
                                                          CONSTRAINT supply_node_full_sync_mismatch_log_pk_id_created_at PRIMARY KEY (id, created_at),
                                                         CONSTRAINT supply_node_full_sync_mismatch_log_fk_supply_activity_item_log_id_created_at FOREIGN KEY (supply_activity_item_log_id, supply_activity_item_log_created_at) REFERENCES supply_activity_item_log (id, created_at),
                                                         CONSTRAINT supply_node_full_sync_mismatch_log_fk_supply_summary_id FOREIGN KEY (supply_summary_id) REFERENCES supply_summary (id)
                                                        );""",
    
      'alter_add_columns_file_name_and_reson_supply_node_full_sync_summary': """ ALTER table IF EXISTS supply_node_full_sync_summary ADD COLUMN IF NOT EXISTS file_name VARCHAR(255) NOT NULL,
                                                                                  ADD column IF NOT EXISTS reason VARCHAR(255);  """,

      'alter_add_column_previous_quantity_unit_of_measure_and_updated_quantity_unit_of_measure_alter_previous_quantity_supply_node_full_sync_mismatch_log' : """ TRUNCATE TABLE supply_node_full_sync_mismatch_log;

                                                                                                                                                                  ALTER TABLE supply_node_full_sync_mismatch_log
                                                                                                                                                                  ADD COLUMN previous_quantity_unit_of_measure VARCHAR(25),
                                                                                                                                                                  ADD COLUMN updated_quantity_unit_of_measure VARCHAR(25) NOT NULL,
                                                                                                                                                                  ALTER COLUMN previous_quantity DROP NOT NULL;""",

      'create_fk_supply_activity_log_and_item_log': """ ALTER TABLE IF EXISTS supply_activity_item_log
                                                         ADD COLUMN IF NOT EXISTS supply_activity_log_job_id UUID NOT NULL,
                                                         ADD COLUMN IF NOT EXISTS supply_activity_log_created_at TIMESTAMPTZ NOT NULL;

                                                         ALTER TABLE IF EXISTS supply_activity_item_log
                                                          ADD CONSTRAINT supply_activity_item_log_fk_supply_activity_log_job_id_created_at
                                                         FOREIGN KEY (supply_activity_log_job_id, supply_activity_log_created_at)
                                                         REFERENCES supply_activity_log (job_id, created_at);""",
                        
      'create_inventory_summary': """ CREATE TABLE IF NOT EXISTS inventory_summary (
                                         id UUID PRIMARY KEY NOT NULL,
                                          item_id VARCHAR NOT NULL,
                                         node_id VARCHAR NOT NULL,
                                         condition VARCHAR NOT NULL,
                                         supply_type VARCHAR NOT NULL,
                                         quantity_in_supply FLOAT NOT NULL,
                                         quantity_in_demand FLOAT NOT NULL,
                                         quantity_ats FLOAT NOT NULL,
                                         quantity_unit_of_measure VARCHAR NOT NULL,
                                         stock_level VARCHAR NOT NULL,
                                         version BIGINT NOT NULL,
                                         created_by VARCHAR NOT NULL,
                                         created_at TIMESTAMP NOT NULL,
                                         last_updated_by VARCHAR NULL,
                                         last_updated_at TIMESTAMP NULL
                                         );
                                         """,
      'node_lookup':"""CREATE TABLE IF NOT EXISTS node_lookup (
                       node_id UUID PRIMARY KEY,
                       business_unit VARCHAR(255) NOT NULL,
                       country_code VARCHAR(5) NOT NULL,
                       node_code VARCHAR(255) NOT NULL,
                       node_type VARCHAR(50) NOT NULL,
                       node_name VARCHAR(255) NULL,
                       created_at TIMESTAMPTZ NOT NULL,
                       last_updated_at TIMESTAMPTZ NULL,
                       CONSTRAINT business_unit_country_and_node_code_node_lookup_unique UNIQUE (business_unit, country_code, node_code));""",
                       
                  
     'create_demand_order_summary': """ CREATE TABLE IF NOT EXISTS demand_order_summary (
                                         id UUID PRIMARY KEY NOT NULL,
                                         channel VARCHAR NOT NULL,
                                         order_type VARCHAR NOT NULL,
                                         order_id VARCHAR NOT NULL,
                                         line_id VARCHAR NOT NULL,
                                         item_id VARCHAR NOT NULL,
                                         node_id VARCHAR NOT NULL,
                                         reference_id VARCHAR NOT NULL,
                                         condition VARCHAR NOT NULL,
                                         quantity FLOAT NOT NULL,
                                         quantity_unit_of_measure VARCHAR NOT NULL,
                                         status VARCHAR NOT NULL,
                                         version BIGINT NOT NULL,
                                         expires_at TIMESTAMP NOT NULL,
                                         scheduler_id VARCHAR NOT NULL,
                                         created_by VARCHAR NOT NULL,
                                         created_at TIMESTAMP NOT NULL,
                                         last_updated_by VARCHAR  NULL,
                                         last_updated_at TIMESTAMP  NULL
                                     ); """}


