# app/services/student_service.py

from typing import List, Optional, Dict, Any
from uuid import UUID
from sqlmodel import Session, select
from src.db.models.student import Student, StudentCreate, StudentRead, StudentUpdate
import structlog

logger = structlog.get_logger(__name__)

class StudentService:
    """
    Service class to encapsulate student-related business logic and database operations.
    """
    def __init__(self, session: Session):
        self.session = session

    def create_student(self, student_create: StudentCreate) -> StudentRead:
        try:
            db_student = Student.model_validate(student_create)
            self.session.add(db_student)
            self.session.commit()
            self.session.refresh(db_student)
            return StudentRead.model_validate(db_student)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"An unexpected error occurred: {e}")

    def get_all_students(self, offset: int = 0, limit: int = 100) -> List[StudentRead]:
        students = self.session.exec(
            select(Student)
            .offset(offset)
            .limit(limit)
        ).all()
        return [StudentRead.model_validate(student) for student in students]

    def get_student_by_id(self, student_id: str) -> Optional[StudentRead]:

        student = self.session.exec(
            select(Student)
            .where(Student.student_id == student_id)
        ).first()
        if student:
            return StudentRead.model_validate(student)
        return None


    def get_student_by_email(self, email: str) -> Optional[StudentRead]:
        student = self.session.exec(
            select(Student)
            .where(Student.email == email)
        ).first()

        if student:
            return StudentRead.model_validate(student)
        return None

    def get_student_by_email_and_id(self, email: str, student_id) -> Optional[StudentRead]:
        student = self.session.exec(
            select(Student)
            .where(Student.email == email)
            .where(Student.student_id == student_id)
        ).first()

        if student:
            return StudentRead.model_validate(student)
        return None

    def update_student(self, student_id: UUID, student_update: StudentUpdate) -> Optional[StudentRead]:
        """Updates an existing student record by their UUID."""
        logger.info(f"Attempting to update student with ID: {student_id}", student_uuid=student_id, update_data=student_update.model_dump(exclude_unset=True))
        db_student = self.session.get(Student, student_id)
        if not db_student:
            logger.warning("Student not found for update", student_uuid=student_id)
            return None

        # Apply updates from the Pydantic model
        update_data = student_update.model_dump(exclude_unset=True) # Only get fields that were actually set
        for key, value in update_data.items():
            setattr(db_student, key, value)

        self.session.add(db_student)
        self.session.commit()
        self.session.refresh(db_student)
        logger.info("Student updated successfully", student_uuid=db_student.id)
        return StudentRead.model_validate(db_student)

    def delete_student(self, student_id: UUID) -> bool:
        """Deletes a student record by their UUID."""
        logger.info(f"Attempting to delete student with ID: {student_id}", student_uuid=student_id)
        student = self.session.get(Student, student_id)
        if not student:
            logger.warning("Student not found for deletion", student_uuid=student_id)
            return False

        self.session.delete(student)
        self.session.commit()
        logger.info("Student deleted successfully", student_uuid=student_id)
        return True