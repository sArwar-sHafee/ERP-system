from langchain_core.tools import tool

@tool
def customer_support(user_info: str):
    """Provide customer support."""
    return {
        "dialog_state": ["Customer_Relationship_Management"],
        "messages": [
            {
                "type": "text",
                "content": "Providing customer support"
            }
        ]
    }