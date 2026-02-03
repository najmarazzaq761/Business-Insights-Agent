
# Business Insights Agent

Business Insights Agent is an AI-powered application designed to analyze business data and generate meaningful insights through natural language interaction. It allows users to query data, perform analysis, and visualize results using intelligent agents and tools.

---

## 🚀 Key Features

*  AI-driven agents for business analysis
*  Natural language querying over structured data
*  Automated charts and insights generation
*  SQL-based data handling
*  Persistent chat history storage
*  Interactive frontend built with Streamlit

---

## Project Structure

```
Business-Insights-Agent/
│
├── backend/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── agents.py          # Core AI agents logic
│   ├── tools.py           # Tools for DB queries & visualizations
│   ├── prompt.py          # System and task prompts
│   ├── chat_storage.py    # Chat history management
│   ├── config.py          # Configuration settings
│   └── data_processing.py # Data cleaning & processing
│
├── frontend/
│   └── app.py             # Streamlit frontend
│
├── user_data.db           # SQLite database
├── chat_history.json      # Stored conversation history
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
├── LICENSE
└── .gitignore
```

---

##  Tech Stack

* **Python** 
* **Streamlit** 
* **SQLite** 
* **LLMs / Agents Framework** 
* **Data Visualization Libraries** 

---

## ⚙️ Installation & Setup

1. Clone the repository

   ```bash
   git clone https://github.com/your-username/business-insights-agent.git
   cd business-insights-agent
   ```

2. Create and activate virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application

   ```bash
   streamlit run frontend/app.py
   ```

---

##  How It Works

* The user interacts with the Streamlit UI.
* Queries are processed by AI agents in the backend.
* Tools handle database queries and chart rendering.
* Results and insights are displayed visually and textually.

---

##  Use Cases

* Sales performance analysis
* Product trend insights
* Business decision support
* Automated reporting

---

##  License

This project is licensed under the MIT License.

---

## Author

Developed by **Najma Razzaq**
* Data Science & AI Enthusiast



