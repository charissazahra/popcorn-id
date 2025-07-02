from fastapi import APIRouter  
from src.models.movie import Movie, MovieCreate #import object MovieCreate 
import json
from pathlib import Path 
from typing import List

router = APIRouter() 

@router.post("/movies/", response_model=Movie)
def add_movie(movie_create: MovieCreate): #ganti parameter

	#akses data movie_data.json nya
	file_path = Path(__file__).resolve().parent.parent / "data" / "movie_data.json"


	if not file_path.exists():
		raise FileNotFoundError("File movie_data tidak ditemukan. Pastikan sudah dibuat secara manual dulu")

	with open(file_path, "r", encoding="utf-8") as f:
		try:
			data = json.load(f)
		except json.JSONDecodeError:
			data = []

	if not data: #krn data itu list dictionary jdi pke not
		last_id = 0
	else:
		last_id = data[-1]["id"] #dapetin last data pada list, tapi kita cuma dapetin id nya aja dari dict

	new_id = last_id + 1

	movie = Movie(
		id=new_id,
		title= movie_create.title,
		description=movie_create.description,
		duration=movie_create.duration,
		rating=movie_create.rating,
		cover=movie_create.cover
	)

	movie_dict = movie.dict()
		
	data.append(movie_dict) #ini tuh insert data movie nya

	with open(file_path, "w", encoding="utf-8") as f: #ini saving 
		try:
			json.dump(data, f, indent=4)
		except Exception as e:
			print(e)

	return movie

@router.get("/movies/latest", response_model=List[Movie]) #agar fastAPI tau klo mau return list of movie, bukan 1 aja
def get_movie_latest(): #tidak butuh parameter krn hnya membaca data dan mengambil 10 terakhir

	#akses data movie_data.json nya
	file_path = Path(__file__).resolve().parent.parent / "data" / "movie_data.json"

	if not file_path.exists():
		raise FileNotFoundError("File movie_data tidak ditemukan. Pastikan sudah dibuat secara manual dulu")

	#baca file
	with open(file_path, "r", encoding="utf-8") as f:
		try:
			data = json.load(f)
		except json.JSONDecodeError:
			data = []

	#Urutkan berdasarkan 'id' secara descending (terbesar ke terkecil)
	data_sorted = sorted(data, key=lambda x: x["id"], reverse=True)

	# Ambil 10 data pertama (karena sudah descending), lalu buang yang title-nya kosong
	latest_movie = [m for m in data_sorted if m.get("title", "").strip()][:10]
	return latest_movie
	
@router.get("/movies/id/{id}", response_model=Movie)
def get_movie(movie_id : int): #ganti parameter

	#akses data movie_data.json nya
	file_path = Path(__file__).resolve().parent.parent / "data" / "movie_data.json"

	if not file_path.exists():
		raise FileNotFoundError("File movie_data tidak ditemukan. Pastikan sudah dibuat secara manual dulu")

	with open(file_path, "r", encoding="utf-8") as f:
		try:
			data = json.load(f)
		except json.JSONDecodeError:
			data = []

	for movie in data: #looping movie di dalam list of dict
		if movie["id"] == movie_id: #dari id yg ada list of dict dan berdasarkan id yg diminta
			return movie

 #klo loop selesai dan gak ada yg cocok
	raise HTTPException(status_code=404, detail="Movie not found")

