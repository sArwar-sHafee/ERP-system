from langchain_core.tools import tool

@tool
def project_status_check(project_name: str, status: str) -> str:
    """Check the status of a project."""
    return {
        "dialog_state": ["Project_Management"],
        "messages": [
            {
                "type": "text",
                "content": f"The status of {project_name} is {status}."
            }
        ]
    }
