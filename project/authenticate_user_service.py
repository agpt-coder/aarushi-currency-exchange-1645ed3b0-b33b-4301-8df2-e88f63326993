import secrets
from datetime import datetime, timedelta

import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class AuthenticateUserResponse(BaseModel):
    """
    Response model for a successful authentication. Provides a session token for the authenticated session.
    """

    token: str
    user_id: str
    expires_at: datetime


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain text password matches the hashed password.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password obtained from the database.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


async def authenticate_user(email: str, password: str) -> AuthenticateUserResponse:
    """
    Authenticates user and returns a session token.

    Args:
    email (str): The user's email address used for login.
    password (str): The user's password for authentication.

    Returns:
    AuthenticateUserResponse: Response model for a successful authentication. Provides a session token for the authenticated session.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user:
        raise Exception("User not found or incorrect password")
    if not await verify_password(password, user.password):
        raise Exception("User not found or incorrect password")
    token = secrets.token_hex(16)
    expires_at = datetime.utcnow() + timedelta(days=1)
    auth_token = await prisma.models.AuthToken.prisma().create(
        data={"userId": user.id, "token": token, "expiresAt": expires_at}
    )
    return AuthenticateUserResponse(token=token, user_id=user.id, expires_at=expires_at)
