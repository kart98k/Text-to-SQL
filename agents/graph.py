from langgraph.graph import StateGraph, END

from agents.nodes import (
    planner_node,
    schema_node,
    sql_node,
    validator_node,
    execute_node,
    chart_node
)


def build_graph():
    graph = StateGraph(dict)

    graph.add_node("planner", planner_node)
    graph.add_node("schema", schema_node)
    graph.add_node("sql", sql_node)
    graph.add_node("validator", validator_node)
    graph.add_node("execute", execute_node)
    graph.add_node("chart", chart_node)

    graph.set_entry_point("planner")

    graph.add_edge("planner", "schema")
    graph.add_edge("schema", "sql")
    graph.add_edge("sql", "validator")
    graph.add_edge("validator", "execute")
    graph.add_edge("execute", "chart")
    graph.add_edge("chart", END)

    return graph.compile()