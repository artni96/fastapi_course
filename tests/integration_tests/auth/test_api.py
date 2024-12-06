import pytest
from fastapi import status


@pytest.mark.parametrize(
    "email, username, password",
    [
        ("test_user_2@ya.ru", "test_user_2", "string"),
    ],
)
async def test_e2e_auth(ac, email, username, password):
    new_user = await ac.post(
        "/users/register",
        json={
            "email": email,
            "password": password,
            "username": username,
            # "first_name": '',
            # "last_name": ''
        },
    )
    assert new_user.status_code == status.HTTP_201_CREATED
    print(new_user.json())
    assert new_user.json()["email"] == email
    assert new_user.json()["username"] == username
    assert "id" in new_user.json()
    assert "password" not in new_user.json()

    get_access_token = await ac.post(
        "/users/login", json={"email": email, "password": password}
    )
    assert get_access_token.status_code == status.HTTP_200_OK
    user_info = await ac.get(
        "/users/me",
        # headers={"Authorization": f"Bearer {access_token}"}
    )
    assert user_info.status_code == status.HTTP_200_OK
    logout = await ac.post(
        "/users/logout",
        # headers={"Authorization": f"Bearer {access_token}"}
    )
    assert logout.status_code == status.HTTP_204_NO_CONTENT
