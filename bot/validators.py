from enum import Enum
from typing import Tuple


class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"


def validate_symbol(symbol: str) -> str:
    """Validate and normalize trading symbol."""
    symbol = symbol.upper().strip()
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    if not symbol.endswith("USDT"):
        raise ValueError("Only USDT-M futures pairs supported (e.g., BTCUSDT)")
    return symbol


def validate_side(side: str) -> OrderSide:
    """Validate order side."""
    try:
        return OrderSide[side.upper()]
    except KeyError:
        raise ValueError(f"Side must be BUY or SELL, got {side}")


def validate_order_type(order_type: str) -> OrderType:
    """Validate order type."""
    try:
        return OrderType[order_type.upper()]
    except KeyError:
        raise ValueError(f"Order type must be MARKET or LIMIT, got {order_type}")


def validate_quantity(quantity: str) -> float:
    """Validate and convert quantity to float."""
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError("Quantity must be greater than 0")
        return qty
    except ValueError as e:
        raise ValueError(f"Invalid quantity: {e}")


def validate_price(price: str) -> float:
    """Validate and convert price to float."""
    try:
        p = float(price)
        if p <= 0:
            raise ValueError("Price must be greater than 0")
        return p
    except ValueError as e:
        raise ValueError(f"Invalid price: {e}")


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: str = None,
) -> Tuple[str, OrderSide, OrderType, float, float]:
    """
    Validate all order parameters.

    Args:
        symbol: Trading symbol
        side: BUY or SELL
        order_type: MARKET or LIMIT
        quantity: Order quantity
        price: Order price (required for LIMIT)

    Returns:
        Tuple of validated parameters

    Raises:
        ValueError: If any parameter is invalid
    """
    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_order_type = validate_order_type(order_type)
    validated_quantity = validate_quantity(quantity)

    if validated_order_type == OrderType.LIMIT:
        if not price:
            raise ValueError("Price is required for LIMIT orders")
        validated_price = validate_price(price)
    else:
        validated_price = None

    return validated_symbol, validated_side, validated_order_type, validated_quantity, validated_price
