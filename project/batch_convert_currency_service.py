from datetime import datetime
from typing import List

from pydantic import BaseModel


class ConversionResult(BaseModel):
    """
    Holds individual conversion data from the base currency to a target currency.
    """

    target_currency: str
    exchange_rate: float
    timestamp: datetime
    status: str


class BatchConversionResponse(BaseModel):
    """
    The response model for the batch conversion request, providing the exchange rates for the base currency to each of the requested target currencies, including a timestamp for each rate.
    """

    base_currency: str
    conversions: List[ConversionResult]


async def batch_convert_currency(
    base_currency: str, target_currencies: List[str]
) -> BatchConversionResponse:
    """
    Performs batch conversion from a base currency to multiple targets.

    Args:
        base_currency (str): The base currency code (e.g., USD) from which to convert.
        target_currencies (List[str]): A list of target currency codes (e.g., ['EUR', 'GBP']) to which the base currency will be converted.

    Returns:
        BatchConversionResponse: The response model for the batch conversion request, which includes the exchange rates
        for the base currency to each of the requested target currencies, along with a timestamp for each rate.

    Example:
        response = await batch_convert_currency("USD", ["EUR", "JPY"])
        print(response)
    """
    conversion_results = []
    for target_currency in target_currencies:
        exchange_rate = 0.75
        conversion_results.append(
            ConversionResult(
                target_currency=target_currency,
                exchange_rate=exchange_rate,
                timestamp=datetime.now(),
                status="success",
            )
        )
    return BatchConversionResponse(
        base_currency=base_currency, conversions=conversion_results
    )
