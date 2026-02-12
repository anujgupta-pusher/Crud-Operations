# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from app.main import app
# from app.database import get_db
# from app.model import Base



# DATABASE_URL = "postgresql://postgres:1234@localhost:5432/todo_db"


# engine = create_engine(DATABASE_URL)
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db


# test_app = TestClient(app)

# @pytest.fixture(scope="session", autouse=True)
# def setup_database():
#     Base.metadata.create_all(bind=engine)
#     yield
#     Base.metadata.drop_all(bind=engine)

def test_create_todo(client):
    client.post(
            "/register" ,
            json={
                "username" :"test@example.com" ,
                "password" : "testpassword"

            }
        )
    login = client.post(
            "/login",
            json={
                "username" : "test@example.com" ,
                "password" : "testpassword"

            }
        )
    print(login.status_code)
    print(login.json())

    token = login.json()["access_token"]
    headers = {"Authorization":f"Bearer {token}"}
    response = client.post(
        "/todos",
        json= {"title": "app"},
        headers=headers
        )
    assert response.status_code==200
    assert response.json()["title"] =="app"

    response = client.get(
        "/todos",
        headers= headers
    )
    assert response.status_code ==200


    #     # "/todos",
    # json={"title": "Buy milk", "completed": False}
    # assert response.status_code in (200, 201)
    # data = response.json()
    # assert data["title"] == "Buy milk"

# def test_get_todos_list(client):
    
#     client.post("/todos", json={"title": "buy", "completed": False})
#     response = client.get("/todos")
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert any(todo["title"] == "buy" for todo in data)

