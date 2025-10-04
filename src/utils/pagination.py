# app/utils/pagination.py

from math import ceil
from typing import List, TypeVar, Generic, Optional, Type

# Assuming your PaginatedResponse model is defined here:
from src.db.models.pagination import PaginatedResponse
from pydantic import BaseModel  # Used for TypeVar 'R'

# Define TypeVars for flexibility
R = TypeVar("R", bound=BaseModel)  # R will be the Pydantic ReadModel (e.g., GraduationRead)
D = TypeVar("D")  # D will be the raw database model (e.g., Graduation)


def create_paginated_response(
        raw_data_list: List[D],
        total_count: int,
        offset: int,
        limit: int,
        ReadModel: Type[R]  # Pass the Pydantic ReadModel class itself (e.g., GraduationRead)
) -> PaginatedResponse[R]:
    """
    Generates a PaginatedResponse object with calculated pagination metadata.

    Args:
        raw_data_list (List[D]): A list of raw database model instances (e.g., Graduation objects)
                                 for the current page.
        total_count (int): The total number of items available across all pages.
        offset (int): The offset (number of items skipped) used for the current query.
        limit (int): The limit (number of items per page) used for the current query.
        ReadModel (Type[R]): The Pydantic model class (e.g., GraduationRead) to which
                             each item in raw_data_list should be converted.

    Returns:
        PaginatedResponse[R]: An instance of the generic PaginatedResponse model
                              containing the paginated data and metadata.
    """

    # Calculate current page number (1-indexed)
    current_page = (offset // limit) + 1 if limit > 0 else 1

    # Calculate last page number
    # If total_count is 0, last_page is 0. If total_count > 0 but limit is 0,
    # it implies a single page. If both > 0, calculate ceil.
    last_page = ceil(total_count / limit) if limit > 0 and total_count > 0 else (1 if total_count > 0 else 0)

    # Calculate 'from' and 'to' item numbers for the current page (1-indexed)
    from_item = offset + 1 if total_count > 0 else None
    to_item = min(offset + limit, total_count) if total_count > 0 else None

    # Handle edge cases for empty or out-of-bounds requests gracefully
    if not raw_data_list and total_count == 0:
        # If no data and total count is 0, reset pagination values
        current_page = 0  # Or 1, depending on desired behavior for entirely empty dataset
        last_page = 0
        from_item = None
        to_item = None
    elif not raw_data_list and total_count > 0:
        # If no data is returned but total_count > 0 (e.g., offset is too large)
        # We can still provide the correct current_page and last_page,
        # but 'from'/'to' items should be None as there are no items on this page.
        current_page = ceil((offset + 1) / limit) if limit > 0 else 1
        from_item = None
        to_item = None

    # Convert raw database models to their Pydantic ReadModel equivalents
    processed_data = [ReadModel.model_validate(item) for item in raw_data_list]

    return PaginatedResponse[ReadModel](
        data=processed_data,
        total=total_count,
        per_page=limit,
        current_page=current_page,
        last_page=last_page,
        from_item=from_item,
        to_item=to_item
    )