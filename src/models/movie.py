from pydantic import BaseModel, field_validator


class MovieCreate(BaseModel):
    title: str
    description: str
    duration: int
    rating: float
    cover: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title cannot be empty")
        return v

    @field_validator("duration")
    @classmethod
    def duration_must_be_positive(cls, v):
        if not isinstance(v, int):
            raise TypeError("Duration must be an integer")
        if v <= 0:
            raise ValueError("Duration must be positive")
        return v


class Movie(MovieCreate):
    id: int
