# Binance Futures Trading Bot Assignment

## Objective
Develop a **command-line interface (CLI)-based trading bot** in Python for the **Binance Futures Testnet (USDT-M)**. The bot must place and manage trading orders using the official Binance Futures Testnet API (`https://testnet.binancefuture.com`). It should support multiple order types, feature robust input validation, structured logging, comprehensive error handling, and clear documentation. The code must be modular, reusable, and submitted in a specific file structure with detailed instructions for setup and usage.

---

## Key Features and Functionalities

### 1. Core Order Types (Mandatory)
The bot must support the following order types, allowing both **buy** and **sell** sides:
- **Market Orders**:
  - Execute immediate buy/sell orders at the current market price.
  - Inputs: Trading pair (e.g., `BTCUSDT`), quantity (e.g., `0.01`).
  - Example CLI command: `python main.py market buy BTCUSDT 0.01`
- **Limit Orders**:
  - Place buy/sell orders at a user-specified price, executed only when the market reaches that price.
  - Inputs: Trading pair, quantity, price (e.g., `30000.50`).
  - Example CLI command: `python main.py limit sell ETHUSDT 0.05 1800.50`

### 2. Advanced Order Types (Optional - Bonus Points)
Implementing at least one of these advanced order types will earn bonus points and higher evaluation priority:
- **Stop-Limit Orders**:
  - Trigger a limit order when the market hits a user-defined stop price.
  - Inputs: Trading pair, quantity, stop price, limit price.
  - Example CLI command: `python main.py stop-limit buy BTCUSDT 0.01 30000 29500`
- **OCO (One-Cancels-the-Other) Orders**:
  - Place a take-profit and stop-loss order simultaneously; if one executes, the other is canceled.
  - Inputs: Trading pair, quantity, take-profit price, stop-loss price.
  - Example CLI command: `python main.py oco sell BTCUSDT 0.01 35000 28000`
- **TWAP (Time-Weighted Average Price) Orders**:
  - Split a large order into smaller chunks executed over a specified time period to minimize market impact.
  - Inputs: Trading pair, total quantity, time duration (e.g., `3600` seconds).
  - Example CLI command: `python main.py twap buy BTCUSDT 0.1 3600`
- **Grid Orders**:
  - Automate buy-low/sell-high orders within a user-defined price range.
  - Inputs: Trading pair, price range (low/high), number of grid levels, quantity per level.
  - Example CLI command: `python main.py grid BTCUSDT 28000 32000 5 0.01`

### 3. Input Validation
- Validate all user inputs before sending API requests:
  - **Trading Pair**: Must be a valid USDT-M pair (e.g., `BTCUSDT`, `ETHUSDT`). Check against Binance’s API (`/fapi/v1/exchangeInfo`).
  - **Quantity**: Positive number, adheres to Binance’s minimum order size and precision rules.
  - **Price** (for limit orders): Positive number, within Binance’s price precision.
  - **Stop Price** (for stop-limit): Logical relative to limit price (e.g., stop price > limit price for buy).
  - **Time Duration** (for TWAP): Positive integer in seconds.
  - **Price Range** (for grid): Low price < high price, both positive.
- If validation fails, display a clear error message in the CLI (e.g., “Error: Quantity must be greater than 0.001 for BTCUSDT”) and log the error.

### 4. Logging
- Log all actions in a structured file named `bot.log`:
  - Use Python’s `logging` module for consistency.
  - Include timestamps in the format `YYYY-MM-DD HH:MM:SS` (e.g., `2025-07-08 15:30:45`).
  - Log:
    - API requests (e.g., endpoint, parameters).
    - API responses (e.g., order ID, status).
    - Errors (e.g., invalid input, API failures).
    - Order executions (e.g., “Market Buy Order: BTCUSDT, Qty: 0.01, Status: Filled”).
  - Example log entries:
    ```
    2025-07-08 15:30:45 - INFO - API Request: POST /fapi/v1/order, Params: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.01}
    2025-07-08 15:30:46 - INFO - Order Placed: Market Buy, BTCUSDT, Qty: 0.01, Status: Filled, Order ID: 123456
    2025-07-08 15:30:47 - ERROR - Invalid Price for Limit Order: Price must be positive
    ```
- Ensure logs are human-readable and appended (not overwritten) during bot operation.

### 5. Error Handling
- Handle API errors gracefully (e.g., rate limits, invalid requests, server downtime):
  - Retry failed requests for transient errors (e.g., “Service Unavailable”) with exponential backoff.
  - Log errors with details (e.g., error code, message).
  - Display user-friendly messages in the CLI (e.g., “API Error: Please try again later”).
