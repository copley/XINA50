# managers/stop_loss_manager.py

class StopLossManager:
    """
    If you want a specialized manager for stop-loss logic,
    separate from the generic PaperTradeManager.
    """
    def __init__(self, fixed_stop_offset=2.0):
        self.fixed_stop_offset = fixed_stop_offset

    def compute_stop_loss(self, entry_price, direction):
        """
        Example: If LONG, stop = entry_price - offset
        """
        if direction == "LONG":
            return entry_price - self.fixed_stop_offset
        else:
            return entry_price + self.fixed_stop_offset
