from langchain_core.tools import tool

@tool
def product_quantity_check(product_name: str, quantity: int) -> str:
    """Check the quantity of a product in the supply chain."""
    return {
        "dialog_state": ["Supply_Chain_Management"],
        "messages": [
            {
                "type": "text",
                "content": f"The quantity of {product_name} is {quantity}."
            }
        ]
    }
