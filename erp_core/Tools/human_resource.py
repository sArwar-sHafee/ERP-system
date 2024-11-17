from langchain_core.tools import tool

@tool
def employee_database_access(user_info: str):
    """Access the employee database."""
    return {
        "dialog_state": ["Human_Resource"],
        "messages": [
            {
                "type": "text",
                "content": "Accessing the employee database"
            }
        ]
    }

@tool
def leave_management(user_info: str):
    """Enter the leave management department."""
    return {
        "dialog_state": ["Human_Resource"],
        "messages": [
            {
                "type": "text",
                "content": "Entering the leave management department"
            }
        ]
    }