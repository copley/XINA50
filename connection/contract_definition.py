# connection/contract_definition.py

import yaml
import os
from ibapi.contract import Contract

def load_config():
    """
    Simple YAML config loader. Adjust path as needed.
    """
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def create_xina50_contract():
    config = load_config()

    contract = Contract()
    contract.symbol = config["symbol"]
    contract.secType = "FUT"
    contract.exchange = config["exchange"]
    contract.currency = config["currency"]
    contract.lastTradeDateOrContractMonth = config["lastTradeDateOrContractMonth"]
    contract.localSymbol = config["localSymbol"]
    contract.multiplier = "1"
    return contract
