

from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import pandas as pd
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
import logging
import os





def drop_staging_tables():
    redshift_hook = PostgresHook(postgres_conn_id='redshift_conn')
    redshift_conn = redshift_hook.get_conn()
    redshift_cursor = redshift_conn.cursor()
    
    try:
        redshift_cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'staging'")
        tables = redshift_cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            redshift_cursor.execute(f"DROP TABLE IF EXISTS staging.{table_name} CASCADE")
            logging.info(f"Dropped table staging.{table_name}")
        
        redshift_conn.commit()
    except Exception as e:
        logging.error(f"Error dropping tables in staging schema: {e}")
    finally:
        redshift_cursor.close()
        redshift_conn.close()


def generate_ddl():
    sql_hook = MsSqlHook(mssql_conn_id='sql_conn')
    redshift_hook = PostgresHook(postgres_conn_id='redshift_conn')
    
    sql_conn = sql_hook.get_conn()
    sql_cursor = sql_conn.cursor()

    sql_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_SCHEMA='dbo'")
    tables = sql_cursor.fetchall()

    for table in tables:
        table_name = table[0]
        sql_cursor.execute(f"""
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME='{table_name}' AND TABLE_SCHEMA='dbo'
        """)
        columns = sql_cursor.fetchall()

        ddl = f"CREATE TABLE staging.{table_name} ("
        for column in columns:
            col_name, data_type, char_len = column
            if data_type in ['varchar', 'char', 'nvarchar', 'nchar'] and char_len is not None:
                ddl += f"{col_name} {data_type}({char_len}), "
            else:
                ddl += f"{col_name} {data_type}, "
        ddl = ddl.rstrip(', ') + ');'

        logging.info(f"Executing DDL for table: {table_name}")
        redshift_hook.run(ddl)

    sql_cursor.close()
    sql_conn.close()


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 26),
    'retries': 1,
}

with DAG('Raw_zone_DDL_Creation_on_redshfit', default_args=default_args, schedule_interval=None) as dag:
    drop_staging_tables_task = PythonOperator(
        task_id='drop_staging_tables',
        python_callable=drop_staging_tables,
    )
    
    generate_ddl_task = PythonOperator(
        task_id='generate_ddl',
        python_callable=generate_ddl,
    )



    drop_staging_tables_task >> generate_ddl_task 