import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def get_test_client():
    from fastapi.testclient import TestClient
    from src.main import app
    return TestClient(app)

def test_add_movie_valid():
    client = get_test_client()
    payload = {
        "title": "Inception",
        "description": "Mind-bending thriller",
        "duration": 148,
        "rating": 8.8,
        "cover": "inception.jpg"
    }

    response = client.post("/movies/", json=payload) #Kirim request POST ke /movies/ kayak dari Swagger/Postman

    assert response.status_code == 200 #Pastikan responnya sukses (kode 200)
    result = response.json()
    assert result["title"] == "Inception" #Cek apakah data yang dikembalikan sesuai dengan input yang kita kirim
    assert result["description"] == "Mind-bending thriller"
    assert result["duration"] == 148
    assert result["rating"] == 8.8
    assert result["cover"] == "inception.jpg"
    assert "id" in result #Pastikan ID otomatis dimasukkan oleh server

def test_add_movie_missing_title():
    client = get_test_client()
    payload = {
        "title": "",
        "description": "Mind-bending thriller3",
        "duration": 148,
        "rating": 8.8,
        "cover": "inception.jpg"
    }

    response = client.post("/movies/", json=payload) #Kirim request POST ke /movies/ kayak dari Swagger/Postman

    assert response.status_code == 422
    result = response.json() 
    print(result)

def test_add_movie_invalid_duration():
    client = get_test_client()
    payload = {
        "title": "Inception1",
        "description": "Mind-bending thriller1",
        "duration": 0,
        "rating": 8.8,
        "cover": "inception.jpg"
    }

    response = client.post("/movies/", json=payload) #Kirim request POST ke /movies/ kayak dari Swagger/Postman

    assert response.status_code == 422
    client = get_test_client()

    payload = {
        "title": "Inception2",
        "description": "Mind-bending thriller2",
        "duration": -1,
        "rating": 8.8,
        "cover": "inception.jpg"
    }

    response = client.post("/movies/", json=payload) #Kirim request POST ke /movies/ kayak dari Swagger/Postman

    assert response.status_code == 422

    # payload = {
    #     "title": "Inception",
    #     "description": "Mind-bending thriller",
    #     "duration": 10.2,
    #     "rating": 8.8,
    #     "cover": "inception.jpg"
    # }

    # response = client.post("/movies/", json=payload) #Kirim request POST ke /movies/ kayak dari Swagger/Postman

    # assert response.status_code == 422




