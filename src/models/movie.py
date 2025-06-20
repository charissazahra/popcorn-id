from pydantic import BaseModel, validator

class MovieCreate(BaseModel): 
	title: str
	description: str
	duration: int
	rating: float
	cover: str

	@validator("title")
	def title_must_not_be_empty(cls, v):
	    if not v.strip():
	        raise ValueError("Title cannot be empty")
	    return v

	@validator("duration")
	def duration_must_be_positive(cls, v):
		if not isinstance(v, int):
			raise TypeError("Duration must be an integer")
		if v <= 0:
			raise ValueError("Duration must be positive")

class Movie(MovieCreate):
	id: int
