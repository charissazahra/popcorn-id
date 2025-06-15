from pydantic import BaseModel

class Movie(BaseModel): 
	id: int
	title: str
	description: str
	duration: int
	rating: float
	cover: str
