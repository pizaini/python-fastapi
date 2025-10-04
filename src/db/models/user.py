from pydantic import BaseModel
from typing import Optional

class CurrentUser(BaseModel):
    email: str # Often a required field
    username: str # Often a required field
    name: Optional[str] = None # Optional, as 'name' might not always be present
    id: Optional[str] = None # Common for 'sub' claim, make Optional if not always used