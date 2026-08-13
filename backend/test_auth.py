def test_register(client):
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "sifre123",
        "first_name": "Test",
        "last_name": "Kullanici",
        "phone": "5551112233",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["first_name"] == "Test"
    assert "id" in data


def test_login(client):
    # Önce kayıt ol
    client.post("/auth/register", json={
        "email": "login@example.com",
        "password": "sifre123",
        "first_name": "Login",
        "last_name": "Test",
        "phone": "5559998877",
    })
    # Sonra giriş yap
    response = client.post("/auth/login", json={
        "email": "login@example.com",
        "password": "sifre123",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    # Kayıt ol
    client.post("/auth/register", json={
        "email": "wrong@example.com",
        "password": "dogrusifre",
        "first_name": "Wrong",
        "last_name": "Pass",
        "phone": "5551234567",
    })
    # Yanlış şifreyle giriş dene
    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "yanlissifre",
    })
    assert response.status_code == 401