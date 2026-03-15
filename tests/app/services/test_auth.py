import pytest

async def test_login_ok(async_client, test_user):
    # 1. Arrange: test_user fixture already created in DB

    # 2. Act
    response = await async_client.post(
        "/token", data={"username": test_user.username, "password": "password123"}
    )

    # 3. Assert
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(async_client, test_user):
    # 1. Arrange: test_user exists but we use a wrong password

    # 2. Act
    response = await async_client.post(
        "/token", data={"username": test_user.username, "password": "wrongpassword"}
    )

    # 3. Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


async def test_login_wrong_username(async_client):
    # 1. Arrange: no user created

    # 2. Act
    response = await async_client.post(
        "/token", data={"username": "ghost", "password": "password123"}
    )

    # 3. Assert
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"

async def test_stations_no_token(async_client):
    # 1. Arrange: unauthenticated client

    # 2. Act
    response = await async_client.post("/stations/", params={"station_name": "Central"})

    # 3. Assert: missing token → 401
    assert response.status_code == 401


async def test_stations_non_admin(auth_client):
    # 1. Arrange: logged in as a regular rider

    # 2. Act
    response = await auth_client.post("/stations/", params={"station_name": "Central"})

    # 3. Assert: authenticated but wrong role → 403
    assert response.status_code == 403
    assert response.json()["detail"] == "Not enough permissions"


async def test_stations_as_admin(admin_client, test_admin):
    # 1. Arrange: logged in as admin

    # 2. Act
    response = await admin_client.post("/stations/", params={"station_name": "Central"})

    # 3. Assert
    assert response.status_code == 200
    data = response.json()
    assert "Central" in data["message"]
    assert test_admin.username in data["message"]
