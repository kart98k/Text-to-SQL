from tools.sqlite_tool import get_schema, run_query
from tools.llm_tool import ask_claude


def planner_node(state):
    state["task"] = "Choose relevant tables from schema, generate safe SQL, create chart"
    return state


def schema_node(state):
    state["schema"] = get_schema()
    return state


def sql_node(state):
    prompt = f"""
You are an expert MySQL SQL developer.

Live Database Schema:
{state["schema"]}

Instructions:
- Use the most relevant table(s) based on user question
- If asking about students -> likely use students table
- If asking about salaries/jobs/pay -> likely use ds_salaries table
- If multiple tables needed, use joins only when keys logically exist
- Generate ONLY SELECT queries
- Never generate DELETE, DROP, UPDATE, INSERT, ALTER
- Use valid MySQL syntax
- Return only SQL
- No markdown
- No explanation

Important:
Use salary_in_usd for salary analysis when available.

User Question:
{state["question"]}
"""

    sql = ask_claude(state["api_key"], prompt)
    sql = sql.replace("```sql", "").replace("```", "").strip()

    state["sql"] = sql
    return state


def validator_node(state):
    sql = state["sql"].lower()

    blocked = [
        "delete", "drop", "update",
        "insert", "truncate", "alter"
    ]

    if any(word in sql for word in blocked):
        state["error"] = "Unsafe SQL detected."
        return state

    if not sql.startswith("select"):
        state["error"] = "Only SELECT queries allowed."
        return state

    return state


def execute_node(state):
    try:
        df = run_query(state["sql"])
        state["result"] = df
    except Exception as e:
        state["error"] = str(e)

    return state


def chart_node(state):
    if "result" not in state:
        return state

    df = state["result"]

    if df.empty:
        state["chart_ready"] = False
        return state

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include="object").columns.tolist()

    chart = {
        "type": None,
        "x": None,
        "y": None,
        "title": "Visualization"
    }

    # categorical + numeric
    if categorical_cols and numeric_cols:
        chart["type"] = "bar"
        chart["x"] = categorical_cols[0]
        chart["y"] = numeric_cols[0]
        chart["title"] = f"{chart['y']} by {chart['x']}"

    # only categorical
    elif categorical_cols:
        chart["type"] = "count"
        chart["x"] = categorical_cols[0]
        chart["title"] = f"Count by {chart['x']}"

    # only numeric
    elif numeric_cols:
        chart["type"] = "histogram"
        chart["x"] = numeric_cols[0]
        chart["title"] = f"Distribution of {chart['x']}"

    state["chart"] = chart
    state["chart_ready"] = True

    return state