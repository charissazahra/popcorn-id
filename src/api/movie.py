from fastapi import APIRouter  
from src.models.movie import Movie
import json
from pathlib import Path 

router = APIRouter() 

@router.post("/movies/", response_model=Movie)
def add_movie(movie: Movie):
	movie_dict = movie.dict()

	print(movie_dict)
	file_path = Path(__file__).resolve().parent.parent / "data" / "movie_data.json"


	if not file_path.exists():
		raise FileNotFoundError("File movie_data tidak ditemukan. Pastikan sudah dibuat secara manual dulu")

	with open(file_path, "r", encoding="utf-8") as f:
		try:
			data = json.load(f)
		except json.JSONDecodeError:
			data = []

	data.append(movie_dict)

	with open(file_path, "w", encoding="utf-8") as f:
		try:
			json.dump(data, f, indent=4)
		except Exception as e:
			print(e)


	return movie

