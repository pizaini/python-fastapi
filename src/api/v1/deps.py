# app/api/v1/deps.py
from typing import Generator
from sqlmodel import Session
from src.db.database import get_session

# Re-export get_session for convenience in endpoints
def get_db_session() -> Generator[Session, None, None]:
    yield from get_session()

# You might add other dependencies here, e.g., for authentication:
# from fastapi import Depends, HTTPException, status
# from src.core.security import verify_token, decode_token
# async def get_current_user(token: str = Depends(oauth2_scheme)): # Assuming oauth2_scheme is defined elsewhere
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = decode_token(token)
#         user_id: str = payload.get("sub")
#         if user_id is None:
#             raise credentials_exception
#         # You'd typically fetch the user from DB here
#         # user = session.get(User, int(user_id))
#         # if user is None:
#         #     raise credentials_exception
#         return {"user_id": user_id} # Or return the actual user object
#     except Exception:
#         raise credentials_exception