from datetime import datetime, timedelta
import os

import prisma
import prisma.models
from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext
from pydantic import BaseModel


class LoginUserResponse(BaseModel):
    """
    Contains the authentication token on successful login.
    """

    token: str
    user_id: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret_key")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 30


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against the hashed version.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hash of the password.

    Returns:
        bool: Whether the password matches the hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    """
    Create a new access token.

    Args:
        data (dict): The payload to include in the token.
        expires_delta (timedelta | None): The lifetime of the token. Defaults to None.

    Returns:
        str: The generated JWT token as a string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def login_user(email: str, password: str) -> LoginUserResponse:
    """
    Authenticates a user and returns a token.

    Args:
        email (str): The email address of the user trying to log in.
        password (str): The password of the user, to be verified against the stored hash.

    Returns:
        LoginUserResponse: Contains the authentication token on successful login.

    Raises:
        HTTPException: If the user cannot be authenticated.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": email})
    if not user or not await verify_password(password, user.hashedPassword):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    await prisma.models.User.prisma().update(
        where={"id": user.id}, data={"last_login": datetime.utcnow()}
    )
    return LoginUserResponse(token=access_token, user_id=user.id)
