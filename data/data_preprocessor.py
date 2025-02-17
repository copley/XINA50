# data/data_preprocessor.py

from datetime import datetime
from indicators.logic1 import TradeAggregator

def feed_historical_data_to_aggregator(aggregator: TradeAggregator, hist_bars):
    """
    Takes the list of historical bars (1 bar every 30s, for instance)
    and simulates a single 'trade' at each bar's close price with the bar's volume.
    This helps 'warm up' VWAP, OBV, etc.
    """
    for bar in hist_bars:
        dt_str = bar["time"]  # e.g. "20230203 12:00:30"
        # IB typically gives date as "YYYYMMDD  HH:MM:SS"
        dt_obj = datetime.strptime(dt_str, "%Y%m%d  %H:%M:%S")

        # Feed aggregator one trade at the bar close
        aggregator.on_new_trade(dt_obj, bar["close"], bar["volume"])

    # Finalize the last partial bar
    aggregator.finalize_bar()
