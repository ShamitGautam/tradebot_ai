import logging
from typing import Dict, Any
from bot.client import BinanceClient
from bot.validators import validate_order_params

logger = logging.getLogger(__name__)


class OrderManager:
    """Manages order placement and validation."""

    def __init__(self, client: BinanceClient):
        """
        Initialize OrderManager.

        Args:
            client: BinanceClient instance
        """
        self.client = client

    def execute_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: str,
        price: str = None,
    ) -> Dict[str, Any]:
        """
        Execute a validated order.

        Args:
            symbol: Trading symbol
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity as string
            price: Order price as string (required for LIMIT)

        Returns:
            Order response dictionary

        Raises:
            ValueError: If validation fails
        """
        # Validate parameters
        symbol, side, order_type, quantity, price = validate_order_params(
            symbol, side, order_type, quantity, price
        )

        logger.info(
            f"Executing order - Symbol: {symbol}, Side: {side.value}, "
            f"Type: {order_type.value}, Qty: {quantity}, Price: {price}"
        )

        # Place the order
        response = self.client.place_order(
            symbol=symbol,
            side=side.value,
            order_type=order_type.value,
            quantity=quantity,
            price=price,
        )

        return response

    @staticmethod
    def format_order_summary(
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float = None,
    ) -> str:
        """Format order request summary for display."""
        summary = f"\n{'='*60}\n"
        summary += "ORDER REQUEST SUMMARY\n"
        summary += f"{'='*60}\n"
        summary += f"Symbol:     {symbol}\n"
        summary += f"Side:       {side}\n"
        summary += f"Type:       {order_type}\n"
        summary += f"Quantity:   {quantity}\n"
        if price:
            summary += f"Price:      {price}\n"
        summary += f"{'='*60}\n"
        return summary

    @staticmethod
    def format_order_response(response: Dict[str, Any]) -> str:
        """Format order response for display."""
        result = f"\n{'='*60}\n"
        result += "ORDER RESPONSE DETAILS\n"
        result += f"{'='*60}\n"
        result += f"Order ID:       {response.get('orderId')}\n"
        result += f"Status:         {response.get('status')}\n"
        result += f"Symbol:         {response.get('symbol')}\n"
        result += f"Side:           {response.get('side')}\n"
        result += f"Type:           {response.get('type')}\n"
        result += f"Quantity:       {response.get('origQty')}\n"
        result += f"Executed Qty:   {response.get('executedQty')}\n"

        if response.get('avgPrice') and response.get('avgPrice') != '0':
            result += f"Avg Price:      {response.get('avgPrice')}\n"

        if response.get('price') and response.get('price') != '0':
            result += f"Price:          {response.get('price')}\n"

        result += f"{'='*60}\n"
        return result
