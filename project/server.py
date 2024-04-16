import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.authenticate_user_service
import project.batch_convert_currency_service
import project.convert_currency_service
import project.create_user_profile_service
import project.register_user_service
import project.update_user_profile_service
import project.view_user_history_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="aarushi-currency-exchange-1",
    lifespan=lifespan,
    description="The endpoint design is focused on performing currency conversions by accepting a base currency and optionally one or more target currency codes. Leveraging the Python programming language with the FastAPI framework, the application will provide fast, asynchronous API responses. The backend will interact with PostgreSQL through Prisma, an ORM that offers robust data management and ease of use for Python developers.\n\nTo fulfill the task requirements, the API will perform the following steps:\n1. Accept a GET request with query parameters for the base currency (e.g., 'GBP') and target currency/currencies.\n2. Use the provided financial data APIs, such as Open Exchange Rates or CurrencyLayer, as the reliable sources for real-time exchange rate data. This choice is based on the search results for reliable sources.\n3. Implement an async function that fetches the latest exchange rates from the chosen API. This function will handle converting the base currency to the target currencies specified by the user. If 'all of them' is specified as the target, the function will fetch the exchange rates for the base currency against every available currency provided by the API.\n4. Calculate the exchange rate between the base and the target currencies using the data retrieved. This involves a straightforward calculation if direct rates are available, or a conversion path if direct rates are not provided.\n5. Format the response to include the exchange rate(s), the base currency, and target currencies, alongside a timestamp marking the exact time of the currency rate retrieval.\n\nThis setup ensures scalability for supporting multiple currencies, efficiency in fetching and calculating real-time exchange rates, and reliability by utilizing trusted financial data sources. The endpoint will be well-documented to guide users on how to specify base and target currencies correctly.",
)


@app.post(
    "/auth/login",
    response_model=project.authenticate_user_service.AuthenticateUserResponse,
)
async def api_post_authenticate_user(
    email: str, password: str
) -> project.authenticate_user_service.AuthenticateUserResponse | Response:
    """
    Authenticates user and returns a session token
    """
    try:
        res = await project.authenticate_user_service.authenticate_user(email, password)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/batch_convert",
    response_model=project.batch_convert_currency_service.BatchConversionResponse,
)
async def api_post_batch_convert_currency(
    base_currency: str, target_currencies: List[str]
) -> project.batch_convert_currency_service.BatchConversionResponse | Response:
    """
    Performs batch conversion from a base currency to multiple targets
    """
    try:
        res = await project.batch_convert_currency_service.batch_convert_currency(
            base_currency, target_currencies
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/user/history",
    response_model=project.view_user_history_service.ViewUserHistoryResponse,
)
async def api_get_view_user_history(
    user_id: str,
) -> project.view_user_history_service.ViewUserHistoryResponse | Response:
    """
    Retrieves the conversion history for a user
    """
    try:
        res = await project.view_user_history_service.view_user_history(user_id)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/convert/{base}/{targets}",
    response_model=project.convert_currency_service.ConvertCurrencyResponse,
)
async def api_get_convert_currency(
    base: str, targets: str
) -> project.convert_currency_service.ConvertCurrencyResponse | Response:
    """
    Converts base currency to target currencies using real-time exchange rates
    """
    try:
        res = await project.convert_currency_service.convert_currency(base, targets)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/auth/register",
    response_model=project.register_user_service.UserRegistrationResponse,
)
async def api_post_register_user(
    email: str, password: str, role: project.register_user_service.UserRole
) -> project.register_user_service.UserRegistrationResponse | Response:
    """
    Registers a new user and returns basic user information
    """
    try:
        res = await project.register_user_service.register_user(email, password, role)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/user",
    response_model=project.create_user_profile_service.CreateUserProfileResponse,
)
async def api_post_create_user_profile(
    email: str, password: str, username: str, role: str
) -> project.create_user_profile_service.CreateUserProfileResponse | Response:
    """
    Creates a new user profile
    """
    try:
        res = await project.create_user_profile_service.create_user_profile(
            email, password, username, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/user/{id}",
    response_model=project.update_user_profile_service.UpdateUserProfileResponse,
)
async def api_put_update_user_profile(
    id: str,
    email: Optional[str],
    username: Optional[str],
    role: project.update_user_profile_service.UserRole,
) -> project.update_user_profile_service.UpdateUserProfileResponse | Response:
    """
    Updates an existing user's profile
    """
    try:
        res = await project.update_user_profile_service.update_user_profile(
            id, email, username, role
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
