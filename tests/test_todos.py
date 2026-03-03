
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

