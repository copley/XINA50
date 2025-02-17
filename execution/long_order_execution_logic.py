# execution/long_order_execution_logic.py

def build_long_order(quantity):
    """
    Stub: Example logic to create a 'BUY' order at market or limit.
    """
    order = {
        "action": "BUY",
        "orderType": "MKT",
        "totalQuantity": quantity
    }
    return order
