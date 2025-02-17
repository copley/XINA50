# execution/stop_loss_order_execution_logic.py

def create_stop_loss_order(action, quantity, stop_price):
    """
    Stub: Create a Stop order object.
    """
    return {
        "orderType": "STP",
        "action": action,  # "BUY" or "SELL"
        "totalQuantity": quantity,
        "auxPrice": stop_price
    }
