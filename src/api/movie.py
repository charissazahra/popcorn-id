from fastapi import APIRouter

from src.models.movie import Movie

router = APIRouter()

@router.post("/movies/", response_model=Movie)
def add_movie(movie: Movie):
	print(f"movie title: {movie.title}") #nge-cetak atribut dari object movie
	print(f"movie id: {movie.id}")
	print(f"movie description: {movie.description}")
	print(f"movie duration: {movie.duration}")
	print(f"movie rating: {movie.rating}")
	print(f"movie cover: {movie.cover}")
	return movie
	