def test_register_login_and_access_profile(client):
    # 1. Kayıt ol
    register_res = client.post("/auth/register", json={
        "email": "akis@example.com",
        "password": "sifre123",
        "first_name": "Akis",
        "last_name": "Testi",
        "phone": "5550001122",
    })
    assert register_res.status_code == 200

    # 2. Giriş yap, token al
    login_res = client.post("/auth/login", json={
        "email": "akis@example.com",
        "password": "sifre123",
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # 3. Token ile korumalı endpoint'e eriş (profil)
    headers = {"Authorization": f"Bearer {token}"}
    profile_res = client.get("/auth/me", headers=headers)
    assert profile_res.status_code == 200
    assert profile_res.json()["email"] == "akis@example.com"


def test_access_protected_without_token(client):
    # Token olmadan korumalı endpoint'e erişmeye çalış
    response = client.get("/auth/me")
    assert response.status_code in (401, 403)