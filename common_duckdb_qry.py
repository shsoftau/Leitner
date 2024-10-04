import duckdb
import pandas as pd

from config import *
from datetime import datetime
from datetime import date

##### Table Load
def duckdb_load_table_to_df(db_fpath, table_name): # load a table data to a dataframe
    conn = duckdb.connect(db_fpath)  # Connect to the DuckDB database
    df = conn.execute(f"SELECT * FROM {table_name}").df()  # Load table into a DataFrame
    conn.close()  # Correctly close the connection
    return df

def append_df_to_db(db_path, table_name, dataframe):
    """
    Update a table in a DuckDB file with the data from a Pandas DataFrame.

    Args:
    db_path (str): Path to the DuckDB file.
    table_name (str): Name of the table to update.
    dataframe (pd.DataFrame): DataFrame containing the data to insert into the table.
    """
    try:
        # Connect to the DuckDB file
        conn = duckdb.connect(db_path)

        # Write DataFrame to the DuckDB table
        # If the table exists, this will replace it with the new data.
        dataframe.to_sql(table_name, conn, if_exists='replace', index=False)
        
        print(f"Table '{table_name}' successfully updated in the database '{db_path}'.")
    
    except Exception as e:
        print(f"An error occurred while updating the table '{table_name}': {e}")
    
    finally:
        # Close the connection
        conn.close()






