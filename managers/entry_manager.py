# managers/entry_manager.py

class EntryManager:
    """
    Decides position sizing or other entry logic.
    For now, always returns 1 contract if LONG/SHORT signal.
    """
    def __init__(self):
        pass

    def process_entry_signal(self, signal):
        if signal == "LONG":
            return {"direction": "LONG", "quantity": 1}
        elif signal == "SHORT":
            return {"direction": "SHORT", "quantity": 1}
        else:
            return None
