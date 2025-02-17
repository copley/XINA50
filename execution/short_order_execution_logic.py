# execution/short_order_execution_logic.py

def build_short_order(quantity):
    """
    Stub: Example logic to create a 'SELL' order at market or limit.
    """
    order = {
        "action": "SELL",
        "orderType": "MKT",
        "totalQuantity": quantity
    }
    return order