- Handle CLI input errors:
  - Prompt users to retry invalid inputs without crashing.
  - Example: “Invalid symbol. Enter a valid pair like BTCUSDT.”
- Ensure the bot remains stable under all conditions.

### 6. Output
- Display order details and execution status in the CLI after each action:
  - Example output for a market order:
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

---

## Technical Requirements

- **Programming Language**: Python 3.8 or higher.
- **API Integration**:
  - Use the Binance Futures Testnet API (`https://testnet.binancefuture.com`).
  - Preferred method: `python-binance` library with `testnet=True`.
  - Alternative: Direct REST calls using `requests` library, ensuring the correct base URL.
  - WebSocket streams (if used) must use `wss://fstream.binancefuture.com`.
- **CLI Interface**:
  - Accept inputs via command-line arguments (e.g., `python main.py market buy BTCUSDT 0.01`).
  - Optionally, support an interactive menu for user convenience (bonus).
  - Display clear prompts and feedback for all actions.
- **Modularity**:
  - Organize code into functions or classes (e.g., `OrderManager`, `Validator`, `Logger`).
  - Example class structure (optional):
    ```python
    class TradingBot:
        def __init__(self):
            self.client = Client(testnet=True)  # Initialize Binance client
        def place_market_order(self, symbol, side, quantity):
            # Logic for market order
        def validate_input(self, symbol, quantity, price=None):
            # Input validation logic
    ```
- **Dependencies**:
  - List all required libraries in `requirements.txt` (e.g., `python-binance==1.0.19`, `requests==2.31.0`).
  - Install via `pip install -r requirements.txt`.

---

## File Structure and Organization

### Directory Structure
The project must follow this exact structure:
```
[your_name]-binance-bot/
├── main.py               # Main script to run the bot
├── bot/
│   ├── __init__.py       # Make bot/ a Python package
│   ├── orders.py         # Order placement logic (market, limit, etc.)
│   ├── validator.py      # Input validation functions
│   ├── logger.py         # Logging setup and utilities
├── config.py             # Configuration (e.g., API endpoint, settings)
├── bot.log               # Structured log file
├── requirements.txt      # Python dependencies
└── README.md             # Detailed project documentation
```
- **main.py**:
  - Entry point for the CLI.
  - Parses command-line arguments or runs an interactive menu.
  - Orchestrates order placement, validation, and logging.
