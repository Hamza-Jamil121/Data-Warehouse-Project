
from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import logging
import os, time, pendulum
from datetime import datetime
import os
from SQL_QUERY.incremental_raw_query import *
from SQL_QUERY.dimension_fact import *

def export_sql_to_s3():
    sql_hook = MsSqlHook(mssql_conn_id='sql_conn')
    s3_hook = S3Hook(aws_conn_id='sql_server_s3_conn')
    bucket_name = 'sql-server-data'
    sql_conn = sql_hook.get_conn()
    sql_cursor = sql_conn.cursor()

    sql_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='dbo'")
    tables = sql_cursor.fetchall()

    for table in tables:
        table_name = table[0]
        logging.info(f"Processing table: {table_name}")
        sql_cursor.execute(f"SELECT * FROM [inventory_management].dbo.{table_name}")
        df = pd.DataFrame(sql_cursor.fetchall(), columns=[col[0] for col in sql_cursor.description])
        
        file_name = f"{table_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        file_path = f"/tmp/{file_name}"
        df.to_csv(file_path, index=False)

        s3_hook.load_file(filename=file_path, bucket_name=bucket_name, key=f"data/{file_name}", replace=True)
        logging.info(f"Uploaded {file_name} to S3 bucket {bucket_name}")
        os.remove(file_path)

    sql_cursor.close()
    sql_conn.close()


def delete_existing_files():


    s3_hook = S3Hook(aws_conn_id='sql_server_s3_conn')

    keys = s3_hook.list_keys(bucket_name='sql-server-data', prefix='data/')

    if keys:
        s3_hook.delete_objects(bucket='sql-server-data', keys=keys)


def truncate_staging_tables():
    redshift_hook = PostgresHook(postgres_conn_id='redshift_conn')
    redshift_conn = redshift_hook.get_conn()
    redshift_cursor = redshift_conn.cursor()
    
    try:
        redshift_cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'staging'")
        tables = redshift_cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            redshift_cursor.execute(f"TRUNCATE TABLE staging.{table_name}")
            logging.info(f"Truncated table staging.{table_name}")
        
        redshift_conn.commit()
    except Exception as e:
        logging.error(f"Error truncating tables in staging schema: {e}")
    finally:
        redshift_cursor.close()
        redshift_conn.close()


def load_s3_to_redshift():
    s3_hook = S3Hook(aws_conn_id='sql_server_s3_conn')
    redshift_hook = PostgresHook(postgres_conn_id='redshift_conn')
    bucket_name = 'sql-server-data'
    redshift_conn = redshift_hook.get_conn()
    redshift_cursor = redshift_conn.cursor()

    # List all files in the S3 bucket under the 'data/' prefix
    s3_keys = s3_hook.list_keys(bucket_name=bucket_name, prefix='data/')
    csv_files = [key for key in s3_keys if key.endswith('.csv')]

    for csv_file in csv_files:
        # Extract the table name correctly from the filename
        table_name = os.path.basename(csv_file).rsplit('_', 1)[0]
        logging.info(f"Loading data for table: {table_name} from file: {csv_file}")

        s3_path = f"s3://{bucket_name}/{csv_file}"
        copy_query = f"""
        COPY staging.{table_name}
        FROM '{s3_path}'
        IAM_ROLE 'arn:aws:iam::975050201835:role/service-role/AmazonRedshift-CommandsAccessRole-20240528T014607'
        FORMAT AS CSV
        IGNOREHEADER 1;
        """
        try:
            redshift_cursor.execute(copy_query)
            redshift_conn.commit()
            logging.info(f"Data loaded into staging.{table_name} from {s3_path}")
        except Exception as e:
            logging.error(f"Error loading data into staging.{table_name} from {s3_path}: {e}")
            logging.error(f"Query: {copy_query}")
            redshift_conn.rollback()


    redshift_cursor.close()
    redshift_conn.close()


local_tz = pendulum.timezone("Europe/London")
start_date=pendulum.yesterday(tz=local_tz)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

  
with DAG('Datawarehouse_project_elt_pipline', default_args=default_args,start_date= start_date,schedule_interval='13 23 * * *') as dag:
    truncate_staging_tables = PythonOperator(
        task_id='truncate_staging_tables_data',
        python_callable=truncate_staging_tables,
    )


    task_delete_existing_files_from_S3 = PythonOperator(
        task_id="delete_existing_files_from_S3",
        python_callable=delete_existing_files
    )

    export_sql_to_s3_task = PythonOperator(
        task_id='export_sql_to_s3',
        python_callable=export_sql_to_s3,
    )

    load_s3_to_redshift_task = PythonOperator(
        task_id='load_s3_to_redshift',
        python_callable=load_s3_to_redshift,
    )



    staging_raw_zone_task = SQLExecuteQueryOperator(
        task_id='staging_to_raw_zone_task',
        conn_id="redshift_conn",
        autocommit=True,
        sql=[
            truncate_scm_raw_zone_customers,
            insert_scm_raw_zone_customers,
            truncate_scm_raw_zone_employees,
            insert_scm_raw_zone_employees,
            truncate_scm_raw_zone_inventory,
            insert_scm_raw_zone_iventory,
            truncate_scm_raw_zone_inventory_transactions,
            insert_scm_raw_zone_inventory_transactions,
            truncate_scm_raw_zone_order_details,
            insert_scm_raw_zone_order_details,
            truncate_scm_raw_zone_orders,
            insert_scm_raw_zone_orders,
            truncate_scm_raw_zone_payment,
            insert_scm_raw_zone_payment,
            truncate_scm_raw_zone_products,
            insert_scm_raw_zone_products,
            truncate_scm_raw_zone_returns,
            insert_scm_raw_zone_returns,
            truncate_scm_raw_zone_shipment,
            insert_scm_raw_zone_shipments,
            truncate_scm_raw_zone_supplier,
            insert_scm_raw_zone_supplier,
            truncate_scm_raw_zone_supplier_product,
            insert_scm_raw_zone_suppliers_products,
            truncate_scm_raw_zone_warehouse,
            insert_scm_raw_zone_warehouse,
        
        ]
    )


    dimension_fact_data_mov = SQLExecuteQueryOperator(
        task_id='dimension_fact_data',
        conn_id="redshift_conn",
        autocommit=True,
        sql=[
            truncate_processing_zone_DimProducts,
            insert_processing_zone_DimProducts,
            truncate_processing_zone_DimSuppliers,
            insert_DimSuppliers,
            truncate_processing_zone_DimWarehouses,
            insert_DimWarehouses,
            truncate_DimCustomers,
            insert_DimCustomers,
            truncate_DimEmployees,
            insert_DimEmployees,
            truncate_DIM_datetime,
            insert_DIM_datetime,
            truncate_FactOrderDetails,
            insert_FactOrderDetails,
            truncate_FactTransactions,
            insert_FactTransactions
        
        ]
    )



    

truncate_staging_tables  >> task_delete_existing_files_from_S3 >> export_sql_to_s3_task >> load_s3_to_redshift_task >> staging_raw_zone_task >> dimension_fact_data_mov

