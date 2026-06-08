#!/usr/bin/env python
"""
Example script demonstrating programmatic usage of the trading bot.

This script shows how to use the bot's API directly in Python code,
without going through the CLI.
"""

import os
import logging
from bot import BinanceClient, OrderManager, setup_logging

# Setup logging
logger = setup_logging()

# Load API credentials from environment
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

if not API_KEY or not API_SECRET:
    print("Error: API_KEY and API_SECRET environment variables are required")
    print("Set them with: export API_KEY='your_key' && export API_SECRET='your_secret'")
    exit(1)


def example_market_order():
    """Example: Place a market buy order."""
    print("\n" + "="*60)
    print("Example 1: Market Buy Order")
    print("="*60)

    try:
        # Initialize client
        client = BinanceClient(API_KEY, API_SECRET, testnet=True)

        # Create order manager
        manager = OrderManager(client)

        # Place market order
        response = manager.execute_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="MARKET",
            quantity="0.01",
        )

        print(manager.format_order_response(response))
        print("✓ Market order example completed!")

    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error(f"Market order example failed: {e}")


def example_limit_order():
    """Example: Place a limit sell order."""
    print("\n" + "="*60)
    print("Example 2: Limit Sell Order")
    print("="*60)

    try:
        client = BinanceClient(API_KEY, API_SECRET, testnet=True)
        manager = OrderManager(client)

        response = manager.execute_order(
            symbol="ETHUSDT",
            side="SELL",
            order_type="LIMIT",
            quantity="0.5",
            price="2500",
        )

        print(manager.format_order_response(response))
        print("✓ Limit order example completed!")

    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error(f"Limit order example failed: {e}")


def example_check_balance():
    """Example: Check account balance."""
    print("\n" + "="*60)
    print("Example 3: Check Account Balance")
    print("="*60)

    try:
        client = BinanceClient(API_KEY, API_SECRET, testnet=True)
        balance = client.get_balance("USDT")
        print(f"USDT Balance: {balance} USDT")
        print("✓ Balance check example completed!")

    except Exception as e:
        print(f"✗ Error: {e}")
        logger.error(f"Balance check example failed: {e}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Trading Bot - Programmatic Usage Examples")
    print("="*60)

    # Uncomment the examples you want to run:

    # example_check_balance()
    # example_market_order()
    # example_limit_order()

    print("\n" + "="*60)
    print("To run examples, uncomment them in the script")
    print("IMPORTANT: Using real testnet credentials!")
    print("="*60)
