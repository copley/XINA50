# managers/take_profit_manager.py

class TakeProfitManager:
    """
    Manages take-profit (target) levels. 
    Could be dynamic or fixed.
    """
    def __init__(self, target_offset=4.0):
        self.target_offset = target_offset

    def compute_target(self, entry_price, direction):
        """
        Example: If LONG, target = entry_price + offset
        """
        if direction == "LONG":
            return entry_price + self.target_offset
        else:
            return entry_price - self.target_offset
