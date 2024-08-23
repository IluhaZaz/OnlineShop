from sqlalchemy import insert, select, update

from auth.models import role, user
from conftest import client, async_session_maker


async def test_add_roles():
    async with async_session_maker() as session:
        roles = [(1, "customer", None), (2, "seller", {"sell": True})]
        stmt = insert(role).values(roles)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, "customer", None), (2, "seller", {"sell": True})], "Role did not add"


def test_register(client):
    response = client.post("/auth/register", json={
        "email": "user@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "name": "string",
        "role_id": 0
    })

    assert response.status_code == 201


def test_auth(client):
    response = client.post("auth/jwt/login", data={"username":"user@example.com", "password":"string"})
    assert response.status_code == 204


async def test_make_verified():
    """Used to check goods tests"""
    async with async_session_maker() as session:
        stmt = update(user).values(is_verified=True)
        await session.execute(stmt)
        await session.commit()