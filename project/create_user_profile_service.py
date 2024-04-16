from datetime import datetime

import bcrypt
import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class CreateUserProfileResponse(BaseModel):
    """
    The response model returning the newly created user profile's public information.
    """

    id: str
    email: str
    username: str
    role: str
    createdAt: datetime
    updatedAt: datetime


async def create_user_profile(
    email: str, password: str, username: str, role: str
) -> CreateUserProfileResponse:
    """
    Creates a new user profile in the database and returns information about the newly created user.

    Args:
    email (str): Email address of the new user. Used as the primary means of identification.
    password (str): The user's chosen password. This will be hashed before being stored.
    username (str): The unique username chosen by the user.
    role (str): The initial role assigned to the user. Defaults to 'USER'.

    Returns:
    CreateUserProfileResponse: The response model returning the newly created user profile's public information.
    """
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_role = (
        prisma.enums.UserRole.USER
        if role.upper() not in prisma.enums.UserRole._member_names_
        else prisma.enums.UserRole[role.upper()]
    )
    user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "password": hashed_password.decode("utf-8"),
            "role": user_role,
        }
    )
    return CreateUserProfileResponse(
        id=user.id,
        email=user.email,
        username=username,
        role=user.role.name,
        createdAt=user.createdAt,
        updatedAt=user.updatedAt,
    )
