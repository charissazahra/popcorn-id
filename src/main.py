from fastapi import FastAPI

from src import api as r

app = FastAPI()

app.include_router(r.movie.router)


@app.get("/")
def root():
    return {"Hello": "World"}
