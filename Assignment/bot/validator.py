# Input validation functions
import requests
from config import BASE_URL

class Validator:
    def __init__(self):
        self.exchange_info = self._get_exchange_info()

    def _get_exchange_info(self):
        try:
            resp = requests.get(f"{BASE_URL}/fapi/v1/exchangeInfo")
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None

    def validate_symbol(self, symbol):
        if not self.exchange_info:
            return False, "Could not fetch exchange info."
        symbols = [s['symbol'] for s in self.exchange_info['symbols'] if s['contractType'] == 'PERPETUAL']
        if symbol.upper() not in symbols:
            return False, f"Invalid symbol. Enter a valid USDT-M pair like BTCUSDT."
        return True, ""

    def validate_quantity(self, symbol, quantity):
        try:
            quantity = float(quantity)
            if quantity <= 0:
                return False, "Quantity must be positive."
            # Check minQty and stepSize
            if not self.exchange_info:
                return False, "Could not fetch exchange info."
            for s in self.exchange_info['symbols']:
                if s['symbol'] == symbol.upper():
                    min_qty = float([f for f in s['filters'] if f['filterType'] == 'LOT_SIZE'][0]['minQty'])
                    step_size = float([f for f in s['filters'] if f['filterType'] == 'LOT_SIZE'][0]['stepSize'])
                    if quantity < min_qty:
                        return False, f"Quantity must be at least {min_qty} for {symbol}."
                    if (quantity * 1e8) % (step_size * 1e8) != 0:
                        return False, f"Quantity must be a multiple of {step_size} for {symbol}."
            return True, ""
        except Exception:
            return False, "Invalid quantity."

    def validate_price(self, symbol, price):
        try:
            price = float(price)
            if price <= 0:
                return False, "Price must be positive."
            if not self.exchange_info:
                return False, "Could not fetch exchange info."
            for s in self.exchange_info['symbols']:
                if s['symbol'] == symbol.upper():
                    min_price = float([f for f in s['filters'] if f['filterType'] == 'PRICE_FILTER'][0]['minPrice'])
                    tick_size = float([f for f in s['filters'] if f['filterType'] == 'PRICE_FILTER'][0]['tickSize'])
                    if price < min_price:
                        return False, f"Price must be at least {min_price} for {symbol}."
                    if (price * 1e8) % (tick_size * 1e8) != 0:
                        return False, f"Price must be a multiple of {tick_size} for {symbol}."
            return True, ""
        except Exception:
            return False, "Invalid price."

    def validate_market_order(self, symbol, side, quantity):
        valid, msg = self.validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = self.validate_quantity(symbol, quantity)
        if not valid:
            return False, msg
        if side.lower() not in ["buy", "sell"]:
            return False, "Side must be 'buy' or 'sell'."
        return True, ""

    def validate_limit_order(self, symbol, side, quantity, price):
        valid, msg = self.validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = self.validate_quantity(symbol, quantity)
        if not valid:
            return False, msg
        valid, msg = self.validate_price(symbol, price)
        if not valid:
            return False, msg
        if side.lower() not in ["buy", "sell"]:
            return False, "Side must be 'buy' or 'sell'."
        return True, ""

    def validate_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        valid, msg = self.validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = self.validate_quantity(symbol, quantity)
        if not valid:
            return False, msg
        valid, msg = self.validate_price(symbol, stop_price)
        if not valid:
            return False, f"Invalid stop price: {msg}"
        valid, msg = self.validate_price(symbol, limit_price)
        if not valid:
            return False, f"Invalid limit price: {msg}"
        if side.lower() not in ["buy", "sell"]:
            return False, "Side must be 'buy' or 'sell'."
        # Logical check: stop > limit for buy, stop < limit for sell
        try:
            stop = float(stop_price)
            limit = float(limit_price)
            if side.lower() == "buy" and stop <= limit:
                return False, "For buy, stop price must be greater than limit price."
            if side.lower() == "sell" and stop >= limit:
                return False, "For sell, stop price must be less than limit price."
        except Exception:
            return False, "Invalid stop/limit price."
        return True, ""

    def validate_oco_order(self, symbol, side, quantity, take_profit_price, stop_loss_price):
        valid, msg = self.validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = self.validate_quantity(symbol, quantity)
        if not valid:
            return False, msg
        valid, msg = self.validate_price(symbol, take_profit_price)
        if not valid:
            return False, f"Invalid take-profit price: {msg}"
        valid, msg = self.validate_price(symbol, stop_loss_price)
        if not valid:
            return False, f"Invalid stop-loss price: {msg}"
        if side.lower() not in ["buy", "sell"]:
            return False, "Side must be 'buy' or 'sell'."
        # Logical check: take-profit > stop-loss for buy, take-profit < stop-loss for sell
        try:
            tp = float(take_profit_price)
            sl = float(stop_loss_price)
            if side.lower() == "buy" and tp <= sl:
                return False, "For buy, take-profit price must be greater than stop-loss price."
            if side.lower() == "sell" and tp >= sl:
                return False, "For sell, take-profit price must be less than stop-loss price."
        except Exception:
            return False, "Invalid take-profit/stop-loss price."
        return True, ""

    def validate_twap_order(self, symbol, side, total_quantity, duration_sec):
        valid, msg = self.validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = self.validate_quantity(symbol, total_quantity)
        if not valid:
            return False, msg
        try:
            duration = int(duration_sec)
            if duration <= 0:
                return False, "Duration must be a positive integer (seconds)."
        except Exception:
            return False, "Invalid duration."
        if side.lower() not in ["buy", "sell"]:
            return False, "Side must be 'buy' or 'sell'."
        return True, ""

    def validate_grid_order(self, symbol, low_price, high_price, grid_levels, quantity_per_level):
        valid, msg = self.validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = self.validate_price(symbol, low_price)
        if not valid:
            return False, f"Invalid low price: {msg}"
        valid, msg = self.validate_price(symbol, high_price)
        if not valid:
            return False, f"Invalid high price: {msg}"
        try:
            low = float(low_price)
            high = float(high_price)
            levels = int(grid_levels)
            if low >= high:
                return False, "Low price must be less than high price."
            if levels < 2:
                return False, "Grid levels must be at least 2."
        except Exception:
            return False, "Invalid price or grid levels."
        valid, msg = self.validate_quantity(symbol, quantity_per_level)
        if not valid:
            return False, msg
        return True, ""
