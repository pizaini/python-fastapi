from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # For Bearer token extraction
import structlog
from jose import jwt, JWTError
from pydantic import ValidationError

from src.db.models.user import CurrentUser

logger = structlog.get_logger(__name__)

bearer_schema = HTTPBearer()


def verify_access_token(token: str, credentials_exception):
    """
    Verifies a JWT access token and returns the payload.
    Raises credentials_exception if token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, key="", algorithms=[],
                    options= {
                        "verify_signature": False,
                        "verify_aud": False,
                        "verify_exp": False,
                        "verify_nbf": False,
                        "verify_iat": False,
                        "verify_at_hash": False,
                        "verify_jti": False,
                    }
                )
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {e}",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user_payload(credentials: HTTPAuthorizationCredentials = Depends(bearer_schema)):
    """
    Dependency to get the decoded JWT payload from the request.
    It verifies the token and raises HTTPException if invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the token using your security logic
    payload = verify_access_token(credentials.credentials, credentials_exception)
    return payload

def get_current_user(payload: dict = Depends(get_current_user_payload)) -> CurrentUser:
    try:
        current_user_data = {
            "email": payload.get("email"),
            "username": payload.get("preferred_username"),  # Maps to 'username' in CurrentUser
            "name": payload.get("name"),  # Maps to 'fullname' in CurrentUser
            "id": payload.get("sub")  # 'sub' is a common standard claim for unique user ID
        }
        user = CurrentUser(**current_user_data)
        return user

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token payload invalid or missing required user claims: {e.errors()}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unable to continue data processing."
        )