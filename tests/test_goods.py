from sqlalchemy import insert, select

from conftest import async_session_maker


def test_get_goods(client):
    response = client.get("goods/get_goods")
    assert response.status_code == 200
    assert response.text == '{"status":"ok","detail":"got goods","data":[]}'


def test_add_good_not_seller(client):
    client.post("auth/jwt/login", data={"username":"user@example.com", "password":"string"})
    token = client.cookies.get("auth")
    response = client.post("goods/add_good", json={
    "name": "string",
    "description": "string",
    "price": 0,
    "amount": 0,
    "seller_id": 0
    }, cookies={"auth": token})
    assert response.status_code == 400
    assert response.text == '{"detail":{"status":"error","detail":"you need to be a seller","data":null}}'


def test_become_seller(client):
    token = client.cookies.get("auth")
    response = client.post("goods/become_seller", json={
  "full_name": "Ivanov Ivan Ivanovich",
  "certificate_num": 11111
}, cookies={"auth": token})
    assert response.status_code == 200
  

def test_add_good(client):

    token = client.cookies.get("auth")
    response = client.post("goods/add_good", json={
    "name": "string",
    "description": "string",
    "price": 0,
    "amount": 0,
    "seller_id": 0
    }, cookies={"auth": token})
    assert response.status_code == 200


def test_update_good(client):
    token = client.cookies.get("auth")
    response = client.patch("goods/update_good", params={
    "id": 1,
    "name": "new_string",
    "description": "new_string",
    "price": 1,
    "amount": 1,
    }, cookies={"auth": token})
    assert response.status_code == 200

def test_delete_good(client):
    token = client.cookies.get("auth")
    response = client.delete("goods/delete_good", params={
    "id": 1,
    }, cookies={"auth": token})
    assert response.status_code == 200