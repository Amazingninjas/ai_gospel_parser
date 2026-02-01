"""
Authentication API Router
=========================
REST API endpoints for user authentication and registration.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import (
    UserRegister, UserLogin, Token, UserResponse, TokenData,
    ForgotPasswordRequest, ResetPasswordRequest
)
from schemas.verse import ErrorResponse
from services.auth_service import AuthService
from services.email_service import send_password_reset_email
from models.user import User



router = APIRouter()

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token.

    Args:
        token: JWT token from Authorization header
        db: Database session

    Returns:
        Current user object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode token
    payload = AuthService.decode_access_token(token)
    if payload is None:
        raise credentials_exception

    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception

    # Get user from database
    user = AuthService.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Email already registered"}
    },
    summary="Register a new user",
    description="""
    Register a new user account with email and password.

    Returns a JWT token that can be used immediately for authentication.
    """
)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.

    Args:
        user_data: Registration data (email, password, full_name)
        db: Database session

    Returns:
        JWT access token
    """
    # Check if user already exists
    existing_user = AuthService.get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user = AuthService.create_user(
        db,
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )

    # Create access token
    access_token = AuthService.create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/login",
    response_model=Token,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid credentials"}
    },
    summary="Login with email and password",
    description="""
    Authenticate with email and password to receive a JWT token.

    The token should be included in subsequent requests as:
    `Authorization: Bearer <token>`
    """
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Login with email and password.

    Args:
        form_data: OAuth2 form with username (email) and password
        db: Database session

    Returns:
        JWT access token
    """
    # Authenticate user (OAuth2 uses 'username' field for email)
    user = AuthService.authenticate_user(db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = AuthService.create_access_token(data={"sub": user.email})

    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="""
    Get information about the currently authenticated user.

    Requires valid JWT token in Authorization header.
    """
)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user.

    Args:
        current_user: Current user from JWT token

    Returns:
        User information (without password)
    """
    return current_user


@router.post(
    "/logout",
    summary="Logout (client-side only)",
    description="""
    Logout endpoint for consistency.

    Note: JWT tokens are stateless, so logout is handled client-side
    by deleting the token from storage. This endpoint just returns a
    success message.
    """
)
async def logout():
    """
    Logout user (client-side token deletion).

    Returns:
        Success message
    """
    return {"message": "Successfully logged out. Delete token from client storage."}


@router.post(
    "/forgot-password",
    status_code=status.HTTP_200_OK,
    summary="Request a password reset",
    description="""
    Initiate the password reset process for a user.

    This endpoint will send a password reset link to the user's email address
    if the account exists. To prevent user enumeration, it will always return
    a success response, even if the email is not found in the database.
    """
)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Request a password reset link.

    Args:
        request: Request containing the user's email
        db: Database session
    """
    token = AuthService.create_password_reset_token(db, email=request.email)

    if token:
        # This function handles the logic for sending email or logging to console
        send_password_reset_email(email=request.email, token=token)

    # Always return a success message to prevent user enumeration
    return {"message": "If an account with that email exists, a password reset link has been sent."}


@router.post(
    "/reset-password",
    status_code=status.HTTP_200_OK,
    summary="Reset password with a token",
    description="""
    Reset the user's password using a valid token from the password reset email.
    """
)
async def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    """
    Reset user's password.

    Args:
        request: Request containing the reset token and new password
        db: Database session
    """
    user = AuthService.reset_password(db, token=request.token, new_password=request.new_password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired password reset token."
        )

    return {"message": "Password has been reset successfully."}
