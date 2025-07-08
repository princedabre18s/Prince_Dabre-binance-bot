# Binance Futures Trading Bot

## Project Overview
A CLI-based trading bot for Binance Futures Testnet (USDT-M). Supports market and limit orders, as well as advanced order types (stop-limit, OCO, TWAP, grid), with modular code, robust input validation, structured logging, and comprehensive error handling. The code and structure strictly follow the assignment prompt.

## Setup Instructions
1. Clone the repo:
   ```bash
   git clone <repo_url>
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set environment variables for API credentials:
   - Create a `.env` file in the root directory (see `.env.example`).
   - Or set environment variables:
     ```bash
     export BINANCE_API_KEY="your_api_key"
     export BINANCE_SECRET_KEY="your_secret_key"
     ```
   - The bot uses `python-dotenv` to load credentials from `.env` automatically.
4. Ensure you have a Binance Futures Testnet account.

## Running the Bot
- Start the bot with CLI commands as below:
  ```bash
  python main.py market buy BTCUSDT 0.01
  python main.py limit sell ETHUSDT 0.05 1800.50
  python main.py stop-limit buy BTCUSDT 0.01 30000 29500
  python main.py oco sell BTCUSDT 0.01 35000 28000
  python main.py twap buy BTCUSDT 0.1 3600
  python main.py grid BTCUSDT 28000 32000 5 0.01
  ```
  python main.py history BTCUSDT 1h 10
  python main.py fear-greed

## Usage Guide
- Place market, limit, advanced orders, and use bonus features using the CLI as shown above.
- Input requirements (e.g., quantity, price, duration, grid levels) are validated automatically against Binance rules.
- To fetch historical data:
  ```
  python main.py history BTCUSDT 1h 10
  ```
  This will print the last 10 hourly candles for BTCUSDT.
- To fetch the latest Crypto Fear & Greed Index:
  ```
  python main.py fear-greed
  ```
  This will print the current index value and classification.
- Example output for a successful order:
  ```
  Order Placed:
  Type: Market Buy
  Symbol: BTCUSDT
  Quantity: 0.01
  Status: Filled
  Order ID: 123456
  Timestamp: 2025-07-08 15:30:45
  ```
- Example output for an error:
  ```
  Error: Invalid quantity for BTCUSDT. Must be at least 0.001.
  ```

## Log File Explanation
- All actions and errors are logged in `bot.log` with timestamps in the format `YYYY-MM-DD HH:MM:SS`.
- Example log entries:
  ```
  2025-07-08 15:30:45 - INFO - API Request: POST /fapi/v1/order, Params: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01}
  2025-07-08 15:30:46 - INFO - Order Placed: Market Buy, BTCUSDT, Qty: 0.01, Status: Filled, Order ID: 123456
  2025-07-08 15:30:47 - ERROR - Invalid Price for Limit Order: Price must be positive
  ```

## Advanced Features
- Advanced order types (stop-limit, OCO, TWAP, grid) are implemented as per the assignment prompt.

## Troubleshooting
- Common issues:
  - Invalid API Key: Ensure you use testnet credentials and `.env` is set up.
  - Input validation errors: Follow CLI prompts for correct input format.
  - API/network errors: Check your internet connection and Binance Testnet status.
- Reference: [Binance API Docs](https://binance-docs.github.io/apidocs/futures/en/)
