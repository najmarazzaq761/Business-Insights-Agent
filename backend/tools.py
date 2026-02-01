from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.tools import tool
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import json
from io import StringIO
from typing import List, Any
from backend.config import USER_DATA_DB_PATH
DB_PATH = USER_DATA_DB_PATH

@tool
def sql_to_graph(sql_result: str, chart_type: str) -> str:
    """
    Converts SQL result data into a graphical representation and displays it in Streamlit.
    
    Args:
        sql_result (str): The result data obtained from an SQL query. 
                          Can be a JSON string, a list of dictionaries, or a string output from the agent.
        chart_type (str): The type of chart to create (e.g., 'bar', 'line', 'pie', 'scatter').

    Returns:
        str: A status message indicating if the graph was displayed or if an error occurred.
    """
    try:
        data = None

        if isinstance(sql_result, str):
            sql_result = sql_result.strip()
            if sql_result.startswith("```json"):
                sql_result = sql_result[7:]
            if sql_result.startswith("```"):
                sql_result = sql_result[3:]
            if sql_result.endswith("```"):
                sql_result = sql_result[:-3]
            sql_result = sql_result.strip()
        if isinstance(sql_result, list):
             data = pd.DataFrame(sql_result)
        elif isinstance(sql_result, str):
            try:
            
                parsed_json = json.loads(sql_result)
                data = pd.DataFrame(parsed_json)
            except json.JSONDecodeError:
              
                try:
                    import ast
                    parsed_list = ast.literal_eval(sql_result)
                    if isinstance(parsed_list, list):
                         data = pd.DataFrame(parsed_list)
                except:
                     pass
        
        if data is None or data.empty:

             try:
                 data = pd.read_csv(StringIO(sql_result), sep="|")

                 data.columns = [c.strip() for c in data.columns] 

                 data = data.dropna(axis=1, how='all').dropna(axis=0, how='all')
             except:
                return "Error: Could not parse SQL result into data for plotting. Please ensure the SQL result is a JSON list of dictionaries or a standard list."

        if data is None or data.empty:
            return "Error: No data available to plot."

        plt.figure(figsize=(10, 6))
        
        if len(data.columns) < 2:
            return "Error: Need at least two columns (Label and Value) to plot."

        x_col = data.columns[0]
        y_cols = data.columns[1:]
        

        for col in y_cols:
            data[col] = pd.to_numeric(data[col], errors='coerce')
        
        # Basic plotting logic
        if chart_type.lower() == 'bar':
             data.plot(x=x_col, kind='bar', ax=plt.gca(), legend=True)
             plt.ylabel("Values")
             plt.xticks(rotation=45, ha='right')
        elif chart_type.lower() == 'line':
             data.plot(x=x_col, kind='line', ax=plt.gca(), marker='o', legend=True)
             plt.ylabel("Values")
             plt.xticks(rotation=45, ha='right')
        elif chart_type.lower() == 'pie':
             if len(y_cols) > 0:
                y_col = y_cols[0]

                pie_data = data.dropna(subset=[y_col])
                plt.pie(pie_data[y_col], labels=pie_data[x_col], autopct='%1.1f%%', startangle=90)
                plt.axis('equal') 
             else:
                return "Error: Pie chart requires at least one numerical column."
        elif chart_type.lower() == 'scatter':
             if len(y_cols) > 0:
                 data.plot.scatter(x=x_col, y=y_cols[0], ax=plt.gca())
        else:
            return f"Error: Unsupported chart type '{chart_type}'. Use bar, line, pie, or scatter."

        plt.title(f"{chart_type.capitalize()} Chart")
        plt.tight_layout()
        st.pyplot(plt)
        
        plt.close()
        
        return "Graph displayed successfully to the user."

    except Exception as e:
        return f"Error plotting graph: {str(e)}"

def get_tools(llm_instance) -> List[Any]:
 
    db = SQLDatabase.from_uri(f"sqlite:///{DB_PATH}")
    
    toolkit = SQLDatabaseToolkit(db=db, llm=llm_instance)
    sql_tools = toolkit.get_tools()
    all_tools = sql_tools + [sql_to_graph]
    
    return all_tools
