# indicators/logic1.py

from datetime import datetime, timedelta
from utils.helpers import align_to_bar_boundary

class TradeAggregator:
    """
    Aggregates raw trades into bars of 'bar_length' seconds.
    Also calculates running intraday VWAP, OBV, etc.
    """
    def __init__(self, bar_length=30):
        self.bar_length = bar_length
        self.delta = timedelta(seconds=bar_length)
        self.bar_start = None

        # Current bar stats
        self.open_price = None
        self.high_price = None
        self.low_price = None
        self.close_price = None
        self.volume = 0

        # Intraday VWAP
        self.cumulative_vp = 0.0  # sum(price*volume)
        self.cumulative_vol = 0.0

        # OBV
        self.current_OBV = 0.0
        self.prev_close_price = None

        # (Optional) for calibration tracking
        self.num_finalized_bars = 0

    def on_new_trade(self, trade_time: datetime, price: float, size: int):
        """
        Called by real-time ticks or by historical 'simulated' trades.
        """
        # Initialize bar_start if needed
        if self.bar_start is None:
            candidate_start = align_to_bar_boundary(trade_time, self.bar_length)
            while trade_time >= candidate_start + self.delta:
                candidate_start += self.delta
            self.bar_start = candidate_start

        # If this trade crosses past the current bar window, finalize old bar(s)
        while trade_time >= self.bar_start + self.delta:
            self.finalize_bar()
            self.bar_start += self.delta

        self.update_current_bar(price, size)

    def update_current_bar(self, price, size):
        if self.open_price is None:
            self.open_price = price
            self.high_price = price
            self.low_price = price
            self.close_price = price
            self.volume = size
        else:
            self.close_price = price
            self.high_price = max(self.high_price, price)
            self.low_price = min(self.low_price, price)
            self.volume += size

        # VWAP increments
        self.cumulative_vp += price * size
        self.cumulative_vol += size

        # OBV logic
        if self.prev_close_price is not None:
            if price > self.prev_close_price:
                self.current_OBV += size
            elif price < self.prev_close_price:
                self.current_OBV -= size

        self.prev_close_price = price

    def finalize_bar(self):
        """
        Prints bar info (for debugging) and resets bar stats.
        Does NOT reset cumulative VWAP/OBV (intraday).
        """
        if self.open_price is not None:
            bar_end_time = self.bar_start + self.delta
            intraday_vwap = None
            if self.cumulative_vol != 0:
                intraday_vwap = self.cumulative_vp / self.cumulative_vol

            print(f"[BAR] {self.bar_start.strftime('%H:%M:%S')} - "
                  f"{bar_end_time.strftime('%H:%M:%S')} | "
                  f"O={self.open_price:.2f}, H={self.high_price:.2f}, "
                  f"L={self.low_price:.2f}, C={self.close_price:.2f}, "
                  f"V={self.volume}, VWAP={intraday_vwap:.2f if intraday_vwap else 'N/A'}, "
                  f"OBV={self.current_OBV:.2f}")

            self.num_finalized_bars += 1

        # Reset bar stats
        self.open_price = None
        self.high_price = None
        self.low_price = None
        self.close_price = None
        self.volume = 0

    def check_force_finalize(self):
        """
        Optional: Force-close a bar if no trades for a while.
        """
        pass
