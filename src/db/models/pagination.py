# app/db/models/pagination.py

from pydantic import BaseModel, Field
from typing import List, TypeVar, Generic, Optional
from math import ceil

T = TypeVar("T")  # Define a TypeVar to make the PaginatedResponse generic


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Generic Pydantic model for paginated API responses,
    mimicking Laravel's pagination structure.
    """
    data: List[T] = Field(..., description="The list of items for the current page.")
    total: int = Field(..., description="The total number of items across all pages.")
    per_page: int = Field(..., description="The number of items per page.")
    current_page: int = Field(..., description="The current page number (1-indexed).")
    last_page: int = Field(..., description="The last page number.")

    # Using Field(alias="from") and Field(alias="to") because 'from' and 'to' are Python keywords.
    # We also make them Optional as they might not make sense for empty data sets.
    from_item: Optional[int] = Field(None, alias="from",
                                     description="The starting item number for the current page (1-indexed).")
    to_item: Optional[int] = Field(None, alias="to",
                                   description="The ending item number for the current page (1-indexed).")

    # Optional fields for URLs (can be added if you want to dynamically generate links)
    # first_page_url: Optional[str] = None
    # last_page_url: Optional[str] = None
    # next_page_url: Optional[str] = None
    # prev_page_url: Optional[str] = None
    # path: Optional[str] = None
    # links: Optional[List[dict]] = None # Example: [{"url": "...", "label": "...", "active": true}]

    class Config:
        populate_by_name = True  # Allows setting 'from' and 'to' using their aliases 'from_item' and 'to_item'
        # arbitrary_types_allowed = True # Might be needed for some complex generic setups, usually not for this