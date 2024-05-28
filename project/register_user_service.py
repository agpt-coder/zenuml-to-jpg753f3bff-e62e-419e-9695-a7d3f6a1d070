import bcrypt
import prisma
import prisma.models
from pydantic import BaseModel


class RegisterUserResponse(BaseModel):
    """
    Response model for a successful user registration. Includes the newly created user id and a message confirming the registration.
    """

    user_id: str
    message: str


async def register_user(
    username: str, email: str, password: str
) -> RegisterUserResponse:
    """
    Registers a new user account.

    Args:
        username (str): The chosen username for the new user account. Must be unique.
        email (str): The user's email address. Must be unique and will be used for account recovery.
        password (str): The password for the new account. It will be hashed before being stored in the database for security.

    Returns:
        RegisterUserResponse: Response model for a successful user registration. Includes the newly created user id and a message confirming the registration.

    This function checks the uniqueness of the username and email, hashes the password, and creates a new user in the database.
    """
    existing_user = await prisma.models.User.prisma().find_unique(
        where={"email": email}
    )
    if existing_user:
        raise Exception("A user with the given email already exists.")
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    new_user = await prisma.models.User.prisma().create(
        data={
            "email": email,
            "hashedPassword": hashed_password.decode("utf-8"),
            "username": username,
        }
    )
    return RegisterUserResponse(
        user_id=new_user.id, message="User successfully registered."
    )
