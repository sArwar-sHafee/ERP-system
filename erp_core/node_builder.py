from typing import Literal

from erp_core.state_definer import State
from langchain_core.messages import ToolMessage
from erp_core._event import create_tool_node_with_fallback
from erp_core.assistant_class import Assistant, CompleteOrEscalate
from erp_core.entry_node import create_entry_node
from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.graph import END, StateGraph, START
from operator import __and__
from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.sqlite import SqliteSaver

from erp_core.runnable.fm_prompt import financial_management_runnable, financial_management_tools
from erp_core.runnable.scm_prompt import supply_chain_management_runnable, supply_chain_management_tools
from erp_core.runnable.hr_prompt import human_resource_runnable, human_resource_tools
from erp_core.runnable.pm_prompt import project_management_runnable, project_management_tools
from erp_core.runnable.crm_prompt import customer_relationship_management_runnable, customer_relationship_management_tools
from erp_core.runnable.primary_assistant_prompt import assistant_runnable, primary_assistant_tools

from erp_core.tool_binder.tool_binder import ToHumanResourceDepartment, ToFinancialManagementDepartment, ToSupplyChainManagementDepartment, ToProjectManagementDepartment, ToCustomerRelationshipManagementDepartment
builder = StateGraph(State)


# fetch user info
# ........................................................................
def user_info(state: State):
    return {"user_info": ""}

builder.add_node("fetch_user_info", user_info)
builder.add_edge(START, "fetch_user_info")


# financial management assistant
# ........................................................................

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

# supply chain management assistant
# ........................................................................

builder.add_node("enter_supply_chain_management", create_entry_node("Supply Chain Management Assistant", "supply_chain_management"))
builder.add_node("supply_chain_management", Assistant(supply_chain_management_runnable))
builder.add_edge("enter_supply_chain_management", "supply_chain_management")
builder.add_node("supply_chain_management_tools", create_tool_node_with_fallback(supply_chain_management_tools))

def route_supply_chain_management(
    state: State,
) -> Literal[
    "supply_chain_management_tools",
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
    safe_toolnames = [t.name for t in supply_chain_management_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "supply_chain_management_tools"
    return "supply_chain_management_tools"

builder.add_edge("supply_chain_management_tools", "supply_chain_management")
builder.add_conditional_edges("supply_chain_management", route_supply_chain_management)



# human resource assistant
# ........................................................................

builder.add_node("enter_human_resource", create_entry_node("Human Resource Assistant", "human_resource"))
builder.add_node("human_resource", Assistant(human_resource_runnable))
builder.add_edge("enter_human_resource", "human_resource")
builder.add_node("human_resource_tools", create_tool_node_with_fallback(human_resource_tools))

def route_human_resource(
    state: State,
) -> Literal[
    "human_resource_tools",
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
        return "human_resource_tools"
    return "human_resource_tools"

builder.add_edge("human_resource_tools", "human_resource")
builder.add_conditional_edges("human_resource", route_human_resource)


# Project management assistant
# ........................................................................

builder.add_node("enter_project_management", create_entry_node("Project Management Assistant", "project_management"))
builder.add_node("project_management", Assistant(project_management_runnable))
builder.add_edge("enter_project_management", "project_management")
builder.add_node("project_management_tools", create_tool_node_with_fallback(project_management_tools))

def route_project_management(
    state: State,
) -> Literal[
    "project_management_tools",
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
    safe_toolnames = [t.name for t in project_management_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "project_management_tools"
    return "project_management_tools"

builder.add_edge("project_management_tools", "project_management")
builder.add_conditional_edges("project_management", route_project_management)


# customer relationship management assistant    
# ........................................................................
builder.add_node("enter_customer_relationship_management", create_entry_node("Customer Relationship Management Assistant", "customer_relationship_management"))
builder.add_node("customer_relationship_management", Assistant(customer_relationship_management_runnable))
builder.add_edge("enter_customer_relationship_management", "customer_relationship_management")
builder.add_node("customer_relationship_management_tools", create_tool_node_with_fallback(customer_relationship_management_tools))  

def route_customer_relationship_management(
    state: State,
) -> Literal[
    "customer_relationship_management_tools",
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
    safe_toolnames = [t.name for t in customer_relationship_management_tools]
    if all(tc["name"] in safe_toolnames for tc in tool_calls):
        return "customer_relationship_management_tools"
    return "customer_relationship_management_tools"

builder.add_edge("customer_relationship_management_tools", "customer_relationship_management")
builder.add_conditional_edges("customer_relationship_management", route_customer_relationship_management)   


# leave skill
# ........................................................................

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


# primary assistant
# ........................................................................

builder.add_node("primary_assistant", Assistant(assistant_runnable))
builder.add_node("primary_assistant_tools", create_tool_node_with_fallback(primary_assistant_tools))

def route_primary_assistant(
    state: State,
) -> Literal[
    "primary_assistant_tools",
    "enter_human_resource",
    "enter_financial_management",
    "enter_supply_chain_management",
    "enter_project_management",
    "enter_customer_relationship_management",
    "__and__",
]:
    route = tools_condition(state)
    if route == END:
        return END
    tool_calls = state["messages"][-1].tool_calls
    if tool_calls:
        if tool_calls[0]["name"] == ToHumanResourceDepartment.__name__:
            return "enter_human_resource"
        elif tool_calls[0]["name"] == ToFinancialManagementDepartment.__name__:
            return "enter_financial_management"
        elif tool_calls[0]["name"] == ToSupplyChainManagementDepartment.__name__:
            return "enter_supply_chain_management"
        elif tool_calls[0]["name"] == ToProjectManagementDepartment.__name__:
            return "enter_project_management"
        elif tool_calls[0]["name"] == ToCustomerRelationshipManagementDepartment.__name__:
            return "enter_customer_relationship_management"
        return "primary_assistant_tools"
    raise ValueError("Invalid route")


# The assistant can route to one of the delegated assistants,
# directly use a tool, or directly respond to the user
builder.add_conditional_edges(
    "primary_assistant",
    route_primary_assistant,
    {
        "enter_human_resource": "enter_human_resource",
        "enter_financial_management": "enter_financial_management",
        "enter_supply_chain_management": "enter_supply_chain_management",
        "enter_project_management": "enter_project_management",
        "enter_customer_relationship_management": "enter_customer_relationship_management",
        "primary_assistant_tools": "primary_assistant_tools",
        END: END,
    },
)
builder.add_edge("primary_assistant_tools", "primary_assistant")


# Each delegated workflow can directly respond to the user
# When the user responds, we want to return to the currently active workflow
def route_to_workflow(
    state: State,
) -> Literal[
    "primary_assistant",
    "human_resource",
    "financial_management",
    "supply_chain_management",
    "project_management",
    "customer_relationship_management",
]:
    """If we are in a delegated state, route directly to the appropriate assistant."""
    dialog_state = state.get("dialog_state")
    if not dialog_state:
        return "primary_assistant"
    return dialog_state[-1]


builder.add_conditional_edges("fetch_user_info", route_to_workflow)


# Compile graph
def compile_graph():
    memory = MemorySaver()
    graph = builder.compile(checkpointer=memory)
    return graph