# Input validation functions
import requests
from config import BASE_URL

class Validator:
    def __init__(self):
        self.exchange_info = self._get_exchange_info()

    def _get_exchange_info(self):
        try:
            resp = requests.get(f"{BASE_URL}/fapi/v1/exchangeInfo")
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception:
            return None

    def validate_symbol(self, symbol):
        if not self.exchange_info:
            return False, "Could not fetch exchange info."
        symbols = [s['symbol'] for s in self.exchange_info['symbols'] if s['contractType'] == 'PERPETUAL']
        if symbol.upper() not in symbols:
            return False, f"Invalid symbol. Enter a valid USDT-M pair like BTCUSDT."
        return True, ""

    def validate_quantity(self, symbol, quantity):
        try:
            quantity = float(quantity)
            if quantity <= 0:
                return False, "Quantity must be positive."
            # Check minQty and stepSize
            if not self.exchange_info:
                return False, "Could not fetch exchange info."
            for s in self.exchange_info['symbols']:
                if s['symbol'] == symbol.upper():
                    min_qty = float([f for f in s['filters'] if f['filterType'] == 'LOT_SIZE'][0]['minQty'])
                    step_size = float([f for f in s['filters'] if f['filterType'] == 'LOT_SIZE'][0]['stepSize'])
                    if quantity < min_qty:
                        return False, f"Quantity must be at least {min_qty} for {symbol}."
                    if (quantity * 1e8) % (step_size * 1e8) != 0:
                        return False, f"Quantity must be a multiple of {step_size} for {symbol}."
            return True, ""
        except Exception:
            return False, "Invalid quantity."

    def validate_price(self, symbol, price):
        try:
            price = float(price)
            if price <= 0:
                return False, "Price must be positive."
            if not self.exchange_info:
                return False, "Could not fetch exchange info."
            for s in self.exchange_info['symbols']:
                if s['symbol'] == symbol.upper():
                    min_price = float([f for f in s['filters'] if f['filterType'] == 'PRICE_FILTER'][0]['minPrice'])
                    tick_size = float([f for f in s['filters'] if f['filterType'] == 'PRICE_FILTER'][0]['tickSize'])
                    if price < min_price:
                        return False, f"Price must be at least {min_price} for {symbol}."
                    if (price * 1e8) % (tick_size * 1e8) != 0:
                        return False, f"Price must be a multiple of {tick_size} for {symbol}."
            return True, ""
        except Exception:
            return False, "Invalid price."

    def validate_market_order(self, symbol, side, quantity):
        valid, msg = self.validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = self.validate_quantity(symbol, quantity)
        if not valid:
            return False, msg
        if side.lower() not in ["buy", "sell"]:
            return False, "Side must be 'buy' or 'sell'."
        return True, ""

    def validate_limit_order(self, symbol, side, quantity, price):
        valid, msg = self.validate_symbol(symbol)
        if not valid:
            return False, msg
        valid, msg = self.validate_quantity(symbol, quantity)
        if not valid:
            return False, msg
        valid, msg = self.validate_price(symbol, price)
        if not valid:
            return False, msg
        if side.lower() not in ["buy", "sell"]:
            return False, "Side must be 'buy' or 'sell'."
        return True, ""
