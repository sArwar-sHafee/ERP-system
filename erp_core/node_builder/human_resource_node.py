from typing import Literal

from erp_core.state_definer import State
from langchain_core.messages import ToolMessage
from erp_core._event import create_tool_node_with_fallback
from erp_core.assistant_class import Assistant, CompleteOrEscalate
from erp_core.entry_node import create_entry_node
from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.graph import END, StateGraph, START

from erp_core.runnable.hr_prompt import human_resource_runnable, human_resource_tools

builder = StateGraph(State)

builder.add_node("enter_human_resource_management", create_entry_node("Human Resource Management Assistant", "human_resource_management"))
builder.add_node("human_resource_management", Assistant(human_resource_runnable))
builder.add_edge("enter_human_resource_management", "human_resource_management")
builder.add_node("human_resource_management_tools", create_tool_node_with_fallback(human_resource_tools))

def route_human_resource_management(
    state: State,
) -> Literal[
    "human_resource_management_tools",
    "leave_skill",
    "__end__",
]:
    route = tools_condition(state)
    if route == END:
        return END # end the graph
    tool_calls = state["messages"][-1].tool_calls
    did_cancel = any(tc["name"] == CompleteOrEscalate.__name__ for tc in tool_calls)
    if did_cancel:
        return "leave_skill"

    safe_toolnames = [t.name for t in human_resource_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "human_resource_management_tools"
    return "human_resource_management_tools"

builder.add_edge("human_resource_management_tools", "human_resource_management")
builder.add_conditional_edges("human_resource_management", route_human_resource_management)
