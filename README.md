# Trading Bot - Binance Futures Testnet

A simple, production-ready Python CLI application for placing market and limit orders on Binance Futures Testnet (USDT-M).

## Features

- ✅ Place **Market** and **Limit** orders on Binance Futures Testnet
- ✅ Support for **BUY** and **SELL** operations
- ✅ Clean CLI with input validation and confirmation
- ✅ Structured code with separate API and CLI layers
- ✅ Comprehensive logging to file and console
- ✅ Proper exception handling for API and network errors
- ✅ Account balance checking
- ✅ Type hints throughout
- ✅ Production-ready error messages

## Architecture

```
trading_bot/
├── bot/
│   ├── __init__.py           # Package exports
│   ├── client.py             # Binance API wrapper
│   ├── orders.py             # Order management logic
│   ├── validators.py         # Input validation
│   └── logging_config.py     # Logging setup
├── cli.py                    # CLI entry point (Click)
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## Requirements

- Python 3.8+
- Binance Futures Testnet account with API credentials

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Binance Testnet credentials

You have two options:

**Option A: Store credentials in `.env` file (recommended)**
```bash
python cli.py init
# Follow the prompts to enter your API key and secret
```

**Option B: Pass credentials via environment variables**
```bash
export API_KEY=your_api_key
export API_SECRET=your_api_secret

# On Windows (PowerShell)
$env:API_KEY="your_api_key"
$env:API_SECRET="your_api_secret"
```

## Usage

### Place a Market Order

```bash
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Place a Limit Order

```bash
python cli.py order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000
```

### Check Account Balance

```bash
python cli.py balance
```

### Interactive Mode (with prompts)

```bash
python cli.py order
# Then follow the on-screen prompts
```

### With inline credentials (not recommended for security)

```bash
python cli.py order \
  --api-key your_key \
  --api-secret your_secret \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.01
```

## Examples

### Example 1: Market Buy Order

```bash
$ python cli.py order \
  --symbol BTCUSDT \
  --side BUY \
  --type MARKET \
  --quantity 0.01

============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:     BTCUSDT
Side:       BUY
Type:       MARKET
Quantity:   0.01
============================================================

Proceed with this order? [y/N]: y

Processing order...

============================================================
ORDER RESPONSE DETAILS
============================================================
Order ID:       12345678
Status:         FILLED
Symbol:         BTCUSDT
Side:           BUY
Type:           MARKET
Quantity:       0.01
Executed Qty:   0.01
Avg Price:      42500.50
============================================================

✓ Order placed successfully!
```

### Example 2: Limit Sell Order

```bash
$ python cli.py order \
  --symbol ETHUSDT \
  --side SELL \
  --type LIMIT \
  --quantity 0.5 \
  --price 2500

============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:     ETHUSDT
Side:       SELL
Type:       LIMIT
Quantity:   0.5
Price:      2500
============================================================

Proceed with this order? [y/N]: y

Processing order...

============================================================
ORDER RESPONSE DETAILS
============================================================
Order ID:       87654321
Status:         NEW
Symbol:         ETHUSDT
Side:           SELL
Type:           LIMIT
Quantity:       0.5
Executed Qty:   0.0
Price:          2500
============================================================

✓ Order placed successfully!
```

## Logging

All API requests, responses, and errors are logged to:
- **Console**: INFO level and above (user-facing)
- **File**: `logs/trading_bot_YYYYMMDD_HHMMSS.log` (DEBUG level and above)

### Log File Location
```
logs/trading_bot_20240101_143022.log
```

### Example Log Content
```
2024-01-01 14:30:22 - trading_bot - INFO - Initializing Binance client (testnet)
2024-01-01 14:30:23 - trading_bot - INFO - Placing MARKET BUY order - Symbol: BTCUSDT, Quantity: 0.01, Price: None
2024-01-01 14:30:24 - trading_bot - INFO - Order placed successfully: 12345678
2024-01-01 14:31:00 - trading_bot - INFO - Placing LIMIT SELL order - Symbol: ETHUSDT, Quantity: 0.5, Price: 2500.0
2024-01-01 14:31:01 - trading_bot - INFO - Order placed successfully: 87654321
```

## Input Validation

The application validates:
- **Symbol**: Must end with USDT (USDT-M pairs only)
- **Side**: Must be BUY or SELL
- **Order Type**: Must be MARKET or LIMIT
- **Quantity**: Must be a positive number
- **Price**: Must be a positive number (required for LIMIT, optional for MARKET)

## Error Handling

The application handles:
- ✅ Invalid user input (validation errors)
- ✅ Missing or invalid API credentials
- ✅ Binance API errors (returned by server)
- ✅ Network connection errors
- ✅ Unexpected exceptions

All errors are logged to file for debugging and displayed to the user with clear messages.

## Important Notes & Assumptions

1. **Testnet Only**: This application is configured for Binance Futures Testnet. To use mainnet, modify the `base_url` in `bot/client.py`.

2. **USDT-M Pairs Only**: Only USDT Margin (USDT-M) perpetual futures pairs are supported.

3. **GTC Orders**: LIMIT orders use "Good Till Cancel" (GTC) time in force.

4. **No Risk Management**: This is a trading tool, not a trading system. Users are responsible for:
   - Position management
   - Risk limits
   - Stop losses
   - Take profits

5. **Credentials Security**: 
   - Keep API credentials secure
   - Use read-only API keys if possible
   - Never commit `.env` to version control

6. **Testnet Restrictions**:
   - Use testnet API key/secret only
   - No real funds are at risk
   - Balances reset periodically

## Troubleshooting

### "API key and secret are required"
Ensure you've either:
- Run `python cli.py init` to save credentials
- Set `API_KEY` and `API_SECRET` environment variables
- Passed `--api-key` and `--api-secret` flags

### "Invalid symbol"
Make sure the symbol ends with USDT (e.g., BTCUSDT, ETHUSDT)

### "Connection Error"
- Check your internet connection
- Verify the testnet URL is accessible
- Check if Binance Testnet is down

### "Price is required for LIMIT orders"
When placing a LIMIT order, you must provide the `--price` parameter

## Dependencies

- **python-binance**: Official Binance Python client
- **click**: CLI framework with interactive prompts
- **requests**: HTTP library (dependency of python-binance)

## File Structure After Running

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
├── logs/
│   ├── trading_bot_20240101_143022.log    # Market order example
│   └── trading_bot_20240101_143100.log    # Limit order example
├── .env                                   # API credentials (created by `init`)
├── cli.py
├── requirements.txt
└── README.md
```

## Next Steps / Enhancements

Potential improvements (not implemented in basic version):

1. **Advanced Order Types**:
   - Stop-Limit orders
   - One-Cancels-Other (OCO) orders
   - Time-Weighted Average Price (TWAP)

2. **Enhanced CLI**:
   - Interactive menu system
   - Order history display
   - Real-time order tracking

3. **Lightweight UI**:
   - Web dashboard
   - Order status monitoring

## License

MIT

## Author

Created for Binance Futures Testnet trading automation.
