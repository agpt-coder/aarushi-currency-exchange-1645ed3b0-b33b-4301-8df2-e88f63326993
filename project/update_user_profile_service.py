from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class UserRole(BaseModel):
    """
    An ENUM defining possible user roles within the system, including 'User', 'Admin', 'Premium'.
    """

    pass


class User(BaseModel):
    """
    Model representing a user profile data structure.
    """

    id: str
    email: str
    username: str
    role: UserRole


class UpdateUserProfileResponse(BaseModel):
    """
    Confirms the updates made to the user's profile, returning the updated data.
    """

    success: bool
    updatedUser: User


async def update_user_profile(
    id: str, email: Optional[str], username: Optional[str], role: UserRole
) -> UpdateUserProfileResponse:
    """
    Updates an existing user's profile in the database.

    Args:
        id (str): The unique identifier of the user being updated.
        email (Optional[str]): The new email address of the user, None if not updating.
        username (Optional[str]): The new username for the user, None if not updating.
        role (UserRole): The new role assigned to the user, determining access levels.

    Returns:
        UpdateUserProfileResponse: Confirms the updates made to the user's profile, returning the updated data.
    """
    update_data = {}
    if email is not None:
        update_data["email"] = email
    if username is not None:
        update_data["username"] = username
    if role:
        update_data["role"] = role
    updated_user = await prisma.models.User.prisma().update(
        where={"id": id}, data=update_data
    )
    return UpdateUserProfileResponse(success=True, updatedUser=updated_user)
