import sqlite3
import pandas as pd

 # data reading
def data_reading(uploaded_file):
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else: 
            return None, "Unsupported file format, please upload a CSV or Excel file"
        if df.empty:
            return None, "File is empty."
        return df, None
    except Exception as e:
        return None, str(e)

# data preprocessing
def data_preprocessing(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    df = df.dropna()
    return df


from backend.config import USER_DATA_DB_PATH

def save_to_sql(df, table_name, db_path=USER_DATA_DB_PATH):
   
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        print(f"Data saved to {db_path} in table '{table_name}'")
    except Exception as e:
        print(f"Error saving data to SQL: {e}")
        raise
    
    
        