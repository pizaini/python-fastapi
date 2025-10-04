from datetime import datetime, timezone
from typing import Optional, Dict, Any, List, Required
from uuid import UUID, uuid4

from sqlalchemy import func
from sqlmodel import Field, SQLModel, Column, JSON, Relationship


# StudentBase defines the common fields for Student
class StudentBase(SQLModel):
    name: str = Field(max_length=50, index=True)
    student_id: str = Field(unique=True, index=True)
    id_semester: str
    email: str = Field(unique=True, index=True)
    # department is a JSON field.
    department: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSON))

# Student is the actual database table model
# Note the 'table="student"' argument to explicitly set the table name
class Student(StudentBase, table=True):
    __tablename__ = "student"
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,  # DB column is NOT NULL
        sa_column_kwargs={"server_default": func.now()}  # DB sets default on insert
    )
    created_by: Optional[str] = Field(default=None, nullable=True)
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,  # DB column is NOT NULL
        sa_column_kwargs={"server_default": func.now()}  # DB sets default on insert
    )
    updated_by: Optional[str] = Field(default=None, nullable=True)


# StudentCreate is used for incoming data when creating a new Student record
class StudentCreate(StudentBase):
    pass

# StudentRead is used for outgoing data when reading Student records
class StudentRead(StudentBase):
    id: UUID

# StudentUpdate is used for incoming data when updating an existing Student record
class StudentUpdate(SQLModel):
    name: Optional[str] = Field(default=None, max_length=50, index=True)
    student_id: Optional[str] = Field(default=None, unique=True, index=True)
    id_semester: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None, unique=True, index=True)
    department: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))