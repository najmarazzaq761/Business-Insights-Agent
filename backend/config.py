import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

USER_DATA_DB_PATH = os.path.join(BASE_DIR, "user_data.db")
CHAT_HISTORY_DB_PATH = os.path.join(BASE_DIR, "chat_history.db")
