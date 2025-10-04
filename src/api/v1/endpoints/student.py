from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from src.db.database import get_session # Your dependency for getting a DB session
from src.db.models.student import StudentCreate, StudentRead, StudentUpdate
from src.services.student_service import StudentService # Import your new service
import structlog

router = APIRouter()
logger = structlog.get_logger(__name__)

# Dependency that provides an instance of StudentService
def get_student_service(session: Session = Depends(get_session)) -> StudentService:
    """Provides a StudentService instance with an injected database session."""
    return StudentService(session)

@router.post("/student/", response_model=StudentRead, status_code=status.HTTP_201_CREATED, summary="Create a new student")
def create_student(
    student_create: StudentCreate,
    student_service: StudentService = Depends(get_student_service)
):
    try:
        new_student = student_service.create_student(student_create)
        return new_student
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Duplicate student: {e}',
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating student: {e}"
        )

@router.get("/student/", response_model=List[StudentRead], summary="Get a list of students")
def read_students(
    student_service: StudentService = Depends(get_student_service),
    offset: int = 0,
    limit: int = 100
):
    students = student_service.get_all_students(offset=offset, limit=limit)
    return students

@router.get("/student/{student_id}", response_model=StudentRead, summary="Get a single student by ID")
def get_student(
    student_id: UUID, # FastAPI automatically converts path parameter to UUID
    student_service: StudentService = Depends(get_student_service)
):
    """
    Retrieve a single student by their unique ID.
    """
    logger.info("API call: get_student", student_uuid=student_id)
    student = student_service.get_student_by_id(student_id)
    if not student:
        logger.warning("Student not found", student_uuid=student_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.put("/student/{student_id}", response_model=StudentRead, summary="Update an existing student")
def update_student(
    student_id: UUID,
    student_update: StudentUpdate,
    student_service: StudentService = Depends(get_student_service)
):
    """
    Update an existing student's information.
    """
    logger.info("API call: update_student", student_uuid=student_id, update_data=student_update.model_dump(exclude_unset=True))
    updated_student = student_service.update_student(student_id, student_update)
    if not updated_student:
        logger.warning("Student not found for update", student_uuid=student_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return updated_student

@router.delete("/student/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a student")
def delete_student(
    student_id: UUID,
    student_service: StudentService = Depends(get_student_service)
):
    """
    Delete a student by their unique ID.
    """
    logger.info("API call: delete_student", student_uuid=student_id)
    if not student_service.delete_student(student_id):
        logger.warning("Student not found for deletion", student_uuid=student_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    # No content to return for 204 No Content
    return Response(status_code=status.HTTP_204_NO_CONTENT)