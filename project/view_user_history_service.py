from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class ConversionRecord(BaseModel):
    """
    A single record of a currency conversion transaction, detailing the base and target currencies, the exchange rate used, and the timestamp of the transaction.
    """

    base_currency: str
    target_currency: str
    exchange_rate: float
    timestamp: str


class ViewUserHistoryResponse(BaseModel):
    """
    This model outlines the structure of the response containing a user's currency conversion history. It includes an array of conversion records with details about each transaction.
    """

    history: List[ConversionRecord]


async def view_user_history(user_id: str) -> ViewUserHistoryResponse:
    """
    Retrieves the conversion history for a user

    Args:
    user_id (str): The unique identifier for the user whose conversion history is being requested.

    Returns:
    ViewUserHistoryResponse: This model outlines the structure of the response containing a user's currency conversion history. It includes an array of conversion records with details about each transaction.
    """
    conversion_query_records = await prisma.models.CurrencyQuery.prisma().find_many(
        where={"userId": user_id}, order={"timestamp": "desc"}
    )
    conversion_records = [
        ConversionRecord(
            base_currency=record.baseCurrency,
            target_currency=record.targetCurrency,
            exchange_rate=record.exchangeRate,
            timestamp=record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        )
        for record in conversion_query_records
    ]
    return ViewUserHistoryResponse(history=conversion_records)
