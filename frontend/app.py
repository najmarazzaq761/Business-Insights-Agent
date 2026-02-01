import streamlit as st
import sys
import os

# Add the parent directory to sys.path to resolve 'backend' imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.agents import get_chat_agent
from backend.data_processing import save_to_sql, data_reading, data_preprocessing
from backend.chat_storage import create_session, list_sessions, get_message_history, update_session_title, delete_session
from backend.config import USER_DATA_DB_PATH



st.set_page_config(page_title="Insight Pilot", layout="wide")
st.title("Business Insights Pilot")

#  Dictionary of Chats 
with st.sidebar:
    st.header("Your chats")
    if st.button("+ New Chat", type="primary", use_container_width=True):
        new_id = create_session()
        st.session_state.current_session_id = new_id
        st.rerun()

    st.write("---")
    
    # List existing sessions
    sessions = list_sessions()
    for s in sessions:
        title = s['title']
        if len(title) > 20:
            title = title[:17] + "..."
            
        col1, col2 = st.columns([0.8, 0.2])
        
        with col1:
             
            if "current_session_id" in st.session_state and st.session_state.current_session_id == s['id']:
                 if st.button(f"👉 {title}", key=f"sel_{s['id']}", use_container_width=True):
                     pass 
            else:
                 if st.button(title, key=f"sel_{s['id']}", use_container_width=True):
                     st.session_state.current_session_id = s['id']
                     st.rerun()
        
        with col2:
            if st.button("🗑️", key=f"del_{s['id']}", help="Delete Chat"):
                delete_session(s['id'])
                if "current_session_id" in st.session_state and st.session_state.current_session_id == s['id']:
                    del st.session_state.current_session_id
                st.rerun()


if "current_session_id" not in st.session_state:
    if sessions:
        st.session_state.current_session_id = sessions[0]['id']
    else:
        st.session_state.current_session_id = create_session()
        st.rerun()

current_session_id = st.session_state.current_session_id
chat_history = get_message_history(current_session_id)


uploaded_data = st.file_uploader("Upload a file", type=["csv", "xlsx"])

if uploaded_data is not None:
    # Read the data
    df, error = data_reading(uploaded_data)
    
    if error:
        st.error(f"Error reading file: {error}")
    else:
        # Preprocess the data
        df = data_preprocessing(df)
        with st.expander("Preview Data"):
            st.dataframe(df.head())
            st.write(df.shape)
        
        # Save to SQL
        table_name = uploaded_data.name.split('.')[0]
        try:
             save_to_sql(df, table_name, USER_DATA_DB_PATH)
             st.success(f"Data ready for analysis (Table: {table_name})")
             
             st.session_state.agent = get_chat_agent()
             
        except Exception as e:
             st.error(f"Error saving to database: {e}")



# Display chat messages from history
for message in chat_history.messages:
    role = "user" if message.type == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(message.content)


if prompt := st.chat_input("Ask a question about your data"):
   
    st.chat_message("user").markdown(prompt)
    chat_history.add_user_message(prompt)
    
 
    current_title = "New Chat" 
    for s in sessions:
        if s['id'] == current_session_id:
            current_title = s['title']
            break
            
    if current_title == "New Chat":
        new_title = prompt[:30] + "..." if len(prompt) > 30 else prompt
        update_session_title(current_session_id, new_title)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                messages_for_agent = chat_history.messages 

                if "agent" not in st.session_state:
                     st.session_state.agent = get_chat_agent()
                
                response = st.session_state.agent.invoke({"messages": messages_for_agent})
                
                response_content = ""
                if isinstance(response, dict) and "messages" in response:
                     response_content = response["messages"][-1].content
                else:
                     # Fallback
                     response_content = str(response.get("output", response))
                
                st.markdown(response_content)
                chat_history.add_ai_message(response_content)
            except Exception as e:
                st.error(f"An error occurred: {e}")

