# connection/ib_connection.py

import time
import threading
from datetime import datetime
import yaml
import os

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import TickAttribLast
from indicators.logic1 import TradeAggregator

def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

class IBApi(EWrapper, EClient):
    """
    IBApi is the main Interactive Brokers EClient/EWrapper class.
    It receives tick data and sends it to the aggregator.
    """
    def __init__(self, aggregator: TradeAggregator):
        EClient.__init__(self, self)
        self.aggregator = aggregator

    def error(self, reqId, errorCode, errorString):
        # Basic error logging
        print(f"[IB ERROR] reqId={reqId}, errorCode={errorCode}, msg={errorString}")

    def tickByTickAllLast(self, reqId: int, tickType: int,
                          time_: int, price: float, size: int,
                          tickAttribLast: TickAttribLast,
                          exchange: str, specialConditions: str):
        """
        Called for each incoming 'AllLast' tick. We pass
        the data to the aggregator to build bars.
        """
        trade_time = datetime.fromtimestamp(time_)
        self.aggregator.on_new_trade(trade_time, price, size)

def ib_run_loop(app: IBApi):
    """
    Runs the IB EClient loop in a background thread.
    """
    app.run()

def connect_ib(aggregator: TradeAggregator):
    """
    Create an IBApi instance, connect to TWS or IB Gateway,
    and start the API thread.
    """
    config = load_config()

    app = IBApi(aggregator)
    app.connect(
        config["ib_connection"]["host"],
        config["ib_connection"]["port"],
        config["ib_connection"]["client_id"]
    )

    # Start the API thread
    api_thread = threading.Thread(target=ib_run_loop, args=(app,), daemon=True)
    api_thread.start()

    # Give IB a moment to connect
    time.sleep(2)

    return app
