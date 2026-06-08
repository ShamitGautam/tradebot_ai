import os
import sys
import click
from pathlib import Path
from bot import BinanceClient, OrderManager, setup_logging
from bot.validators import OrderSide, OrderType
from binance.exceptions import BinanceAPIException, BinanceConnectionError

logger = None


def init_logger():
    """Initialize logger at module level."""
    global logger
    logger = setup_logging()


@click.group()
def cli():
    """
    Trading Bot for Binance Futures Testnet

    A simple CLI tool to place market and limit orders on Binance Futures.
    """
    init_logger()


@cli.command()
@click.option(
    "--api-key",
    prompt=True,
    hide_input=False,
    help="Your Binance Futures API key",
)
@click.option(
    "--api-secret",
    prompt=True,
    hide_input=True,
    help="Your Binance Futures API secret",
)
def init(api_key: str, api_secret: str):
    """
    Initialize and save API credentials.

    Credentials are stored in .env file in the current directory.
    """
    init_logger()

    try:
        # Create .env file
        with open(".env", "w") as f:
            f.write(f"API_KEY={api_key}\n")
            f.write(f"API_SECRET={api_secret}\n")

        logger.info("Credentials saved to .env file")
        click.secho("✓ Credentials saved successfully!", fg="green")

    except Exception as e:
        logger.error(f"Error saving credentials: {e}")
        click.secho(f"✗ Error: {e}", fg="red")


@cli.command()
@click.option("--symbol", prompt="Trading symbol (e.g., BTCUSDT)", help="Trading pair")
@click.option(
    "--side",
    type=click.Choice(["BUY", "SELL"], case_sensitive=False),
    prompt="Order side",
    help="BUY or SELL",
)
@click.option(
    "--type",
    "order_type",
    type=click.Choice(["MARKET", "LIMIT"], case_sensitive=False),
    prompt="Order type",
    help="MARKET or LIMIT",
)
@click.option("--quantity", prompt="Quantity", help="Order quantity")
@click.option(
    "--price",
    default=None,
    help="Price (required for LIMIT orders)",
)
@click.option(
    "--api-key",
    default=None,
    help="Binance API key (or set API_KEY env var)",
)
@click.option(
    "--api-secret",
    default=None,
    help="Binance API secret (or set API_SECRET env var)",
)
def order(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str,
    api_key: str,
    api_secret: str,
):
    """
    Place a market or limit order on Binance Futures Testnet.

    Examples:
        # Market buy
        python cli.py order --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

        # Limit sell
        python cli.py order --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 2000
    """
    init_logger()

    try:
        # Load credentials from env or CLI args
        api_key = api_key or os.getenv("API_KEY")
        api_secret = api_secret or os.getenv("API_SECRET")

        if not api_key or not api_secret:
            click.secho(
                "✗ Error: API credentials not provided.\n"
                "Use 'python cli.py init' to save credentials or pass --api-key and --api-secret",
                fg="red",
            )
            logger.error("Missing API credentials")
            sys.exit(1)

        # Initialize client and manager
        client = BinanceClient(api_key, api_secret, testnet=True)
        manager = OrderManager(client)

        # Display order summary
        click.echo(
            manager.format_order_summary(
                symbol=symbol.upper(),
                side=side.upper(),
                order_type=order_type.upper(),
                quantity=quantity,
                price=price,
            )
        )

        # Confirm order
        if not click.confirm("Proceed with this order?"):
            click.echo("Order cancelled.")
            logger.info("Order cancelled by user")
            return

        # Execute order
        click.echo("\nProcessing order...")
        response = manager.execute_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
        )

        # Display response
        click.echo(manager.format_order_response(response))

        status = response.get("status", "UNKNOWN")
        if status in ["FILLED", "PARTIALLY_FILLED", "NEW", "PENDING_CANCEL"]:
            click.secho("✓ Order placed successfully!", fg="green")
        else:
            click.secho(f"⚠ Order status: {status}", fg="yellow")

        logger.info(f"Order completed with status: {status}")

    except ValueError as e:
        click.secho(f"✗ Validation Error: {e}", fg="red")
        logger.error(f"Validation error: {e}")
        sys.exit(1)

    except BinanceAPIException as e:
        click.secho(
            f"✗ Binance API Error ({e.status_code}): {e.message}",
            fg="red",
        )
        logger.error(f"Binance API error: {e}")
        sys.exit(1)

    except BinanceConnectionError as e:
        click.secho(f"✗ Connection Error: {e}", fg="red")
        logger.error(f"Connection error: {e}")
        sys.exit(1)

    except Exception as e:
        click.secho(f"✗ Unexpected Error: {e}", fg="red")
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)


@cli.command()
@click.option(
    "--api-key",
    default=None,
    help="Binance API key (or set API_KEY env var)",
)
@click.option(
    "--api-secret",
    default=None,
    help="Binance API secret (or set API_SECRET env var)",
)
def balance(api_key: str, api_secret: str):
    """Check account balance."""
    init_logger()

    try:
        api_key = api_key or os.getenv("API_KEY")
        api_secret = api_secret or os.getenv("API_SECRET")

        if not api_key or not api_secret:
            click.secho("✗ Error: API credentials not provided", fg="red")
            sys.exit(1)

        client = BinanceClient(api_key, api_secret, testnet=True)
        balance = client.get_balance("USDT")

        click.echo(f"\nUSAT Balance: {balance} USDT\n")
        logger.info(f"Fetched balance: {balance} USDT")

    except Exception as e:
        click.secho(f"✗ Error: {e}", fg="red")
        logger.error(f"Error fetching balance: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
