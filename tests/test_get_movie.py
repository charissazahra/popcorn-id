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
        "cover": "inception.jpg",
    }

    response = client.post(
        "/movies/", json=payload
    )  # Kirim request POST ke /movies/ kayak dari Swagger/Postman

    assert response.status_code == 200  # Pastikan responnya sukses (kode 200)
    result = response.json()

    # Validasi isi respons sesuai dgn payload
    assert (
        result["title"] == "Inception"
    )  # Cek apakah data yang dikembalikan sesuai dengan input yang kita kirim
    assert result["description"] == "Mind-bending thriller"
    assert result["duration"] == 148
    assert result["rating"] == 8.8
    assert result["cover"] == "inception.jpg"
    assert "id" in result  # Pastikan ID otomatis dimasukkan oleh server

    # Gunakan ID dari POST (menyimpan ID dari data yang baru saja di-post, jadi pastiin data benar-benar ada)
    movie_id = result["id"]

    # GET movie berdasarkan ID
    response = client.get(
        f"/movies/{movie_id}"
    )  # Kirim request GET ke /movies/{parameter}
    assert response.status_code == 200  # Pastikan responnya sukses (kode 200)
    get_result = response.json()

    # Validasi data hasil GET
    assert get_result == result

    # GET movie dengan invalid id (cocok digunakan untuk test data yang hilang.)
    response = client.get(f"/movies/9999")
    assert response.status_code == 404  # (kode 404 not found)

    # GET movie dengan Negative ID
    response = client.get(f"/movies/-1")
    assert response.status_code in [
        404,
        422,
    ]  # (kode 404 atau 422 not found or rejected)

    # GET movie dengan Non-Integer ID
    response = client.get(f"/movies/abc")
    assert (
        response.status_code == 422
    )  # (kode 422 Unprocessable Entity, id hrs integer)
