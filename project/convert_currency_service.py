from datetime import datetime
from typing import List

import httpx
from pydantic import BaseModel


class TargetCurrencyDetail(BaseModel):
    """
    Holds the target currency code and the calculated exchange rate from the base currency.
    """

    currency_code: str
    exchange_rate: float


class ConvertCurrencyResponse(BaseModel):
    """
    Includes the conversion rate(s), base and target currency codes, and a timestamp. Designed to provide a comprehensive outcome of the conversion request.
    """

    base_currency: str
    target_currencies: List[TargetCurrencyDetail]
    timestamp: datetime


async def fetch_exchange_rate(base: str, targets: List[str]) -> dict:
    """
    Fetches the exchange rates for the base currency compared to the target currencies from an external API.

    Args:
        base (str): The base currency code.
        targets (List[str]): A list of target currency codes.

    Returns:
        dict: A dictionary with target currency codes as keys and exchange rates as values.
    """
    api_url = f"http://api.example.com/latest?access_key=API_KEY&base={base}&symbols={','.join(targets)}"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        if response.status_code == 200:
            data = response.json()
            rates = data["rates"]
            return rates
        else:
            return {}


async def convert_currency(base: str, targets: str) -> ConvertCurrencyResponse:
    """
    Converts base currency to target currencies using real-time exchange rates.

    Args:
        base (str): The base currency code to convert from, e.g., 'USD'.
        targets (str): A comma-separated string of target currency codes to convert to, e.g., 'EUR,JPY'. Can also accept a special keyword 'all' to convert to all available currencies.

    Returns:
        ConvertCurrencyResponse: Includes the conversion rate(s), base and target currency codes, and a timestamp. Designed to provide a comprehensive outcome of the conversion request.
    """
    all_targets = ["EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNH", "SEK", "NZD"]
    target_currencies = targets.split(",") if targets != "all" else all_targets
    rates = await fetch_exchange_rate(base, target_currencies)
    target_currency_details = [
        TargetCurrencyDetail(currency_code=target, exchange_rate=rates.get(target, 0))
        for target in target_currencies
        if target in rates
    ]
    return ConvertCurrencyResponse(
        base_currency=base,
        target_currencies=target_currency_details,
        timestamp=datetime.now(),
    )
