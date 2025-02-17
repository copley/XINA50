# execution/limit_order_execution_logic.py

def create_limit_order(action, quantity, limit_price):
    """
    Stub: Create a limit order object for future usage.
    """
    return {
        "orderType": "LMT",
        "action": action,
        "totalQuantity": quantity,
        "lmtPrice": limit_price
    }
