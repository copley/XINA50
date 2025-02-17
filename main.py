# main.py

import time
import sys

from connection.ib_connection import connect_ib
from connection.contract_definition import create_xina50_contract
from indicators.logic1 import TradeAggregator
from indicators.logic2 import evaluate_scalp_signal
from managers.entry_manager import EntryManager
from managers.paper_trade_manager import PaperTradeManager
from utils.paper_trade_logger import PaperTradeLogger

# For calibration
from data.data_loader import get_historical_data
from data.data_preprocessor import feed_historical_data_to_aggregator

def main():
    # 1) Create the aggregator (for 30-second bars) and the logger
    aggregator = TradeAggregator(bar_length=30)
    logger = PaperTradeLogger()

    # 2) Simple paper trade manager and entry manager
    paper_trade_mgr = PaperTradeManager(logger=logger, stop_offset=2.0, target_offset=4.0)
    entry_mgr = EntryManager()

    print("[INFO] Creating contract for XINA50...")
    contract = create_xina50_contract()

    # 3) Warm-up / calibration with historical data
    print("[INFO] Fetching historical data for calibration...")
    hist_bars = get_historical_data(contract, durationStr="1800 S", barSize="30 secs")
    print(f"[INFO] Fetched {len(hist_bars)} historical bars.")

    print("[INFO] Feeding historical data to aggregator for warm-up...")
    feed_historical_data_to_aggregator(aggregator, hist_bars)
    print("[INFO] Aggregator warmed up. Current intraday VWAP/OBV are primed.")

    # 4) Now connect to IB for real-time data
    print("[INFO] Connecting real-time to IB for paper trading...")
    app = connect_ib(aggregator)

    # 5) Request tick-by-tick data
    app.reqTickByTickData(
        reqId=1,
        contract=contract,
        tickType="AllLast",
        numberOfTicks=0,
        ignoreSize=False
    )

    print("[INFO] Running in real-time. Press Ctrl+C to exit.")

    try:
        while True:
            time.sleep(1)

            # Optionally finalize a bar if needed, or rely on aggregator's logic
            # aggregator.check_force_finalize()

            # Evaluate a scalp signal from aggregator's last bar
            signal = evaluate_scalp_signal(aggregator)

            # Example: skip signals if we haven't finalized at least X bars
            # so that there's enough warm-up data.
            MIN_BARS_FOR_CALIBRATION = 10
            if aggregator.num_finalized_bars < MIN_BARS_FOR_CALIBRATION:
                continue  # still warming up in real-time, skip signals

            # If no open position, consider an entry
            if not paper_trade_mgr.is_in_position():
                if signal in ("LONG", "SHORT"):
                    order_info = entry_mgr.process_entry_signal(signal)
                    if order_info and aggregator.close_price:
                        direction = order_info["direction"]
                        paper_trade_mgr.open_position(direction, aggregator.close_price)

            # If in a position, check if stop/target triggered
            if paper_trade_mgr.is_in_position() and aggregator.close_price:
                paper_trade_mgr.update_position(current_price=aggregator.close_price)

    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user. Finalizing last bar and closing logger.")
    finally:
        aggregator.finalize_bar()
        logger.close()
        app.disconnect()
        sys.exit(0)

if __name__ == "__main__":
    main()
