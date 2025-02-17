# data/data_loader.py

import threading
import time
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from datetime import datetime

class HistDataApp(EWrapper, EClient):
    """
    A lightweight IB app to fetch historical data.
    It stores bars in 'historical_bars'.
    """
    def __init__(self):
        EClient.__init__(self, self)
        self.historical_bars = []

    def historicalData(self, reqId, bar):
        """
        Called for each historical bar returned by reqHistoricalData().
        'bar' has fields: date, open, high, low, close, volume, etc.
        """
        bar_time = bar.date  # string date/time
        self.historical_bars.append({
            "time": bar_time,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume
        })

    def historicalDataEnd(self, reqId, start, end):
        """
        Called once historical data download finishes.
        """
        print(f"[INFO] Historical data download finished. Received {len(self.historical_bars)} bars.")
        self.disconnect()

def get_historical_data(contract: Contract, durationStr="1800 S", barSize="30 secs"):
    """
    Fetch historical data (e.g., the last 1800 seconds ~ 30 mins, 30-sec bars).
    """
    app = HistDataApp()
    # Use a separate clientId so we don't conflict with the main real-time connection
    app.connect("127.0.0.1", 7496, clientId=9999)

    # Start the thread
    hist_thread = threading.Thread(target=app.run, daemon=True)
    hist_thread.start()

    # Request historical data
    app.reqHistoricalData(
        reqId=1,
        contract=contract,
        endDateTime="",        # now
        durationStr=durationStr,
        barSizeSetting=barSize,
        whatToShow="TRADES",   # or MIDPOINT, etc.
        useRTH=0,
        formatDate=1,          # "YYYYMMDD HH:mm:ss" format
        keepUpToDate=False,
        chartOptions=[]
    )

    # Wait until data finishes
    while app.isConnected():
        time.sleep(1)

    return app.historical_bars
