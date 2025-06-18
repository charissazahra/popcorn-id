from pydantic import BaseModel

class MovieCreate(BaseModel): 
	title: str
	description: str
	duration: int
	rating: float
	cover: str

class Movie(MovieCreate):
	id: int
