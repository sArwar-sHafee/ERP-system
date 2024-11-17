from langchain_core.tools import tool

@tool
def register_purchase_request(user_info: str):
    """Register a purchase request."""
    return {
        "dialog_state": ["Financial_Management"],
        "messages": [
            {
                "type": "text",
                "content": "Registering a purchase request"
            }
        ]
    }  
@tool
def view_expense_report(user_info: str):
    """View an expense report."""
    return {
        "dialog_state": ["Financial_Management"],
        "messages": [
            {
                "type": "text",
                "content": "Viewing an expense report"
            }
        ]
    }