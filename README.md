# ⚡ NeonSQL Agent

NeonSQL Agent is an Agentic AI-powered Text-to-SQL analytics platform built using:

- Streamlit
- LangGraph
- Anthropic Claude
- SQLite
- Plotly

Users can ask natural language questions and get:

- SQL query generation
- Query results table
- Interactive charts
- AI-powered database analytics

---

## 🚀 Features

- Natural language to SQL
- Multi-table database querying
- Dynamic schema detection
- Safe SELECT-only SQL validation
- Interactive Plotly visualizations
- Dark neon futuristic UI
- Streamlit Cloud deployable

---

## 📁 Project Structure

agentic-sql-ai/
├── .streamlit/
│   └── secrets.toml
├── frontend/
│   └── app.py
├── agents/
│   ├── graph.py
│   └── nodes.py
├── tools/
│   ├── llm_tool.py
│   └── sqlite_tool.py
├── college.db
├── requirements.txt

---

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run frontend/app.py