- **bot/**:
  - Contains modular components:
    - `orders.py`: Functions/classes for placing orders.
    - `validator.py`: Functions for validating inputs.
    - `logger.py`: Configures and manages logging.
- **config.py**:
  - Stores settings like the API base URL (`https://testnet.binancefuture.com`).
  - Accesses API credentials via environment variables (e.g., `os.environ.get("BINANCE_API_KEY")`).
  - Example:
    ```python
    BASE_URL = "https://testnet.binancefuture.com"
    WEBSOCKET_URL = "wss://fstream.binancefuture.com"
    ```
- **bot.log**:
  - Generated by the bot to record all actions and errors.
  - Must be timestamped and readable.
- **requirements.txt**:
  - Example:
    ```
    python-binance==1.0.19
    requests==2.31.0
    python-dotenv==1.0.1
    ```
- **README.md**:
  - See the “Documentation” section below.

### Why This Structure?
- Promotes modularity and reusability.
- Separates concerns (execution, configuration, logging, validation).
- Aligns with Python best practices for package organization.

---

## Submission Guidelines

### 1. GitHub Repository
- Create a **private** GitHub repository named `[your_name]-binance-bot` (e.g., `john-binance-bot`).
- Push all files in the structure above to the repo.
- Add collaborators as specified by the employer (details provided separately).
- Exclude sensitive files:
  - Add `.env`, `bot.log`, `__pycache__`, and `.DS_Store` to `.gitignore`.
- Ensure the repo is clean and well-organized.

### 2. Zip File
- Compress the project folder into a zip file named `[your_name]_binance_bot.zip` (e.g., `john_binance_bot.zip`).
- Verify it contains all required files and matches the directory structure.
- Submit the zip file to `saami@bajarangs.com`, `nagasai@bajarangs.com`, and CC `sonika@primetrade.ai` with the subject:
  ```
  Junior Python Developer - Crypto Trading Bot
  ```

---

## Documentation (README.md)

The `README.md` must include the following sections, written clearly and professionally:

1. **Project Overview**:
   - Describe the bot’s purpose: A CLI-based trading bot for Binance Futures Testnet (USDT-M).
   - List supported features (market/limit orders, advanced orders if implemented).

2. **Setup Instructions**:
   - Explain how to set up the project:
     - Clone the repo: `git clone <repo_url>`.
     - Install dependencies: `pip install -r requirements.txt`.
     - Set environment variables for API credentials:
       ```bash
       export BINANCE_API_KEY="your_api_key"
       export BINANCE_SECRET_KEY="your_secret_key"
       ```
       Or use a `.env` file with `python-dotenv`.
   - Mention the need for a Binance Futures Testnet account.

3. **Running the Bot**:
   - Command to start: `python main.py`.
   - CLI command examples:
     ```bash
     python main.py market buy BTCUSDT 0.01
     python main.py limit sell ETHUSDT 0.05 1800.50
     python main.py oco buy BTCUSDT 0.01 30000 28000
     ```
   - If interactive mode is implemented, explain how to use it.

4. **Usage Guide**:
   - Detail how to place each order type (basic and advanced, if implemented).
   - Show sample CLI outputs:
     ```
     Order Placed:
     Type: Market Buy
     Symbol: BTCUSDT
     Quantity: 0.01
     Status: Filled
     ```
   - Explain input requirements (e.g., quantity precision).

5. **Log File Explanation**:
   - Describe the structure of `bot.log`.
   - Example entry:
     ```
     2025-07-08 15:30:45 - INFO - Order Placed: Market Buy, BTCUSDT, Qty: 0.01
     ```
   - Note that logs are appended and timestamped.

6. **Advanced Features** (if implemented):
   - Describe any bonus features (e.g., OCO orders, CLI menu).
   - Provide usage examples.

7. **Troubleshooting**:
   - Common issues and solutions (e.g., “Invalid API Key: Ensure testnet credentials are used”).
   - Reference Binance API docs: `https://binance-docs.github.io/apidocs/futures/en/`.

---

## Evaluation Criteria

The bot will be evaluated based on these criteria:

| **Criteria**          | **Weight** | **Details**                                                                 |
|-----------------------|------------|-----------------------------------------------------------------------------|
| **Basic Orders**      | 40%        | Market and limit orders function correctly with proper validation.          |
| **Advanced Orders**   | 30%        | Bonus for stop-limit, OCO, TWAP, or grid orders. Higher priority if robust. |
| **Logging**           | 15%        | Structured, timestamped logs capturing all actions and errors.              |
| **Documentation**     | 15%        | Clear, detailed README covering setup, usage, and examples.                 |

---

## Optional Enhancements (Bonus Points)
- Implement multiple advanced order types (e.g., Stop-Limit + OCO).
- Add CLI features:
  - Display account balance: Use `/fapi/v2/balance`.
  - Show order history: Use `/fapi/v1/allOrders`.
  - Interactive menu for easier navigation.
- Lightweight UI:
  - Basic web interface (e.g., using `Flask`) or enhanced CLI with `prompt_toolkit`.
- Real-time price monitoring via WebSocket (`wss://fstream.binancefuture.com`).

---

## Important Notes
- **API Endpoint**: All interactions must use `https://testnet.binancefuture.com` for REST and `wss://fstream.binancefuture.com` for WebSocket.
- **Credentials**: Never hardcode API keys or secrets. Use environment variables or a `.env` file.
- **Code Quality**:
  - Follow PEP 8 style guidelines.
  - Write clear comments and docstrings.
  - Ensure modularity (e.g., separate order logic from validation).
- **Testnet Behavior**:
  - Virtual funds are provided automatically.
  - Testnet resets monthly, clearing orders and refreshing balances.[](https://fsr-develop.com/blog-cscalp/tpost/k36bu1d4t1-what-is-binance-testnet-and-how-does-it)
- **Early Submission**:
  - Submit within 72 hours for priority consideration, as per the employer’s instructions.

---

## Summary
- Build a CLI trading bot for Binance Futures Testnet (USDT-M).
- Implement market and limit orders with robust validation.
- Optionally add advanced orders (Stop-Limit, OCO, TWAP, Grid) for bonus points.
- Log all actions in `bot.log` with timestamps.
- Handle errors gracefully and provide clear CLI feedback.
- Follow the specified file structure and submission guidelines.
- Document everything thoroughly in `README.md`.

This prompt provides all the details needed to create an excellent, production-ready trading bot. Good luck!




API Key
777f62daa187650178365c242a470ef4161d72ef5d3f2cab959d605e02838bcc
API Secret
d98e84b0ad8817697b22538051805be55e6345b765ff9d34289b6e3e1e0e055f