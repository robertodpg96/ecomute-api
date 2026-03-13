import pytest
from src.app.routers import bike
from src.app.models.bikes import BikeCreate, BikeResponse
from src.app.data.models import Bike

@pytest.mark.asyncio
async def test_get_bikes(async_client, test_db_session):
    # Bonus: inject a bike into the DB so the API returns 1 bike
    bike = Bike(model="TestBike", battery=80, status="available")
    test_db_session.add(bike)
    await test_db_session.commit()

    response = await async_client.get("/bikes/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["model"] == "TestBike"

@pytest.mark.asyncio
async def insert_bike(async_client, bike_data: dict) -> dict:
    response = await async_client.post("/bikes/", json=bike_data)
    assert response.status_code == 201
    return response.json()

@pytest.mark.asyncio
async def test_read_bike(async_client, test_db_session):
    # 1. Arrange: Insert a bike into the database
    new_bike = Bike(model="TestBike", battery=80, status="available")
    test_db_session.add(new_bike)
    await test_db_session.commit()

    # 2. Act: Call the API to read the bike
    response = await async_client.get(f"/bikes/{new_bike.id}")

    # 3. Assert: Check the response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == new_bike.id

@pytest.mark.asyncio
async def test_no_bike(async_client, test_db_session):
    # 1. Arrange: Insert a bike into the database
    id = 1

    # 2. Act: Call the API to read the bike
    response = await async_client.get(f"/bikes/{id}")

    # 3. Assert: Check the response
    assert response.status_code == 404
    assert response.json()["detail"] == f"Bike with id {id} not found."

@pytest.mark.asyncio
async def test_wrong_bike(async_client, test_db_session):
    # 1. Arrange: Insert a bike into the database
    new_bike = Bike(model="TestBike", battery=80, status="available")
    test_db_session.add(new_bike)
    await test_db_session.commit()

    # 2. Act: Call the API to read the bike
    response = await async_client.get(f"/bikes/{3}")

    # 3. Assert: Check the response
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == f"Bike with id {3} not found."

@pytest.mark.asyncio
async def test_add_bike_ok(async_client, test_db_session):
    # 1. Arrange
    bike = BikeCreate(model="TestBike", battery=80, status="available")
    bikeResponse = BikeResponse(model="TestBike", battery=80, status="available", id=1)
    
    # 2. Act
    response = await async_client.post("/bikes/", json=bike.model_dump())

    # 3. Assert
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_add_bike_wrong_data(async_client, test_db_session):
    # 1. Arrange
    wrong_data = 'wrong data'
    
    # 2. Act
    response = await async_client.post("/bikes/", json=wrong_data)

    # 3. Assert
    assert response.status_code == 422