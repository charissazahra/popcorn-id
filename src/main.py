from fastapi import FastAPI

app = FastAPI()
from src import api as r

app.include_router(r.movie.router)

@app.get("/")
def root():
	return {"Hello": "World"}