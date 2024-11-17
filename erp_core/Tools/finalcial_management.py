from langchain_core.tools import tool
import csv
@tool
def register_purchase_request(product: str, price: float):
    """Register a purchase request."""
    try:
        with open("purchase_requests.csv", "a") as f:    
            writer = csv.writer(f)
            writer.writerow([product, price])
    except Exception as e:
        pass

    return {
        "dialog_state": ["Financial_Management"],
        "messages": [
            {
                "type": "text",
                "content": f"Registering a purchase request for {product} at {price}"
            }
        ]
    }  
@tool
def view_expense_report(info: str):
    """View an expense report."""
    try:
        with open("expense_reports.csv", "r") as f:
            reader = csv.reader(f)
            expense_reports = list(reader)
    except Exception as e:
        expense_reports = []
    return {
        "dialog_state": ["Financial_Management"],
        "messages": [
            {
                "type": "text",
                "content": f"Expense report: {expense_reports}"
            }
        ]
    }