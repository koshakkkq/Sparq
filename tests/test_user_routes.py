import pytest

from sqlalchemy.future import select

from app.models.test_model import User


@pytest.mark.asyncio()
async def test_create_user(test_client, db_session):
    res = await test_client.post(
        "auth/register",
        json={
            "username": "TestUser",
            "email": "TestUser@mail.ru",
            "password": "SomePassword",
        },
    )
    assert res.json()["message"] == "User created successfully"

    select_all = select(User)
    rows = await db_session.execute(select_all)
    rows = list(rows.scalars())
    assert len(rows) == 1
    new_user = rows[0]
    assert new_user.username == "TestUser"
    assert new_user.email == "TestUser@mail.ru"
