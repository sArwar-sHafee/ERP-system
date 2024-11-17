from typing import Literal

from erp_core.state_definer import State
from langchain_core.messages import ToolMessage
from erp_core._event import create_tool_node_with_fallback
from erp_core.assistant_class import Assistant, CompleteOrEscalate
from erp_core.entry_node import create_entry_node
from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.graph import END, StateGraph, START

from erp_core.runnable.fm_prompt import financial_management_runnable, financial_management_tools

builder = StateGraph(State)

builder.add_node("enter_financial_management", create_entry_node("Financial Management Assistant", "financial_management"))
builder.add_node("financial_management", Assistant(financial_management_runnable))
builder.add_edge("enter_financial_management", "financial_management")
builder.add_node("financial_management_tools", create_tool_node_with_fallback(financial_management_tools))

def route_financial_management(
    state: State,
) -> Literal[
    "financial_management_tools",
    "leave_skill",
    "__end__",
]:
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "leave_skill"
    safe_toolnames = [t.name for t in financial_management_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "financial_management_tools"
    return "financial_management_tools"

builder.add_edge("financial_management_tools", "financial_management")
builder.add_conditional_edges("financial_management", route_financial_management)