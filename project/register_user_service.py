import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class UserRole(BaseModel):
    """
    An ENUM defining possible user roles within the system, including 'User', 'Admin', 'Premium'.
    """

    pass


class UserRegistrationResponse(BaseModel):
    """
    The response model conveying the basic information of a newly registered user.
    """

    user_id: str
    email: str
    role: str


async def register_user(
    email: str, password: str, role: UserRole
) -> UserRegistrationResponse:
    """
    Registers a new user and returns basic user information

    Args:
        email (str): The email address of the new user. It will be used as the unique identifier for login purposes.
        password (str): The password for the new user. This will be hashed before storage for security reasons.
        role (UserRole): The role assigned to the new user (e.g., 'User', 'Admin', 'Premium'). Defaults to 'User' if not specified.

    Returns:
        UserRegistrationResponse: The response model conveying the basic information of a newly registered user.

    Raises:
        ValidationError: If the email is already taken or the role is not valid.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        raise ValueError("Email already in use")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    new_user = await prisma.models.User.prisma().create(
        data={"email": email, "password": hashed_password, "role": role}
    )
    return UserRegistrationResponse(
        user_id=new_user.id, email=new_user.email, role=new_user.role
    )
