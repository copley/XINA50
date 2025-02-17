# utils/paper_trade_logger.py

import csv
import datetime
import os

class PaperTradeLogger:
    """
    Logs paper trades to a CSV file. 
    Each trade is one row with entry+exit info.
    """

    def __init__(self):
        dt_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"paper_trades_{dt_str}.csv"
        self.file = open(self.filename, mode="w", newline="")
        self.csv_writer = csv.writer(self.file)

        # Write header
        self.csv_writer.writerow([
            "Direction", "EntryTime", "EntryPrice",
            "StopLoss", "TakeProfit",
            "ExitTime", "ExitPrice", "ExitReason", "PnL"
        ])

        self.current_trade = None

    def start_trade(self, direction, entry_time, entry_price, stop_loss, take_profit):
        """
        Saves the entry details in memory (not written until exit).
        """
        self.current_trade = {
            "direction": direction,
            "entry_time": entry_time,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        }

    def end_trade(self, exit_time, exit_price, reason, pnl):
        """
        Completes the trade and writes the row (entry + exit).
        """
        if not self.current_trade:
            return

        row = [
            self.current_trade["direction"],
            self.current_trade["entry_time"].strftime("%Y-%m-%d %H:%M:%S"),
            self.current_trade["entry_price"],
            self.current_trade["stop_loss"],
            self.current_trade["take_profit"],
            exit_time.strftime("%Y-%m-%d %H:%M:%S"),
            exit_price,
            reason,
            pnl
        ]
        self.csv_writer.writerow(row)
        self.file.flush()
        self.current_trade = None

    def close(self):
        """
        Close the file when shutting down.
        """
        self.file.close()
        print(f"[INFO] PaperTradeLogger closed. Log saved to {self.filename}")
