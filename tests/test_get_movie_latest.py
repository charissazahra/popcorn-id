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

     # Validasi isi respons sesuai dgn payload
    assert result["title"] == "Inception" #Cek apakah data yang dikembalikan sesuai dengan input yang kita kirim
    assert result["description"] == "Mind-bending thriller"
    assert result["duration"] == 148
    assert result["rating"] == 8.8
    assert result["cover"] == "inception.jpg"
    assert "id" in result #Pastikan ID otomatis dimasukkan oleh server

    # Gunakan ID dari POST (menyimpan ID dari data yang baru saja di-post, jadi pastiin data benar-benar ada)
    movie_id = result["id"]

def test_get_movie_latest():
    client = get_test_client()
    response = client.get("/movies/latest") #Kirim request GET ke /movies/latest
    assert response.status_code == 200 #Pastikan responnya sukses (kode 200)
    result = response.json()

    # Pastikan jumlah maksimal 10
    assert isinstance(result, list) #mastiin bahwa result nya itu list of dict
    assert len(result) <= 10

    # Pastikan id urut dari besar ke kecil (descending)
    id_list = [movie["id"] for movie in result]
    assert id_list == sorted(id_list, reverse=True)

     # Pastikan semua title tidak kosong
    for movie in result:
        assert movie["title"].strip() != ""

    #Get movie latest, jika data kurang dari 10, tapi valid
def test_get_movie_latest_less_than_10():
    client = get_test_client()
    response = client.get("/movies/latest")
    assert response.status_code == 200
    result = response.json()

    assert isinstance(result, list)
    assert len(result) <= 5

    id_list = [movie["id"] for movie in result]
    assert id_list == sorted(id_list, reverse=True)

    for movie in result:
        assert movie["title"].strip() != ""

    #Get movie latest, jika file movie_data.json empty
def test_latest_movie_when_empty_file():
    client = get_test_client()
    response = client.get("/movies/latest")
    assert response.status_code == 200
    result = response

    assert isinstance(result, list)
    assert result == [] # Pastikan list kosong dikembalikan

    #Get movie latest, jika file movie_data.json is missing
def test_latest_movie_when_file_missing():
    client = get_test_client()

    # Simulasikan file tidak ada
    file_path = Path(__file__).resolve().parent.parent / "data" / "movie_data.json"
    if file_path.exists():
        os.rename(file_path, file_path.with_suffix(".bak"))  # Rename sementara

    try:
        response = client.get("/movies/latest")
        assert response.status_code == 500
        result = response.json()
        assert result["detail"] == "File movie_data tidak ditemukan. Pastikan sudah dibuat secara manual dulu"
    finally:
        # Restore file agar tidak rusak untuk test lainnya
        if file_path.with_suffix(".bak").exists():
            os.rename(file_path.with_suffix(".bak"), file_path)
