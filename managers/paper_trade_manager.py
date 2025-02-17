# managers/paper_trade_manager.py

from datetime import datetime

class PaperTradeManager:
    """
    Manages a single paper-trade position at a time.
    Logs entries and exits via the provided logger.
    Stop/Target are fixed offsets (example).
    """

    def __init__(self, logger, stop_offset=2.0, target_offset=4.0):
        self.logger = logger
        self.stop_offset = stop_offset
        self.target_offset = target_offset

        self.position_direction = None  # 'LONG' or 'SHORT'
        self.entry_price = None
        self.stop_price = None
        self.target_price = None
        self.entry_time = None

    def is_in_position(self):
        return self.position_direction is not None

    def open_position(self, direction, entry_price):
        """
        Open a new trade if none is currently open.
        """
        if self.is_in_position():
            return  # Already in a position, ignore

        self.position_direction = direction
        self.entry_price = entry_price
        self.entry_time = datetime.now()

        if direction == "LONG":
            self.stop_price = entry_price - self.stop_offset
            self.target_price = entry_price + self.target_offset
        else:  # SHORT
            self.stop_price = entry_price + self.stop_offset
            self.target_price = entry_price - self.target_offset

        # Log the entry
        self.logger.start_trade(
            direction=self.position_direction,
            entry_time=self.entry_time,
            entry_price=self.entry_price,
            stop_loss=self.stop_price,
            take_profit=self.target_price
        )

    def update_position(self, current_price):
        """
        Checks if stop or target is hit based on the bar's close price.
        Exits if triggered.
        """
        if not self.is_in_position():
            return

        if self.position_direction == "LONG":
            if current_price <= self.stop_price:
                self.exit_position(current_price, "STOP")
            elif current_price >= self.target_price:
                self.exit_position(current_price, "TARGET")

        else:  # SHORT
            if current_price >= self.stop_price:
                self.exit_position(current_price, "STOP")
            elif current_price <= self.target_price:
                self.exit_position(current_price, "TARGET")

    def exit_position(self, exit_price, reason):
        """
        Logs the exit, calculates PnL, resets position state.
        """
        if not self.is_in_position():
            return

        # Calculate PnL
        if self.position_direction == "LONG":
            pnl = exit_price - self.entry_price
        else:
            pnl = self.entry_price - exit_price

        exit_time = datetime.now()

        self.logger.end_trade(
            exit_time=exit_time,
            exit_price=exit_price,
            reason=reason,
            pnl=pnl
        )

        # Reset position
        self.position_direction = None
        self.entry_price = None
        self.stop_price = None
        self.target_price = None
        self.entry_time = None
