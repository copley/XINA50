# indicators/logic2.py

def evaluate_scalp_signal(aggregator):
    """
    Example scalp logic:
    - LONG if last close > intraday VWAP & OBV > 0
    - SHORT if last close < intraday VWAP & OBV < 0
    - Otherwise FLAT
    """
    if aggregator.cumulative_vol == 0:
        return "FLAT"

    intraday_vwap = aggregator.cumulative_vp / aggregator.cumulative_vol
    if aggregator.close_price and intraday_vwap:
        if aggregator.close_price > intraday_vwap and aggregator.current_OBV > 0:
            return "LONG"
        elif aggregator.close_price < intraday_vwap and aggregator.current_OBV < 0:
            return "SHORT"

    return "FLAT"
