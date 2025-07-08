# Order placement logic (market, limit, etc.)
import logging
import time
from config import BINANCE_API_KEY, BINANCE_SECRET_KEY, BASE_URL
from binance.client import Client
from binance.exceptions import BinanceAPIException

class OrderManager:
    def __init__(self):
        self.client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_SECRET_KEY, testnet=True)
        self.logger = logging.getLogger("bot")
        
        # Sync server time to fix timestamp issues
        try:
            server_time = self.client.get_server_time()
            self.client.timestamp_offset = server_time['serverTime'] - int(time.time() * 1000)
        except Exception as e:
            self.logger.warning(f"Could not sync server time: {e}")
            self.client.timestamp_offset = 0

    def place_market_order(self, symbol, side, quantity):
        try:
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'MARKET',
                'quantity': quantity
            }
            self.logger.info(f"API Request: POST /fapi/v1/order, Params: {params}")
            order = self.client.futures_create_order(**params)
            self.logger.info(f"Order Placed: Market {side.title()}, {symbol}, Qty: {quantity}, Status: {order['status']}, Order ID: {order['orderId']}")
            return {
                'Type': f"Market {side.title()}",
                'Symbol': symbol,
                'Quantity': quantity,
                'Status': order['status'],
                'Order ID': order['orderId'],
                'Timestamp': order['updateTime']
            }, None
        except BinanceAPIException as e:
            self.logger.error(f"API Error: {e.status_code} - {e.message}")
            return None, f"API Error: {e.message}"
        except Exception as e:
            self.logger.error(f"Order Error: {str(e)}")
            return None, str(e)

    def place_limit_order(self, symbol, side, quantity, price):
        try:
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'LIMIT',
                'quantity': quantity,
                'price': price,
                'timeInForce': 'GTC'
            }
            self.logger.info(f"API Request: POST /fapi/v1/order, Params: {params}")
            order = self.client.futures_create_order(**params)
            self.logger.info(f"Order Placed: Limit {side.title()}, {symbol}, Qty: {quantity}, Price: {price}, Status: {order['status']}, Order ID: {order['orderId']}")
            return {
                'Type': f"Limit {side.title()}",
                'Symbol': symbol,
                'Quantity': quantity,
                'Price': price,
                'Status': order['status'],
                'Order ID': order['orderId'],
                'Timestamp': order['updateTime']
            }, None
        except BinanceAPIException as e:
            self.logger.error(f"API Error: {e.status_code} - {e.message}")
            return None, f"API Error: {e.message}"
        except Exception as e:
            self.logger.error(f"Order Error: {str(e)}")
            return None, str(e)

    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price):
        try:
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'STOP',
                'quantity': quantity,
                'price': limit_price,
                'stopPrice': stop_price,
                'timeInForce': 'GTC'
            }
            self.logger.info(f"API Request: POST /fapi/v1/order, Params: {params}")
            order = self.client.futures_create_order(**params)
            self.logger.info(f"Order Placed: Stop-Limit {side.title()}, {symbol}, Qty: {quantity}, Stop: {stop_price}, Limit: {limit_price}, Status: {order['status']}, Order ID: {order['orderId']}")
            return {
                'Type': f"Stop-Limit {side.title()}",
                'Symbol': symbol,
                'Quantity': quantity,
                'Stop Price': stop_price,
                'Limit Price': limit_price,
                'Status': order['status'],
                'Order ID': order['orderId'],
                'Timestamp': order['updateTime']
            }, None
        except BinanceAPIException as e:
            self.logger.error(f"API Error: {e.status_code} - {e.message}")
            return None, f"API Error: {e.message}"
        except Exception as e:
            self.logger.error(f"Order Error: {str(e)}")
            return None, str(e)

    def place_oco_order(self, symbol, side, quantity, take_profit_price, stop_loss_price):
        # OCO is not directly supported in Binance Futures, so we simulate with two orders
        try:
            # Place take-profit order
            tp_params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'TAKE_PROFIT_MARKET',
                'quantity': quantity,
                'stopPrice': take_profit_price,
                'reduceOnly': True
            }
            sl_params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'STOP_MARKET',
                'quantity': quantity,
                'stopPrice': stop_loss_price,
                'reduceOnly': True
            }
            self.logger.info(f"API Request: POST /fapi/v1/order (TP), Params: {tp_params}")
            tp_order = self.client.futures_create_order(**tp_params)
            self.logger.info(f"API Request: POST /fapi/v1/order (SL), Params: {sl_params}")
            sl_order = self.client.futures_create_order(**sl_params)
            self.logger.info(f"OCO Orders Placed: TP Order ID: {tp_order['orderId']}, SL Order ID: {sl_order['orderId']}")
            return {
                'Type': f"OCO {side.title()}",
                'Symbol': symbol,
                'Quantity': quantity,
                'Take Profit Price': take_profit_price,
                'Stop Loss Price': stop_loss_price,
                'TP Order ID': tp_order['orderId'],
                'SL Order ID': sl_order['orderId']
            }, None
        except BinanceAPIException as e:
            self.logger.error(f"API Error: {e.status_code} - {e.message}")
            return None, f"API Error: {e.message}"
        except Exception as e:
            self.logger.error(f"Order Error: {str(e)}")
            return None, str(e)

    def place_twap_order(self, symbol, side, total_quantity, duration_sec):
        # TWAP: Split total_quantity into N chunks and execute over duration_sec
        import time
        try:
            chunks = 10  # For simplicity, split into 10 chunks
            qty_per_chunk = total_quantity / chunks
            interval = duration_sec / chunks
            results = []
            for i in range(chunks):
                params = {
                    'symbol': symbol,
                    'side': side.upper(),
                    'type': 'MARKET',
                    'quantity': round(qty_per_chunk, 8)
                }
                self.logger.info(f"TWAP Chunk {i+1}: POST /fapi/v1/order, Params: {params}")
                try:
                    order = self.client.futures_create_order(**params)
                    results.append({'orderId': order['orderId'], 'status': order['status']})
                except Exception as e:
                    results.append({'error': str(e)})
                time.sleep(interval)
            self.logger.info(f"TWAP Orders Placed: {results}")
            return {'Type': 'TWAP', 'Symbol': symbol, 'Chunks': chunks, 'Results': results}, None
        except Exception as e:
            self.logger.error(f"TWAP Error: {str(e)}")
            return None, str(e)

    def place_grid_order(self, symbol, low_price, high_price, grid_levels, quantity_per_level, side='buy'):
        # Grid: Place limit orders at grid_levels between low_price and high_price
        try:
            price_step = (high_price - low_price) / (grid_levels - 1)
            orders = []
            for i in range(grid_levels):
                price = round(low_price + i * price_step, 2)
                params = {
                    'symbol': symbol,
                    'side': side.upper(),
                    'type': 'LIMIT',
                    'quantity': quantity_per_level,
                    'price': price,
                    'timeInForce': 'GTC'
                }
                self.logger.info(f"Grid Order {i+1}: POST /fapi/v1/order, Params: {params}")
                try:
                    order = self.client.futures_create_order(**params)
                    orders.append({'orderId': order['orderId'], 'price': price, 'status': order['status']})
                except Exception as e:
                    orders.append({'error': str(e), 'price': price})
            self.logger.info(f"Grid Orders Placed: {orders}")
            return {'Type': 'Grid', 'Symbol': symbol, 'Levels': grid_levels, 'Orders': orders}, None
        except Exception as e:
            self.logger.error(f"Grid Error: {str(e)}")
            return None, str(e)
