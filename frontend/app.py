import sys
import os

# Add project root to path
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
import plotly.express as px
from agents.graph import build_graph


# ---------------- PAGE ----------------
st.set_page_config(
    page_title="NeonSQL Agent",
    layout="wide"
)


# ---------------- CSS ----------------
st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #050816;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #0d1117;
}

h1, h2, h3 {
    color: #00F5FF;
}

.stButton > button {
    background: linear-gradient(90deg,#00F5FF,#00C3FF);
    color: black;
    font-weight: bold;
    border-radius: 10px;
    border: none;
}

textarea {
    background-color: #111827 !important;
    color: white !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #00F5FF;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚡ NeonSQL Agent")

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="Enter Claude API Key"
    )

    st.markdown("---")
    st.caption("Claude + LangGraph + MySQL")
    st.caption("😊 Made by Srikonda Karthik")


# ---------------- MAIN ----------------
st.title("⚡ NeonSQL Agent")
st.caption("Ask questions to your SQLite database in natural language.")

question = st.text_area(
    "Ask your question",
    placeholder="Show all students"
)


# ---------------- BUTTON ----------------
if st.button("Run Query"):

    if not api_key:
        st.warning("Please enter Anthropic API key.")
        st.stop()

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    graph = build_graph()

    state = {
        "question": question,
        "api_key": api_key
    }

    with st.spinner("Thinking like an analyst..."):
        result = graph.invoke(state)

    # ---------- ERROR ----------
    if result.get("error"):
        st.error(result["error"])

    else:
        # ---------- SQL ----------
        st.subheader("Generated SQL")
        st.code(result["sql"], language="sql")

        # ---------- TABLE ----------
        df = result["result"]

        st.subheader("Results")
        st.dataframe(df, use_container_width=True)

        # ---------- CHART ----------
        if result.get("chart_ready"):

            chart = result["chart"]

            st.subheader("Visualization")

            if chart["type"] == "bar":

                fig = px.bar(
                    df,
                    x=chart["x"],
                    y=chart["y"],
                    color=chart["x"],
                    title=chart["title"],
                    template="plotly_dark"
                )

            elif chart["type"] == "count":

                temp = df[chart["x"]].value_counts().reset_index()
                temp.columns = [chart["x"], "count"]

                fig = px.bar(
                    temp,
                    x=chart["x"],
                    y="count",
                    color=chart["x"],
                    title=chart["title"],
                    template="plotly_dark"
                )

            elif chart["type"] == "histogram":

                fig = px.histogram(
                    df,
                    x=chart["x"],
                    title=chart["title"],
                    template="plotly_dark"
                )

            st.plotly_chart(fig, use_container_width=True)