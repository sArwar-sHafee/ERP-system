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
from erp_core.runnable.scm_prompt import supply_chain_management_runnable, supply_chain_management_tools
from erp_core.runnable.hr_prompt import human_resource_runnable, human_resource_tools
from erp_core.runnable.pm_prompt import project_management_runnable, project_management_tools
from erp_core.runnable.crm_prompt import customer_relationship_management_runnable, customer_relationship_management_tools


builder = StateGraph(State)


def user_info(state: State):
    return {"user_info": "Kamal Ahmed, mobile number: 1234567890"}


builder.add_node("fetch_user_info", user_info)
builder.add_edge(START, "fetch_user_info")

def pop_dialog_state(state: State) -> dict:
    """Pop the dialog stack and return to the main assistant.

    This lets the full graph explicitly track the dialog flow and delegate control
    to specific sub-graphs.
    """
    messages = []
    if state["messages"][-1].tool_calls:
        # Note: Doesn't currently handle the edge case where the llm performs parallel tool calls
        messages.append(
            ToolMessage(
                content="Resuming dialog with the host assistant. Please reflect on the past conversation and assist the user as needed.",
                tool_call_id=state["messages"][-1].tool_calls[0]["id"],
            )
        )
    return {
        "dialog_state": "pop",
        "messages": messages,
    }

builder.add_node("leave_skill", pop_dialog_state)
builder.add_edge("leave_skill", "primary_assistant")