# Entry point for the Binance Futures Trading Bot CLI
import sys
from bot.orders import OrderManager
from bot.validator import Validator
from bot.logger import setup_logger
import logging

def print_usage():
    print("""
Usage:
  python main.py market buy|sell SYMBOL QUANTITY
  python main.py limit buy|sell SYMBOL QUANTITY PRICE
  # Advanced order types can be added here
Example:
  python main.py market buy BTCUSDT 0.01
  python main.py limit sell ETHUSDT 0.05 1800.50
    """)

def main():
    setup_logger()
    logger = logging.getLogger("bot")
    args = sys.argv[1:]
    if len(args) < 1:
        print_usage()
        return

    order_manager = OrderManager()
    validator = Validator()

    order_type = args[0].lower()
    if order_type == "market":
        if len(args) != 4:
            print("Error: Invalid arguments for market order.")
            print_usage()
            return
        _, side, symbol, quantity = args
        valid, msg = validator.validate_market_order(symbol, side, quantity)
        if not valid:
            print(f"Error: {msg}")
            logger.error(f"Invalid Market Order Input: {msg}")
            return
        result, error = order_manager.place_market_order(symbol, side, float(quantity))
        if error:
            print(f"Error: {error}")
        else:
            print("Order Placed:")
            for k, v in result.items():
                print(f"{k}: {v}")
    elif order_type == "limit":
        if len(args) != 5:
            print("Error: Invalid arguments for limit order.")
            print_usage()
            return
        _, side, symbol, quantity, price = args
        valid, msg = validator.validate_limit_order(symbol, side, quantity, price)
        if not valid:
            print(f"Error: {msg}")
            logger.error(f"Invalid Limit Order Input: {msg}")
            return
        result, error = order_manager.place_limit_order(symbol, side, float(quantity), float(price))
        if error:
            print(f"Error: {error}")
        else:
            print("Order Placed:")
            for k, v in result.items():
                print(f"{k}: {v}")
    elif order_type == "stop-limit":
        if len(args) != 6:
            print("Error: Invalid arguments for stop-limit order.")
            print("Usage: python main.py stop-limit buy|sell SYMBOL QUANTITY STOP_PRICE LIMIT_PRICE")
            return
        _, side, symbol, quantity, stop_price, limit_price = args
        valid, msg = validator.validate_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
        if not valid:
            print(f"Error: {msg}")
            logger.error(f"Invalid Stop-Limit Order Input: {msg}")
            return
        result, error = order_manager.place_stop_limit_order(symbol, side, float(quantity), float(stop_price), float(limit_price))
        if error:
            print(f"Error: {error}")
        else:
            print("Order Placed:")
            for k, v in result.items():
                print(f"{k}: {v}")
    elif order_type == "oco":
        if len(args) != 6:
            print("Error: Invalid arguments for oco order.")
            print("Usage: python main.py oco buy|sell SYMBOL QUANTITY TAKE_PROFIT STOP_LOSS")
            return
        _, side, symbol, quantity, tp_price, sl_price = args
        valid, msg = validator.validate_oco_order(symbol, side, quantity, tp_price, sl_price)
        if not valid:
            print(f"Error: {msg}")
            logger.error(f"Invalid OCO Order Input: {msg}")
            return
        result, error = order_manager.place_oco_order(symbol, side, float(quantity), float(tp_price), float(sl_price))
        if error:
            print(f"Error: {error}")
        else:
            print("Order Placed:")
            for k, v in result.items():
                print(f"{k}: {v}")
    elif order_type == "twap":
        if len(args) != 5:
            print("Error: Invalid arguments for twap order.")
            print("Usage: python main.py twap buy|sell SYMBOL TOTAL_QUANTITY DURATION_SEC")
            return
        _, side, symbol, total_quantity, duration_sec = args
        valid, msg = validator.validate_twap_order(symbol, side, total_quantity, duration_sec)
        if not valid:
            print(f"Error: {msg}")
            logger.error(f"Invalid TWAP Order Input: {msg}")
            return
        result, error = order_manager.place_twap_order(symbol, side, float(total_quantity), int(duration_sec))
        if error:
            print(f"Error: {error}")
        else:
            print("Order Placed:")
            for k, v in result.items():
                print(f"{k}: {v}")
    elif order_type == "grid":
        if len(args) != 7:
            print("Error: Invalid arguments for grid order.")
            print("Usage: python main.py grid SYMBOL LOW_PRICE HIGH_PRICE GRID_LEVELS QTY_PER_LEVEL")
            return
        _, symbol, low_price, high_price, grid_levels, qty_per_level = args[0:6]
        valid, msg = validator.validate_grid_order(symbol, low_price, high_price, grid_levels, qty_per_level)
        if not valid:
            print(f"Error: {msg}")
            logger.error(f"Invalid Grid Order Input: {msg}")
            return
        result, error = order_manager.place_grid_order(symbol, float(low_price), float(high_price), int(grid_levels), float(qty_per_level))
        if error:
            print(f"Error: {error}")
        else:
            print("Order Placed:")
            for k, v in result.items():
                print(f"{k}: {v}")
    elif order_type == "history":
        # Usage: python main.py history SYMBOL INTERVAL LIMIT
        if len(args) != 4:
            print("Usage: python main.py history SYMBOL INTERVAL LIMIT")
            return
        _, symbol, interval, limit = args
        try:
            from binance.client import Client
            from config import BINANCE_API_KEY, BINANCE_SECRET_KEY
            client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY, testnet=True)
            klines = client.futures_klines(symbol=symbol.upper(), interval=interval, limit=int(limit))
            print(f"Historical Data for {symbol.upper()} ({interval}, last {limit}):")
            for k in klines:
                print(f"Open Time: {k[0]}, Open: {k[1]}, High: {k[2]}, Low: {k[3]}, Close: {k[4]}, Volume: {k[5]}")
        except Exception as e:
            print(f"Error fetching historical data: {e}")
    elif order_type == "fear-greed":
        # Usage: python main.py fear-greed
        try:
            import requests
            url = "https://api.alternative.me/fng/"  # Public API for Fear & Greed Index
            resp = requests.get(url)
            if resp.status_code == 200:
                data = resp.json()
                value = data['data'][0]['value']
                value_classification = data['data'][0]['value_classification']
                timestamp = data['data'][0]['timestamp']
                print(f"Crypto Fear & Greed Index: {value} ({value_classification}) at {timestamp}")
            else:
                print("Could not fetch Fear & Greed Index (API error)")
        except Exception as e:
            print(f"Error fetching Fear & Greed Index: {e}")
    else:
        print(f"Error: Unknown order type '{order_type}'.")
        print_usage()

if __name__ == "__main__":
    main()
