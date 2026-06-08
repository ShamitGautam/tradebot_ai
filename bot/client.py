import logging
from typing import Dict, Any, Optional
from binance.um_futures import UMFutures
from binance.exceptions import BinanceAPIException, BinanceConnectionError

logger = logging.getLogger(__name__)


class BinanceClient:
    """Wrapper for Binance Futures Testnet API interactions."""

    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        """
        Initialize Binance Futures client.

        Args:
            api_key: Binance API key
            api_secret: Binance API secret
            testnet: Use testnet (default) or mainnet

        Raises:
            ValueError: If credentials are missing
        """
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required")

        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet

        logger.info(f"Initializing Binance client ({'testnet' if testnet else 'mainnet'})")

        self.client = UMFutures(
            key=api_key,
            secret=api_secret,
            base_url="https://testnet.binancefuture.com" if testnet else "https://fapi.binance.com",
        )

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Place an order on Binance Futures Testnet.

        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT orders)

        Returns:
            Order response dictionary

        Raises:
            BinanceAPIException: If API returns an error
            BinanceConnectionError: If network connection fails
            ValueError: If parameters are invalid
        """
        try:
            logger.info(
                f"Placing {order_type} {side} order - Symbol: {symbol}, "
                f"Quantity: {quantity}, Price: {price}"
            )

            order_params = {
                "symbol": symbol,
                "side": side,
                "type": order_type,
                "quantity": quantity,
            }

            if order_type == "LIMIT":
                if price is None:
                    raise ValueError("Price is required for LIMIT orders")
                order_params["price"] = price
                order_params["timeInForce"] = "GTC"  # Good Till Cancel

            response = self.client.new_order(**order_params)

            logger.info(f"Order placed successfully: {response['orderId']}")
            return response

        except BinanceAPIException as e:
            logger.error(f"Binance API Error: {e.status_code} - {e.message}")
            raise
        except BinanceConnectionError as e:
            logger.error(f"Connection Error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing order: {e}")
            raise

    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information.

        Returns:
            Account info dictionary
        """
        try:
            logger.debug("Fetching account information")
            return self.client.account()
        except Exception as e:
            logger.error(f"Error fetching account info: {e}")
            raise

    def get_balance(self, asset: str = "USDT") -> float:
        """
        Get account balance for a specific asset.

        Args:
            asset: Asset symbol (default: USDT)

        Returns:
            Balance amount
        """
        try:
            account = self.get_account_info()
            for balance in account["assets"]:
                if balance["asset"] == asset:
                    return float(balance["walletBalance"])
            logger.warning(f"No balance found for {asset}")
            return 0.0
        except Exception as e:
            logger.error(f"Error getting balance: {e}")
            raise
