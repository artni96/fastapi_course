import pytest
from fastapi import status


@pytest.mark.parametrize(
    'email, username, password',
    [
        ('test_user_2@ya.ru', 'test_user_2', 'string'),
    ]
)
async def test_e2e_auth(
    ac,
    email,
    username,
    password
):
    new_user = await ac.post(
        '/auth/register',
        json={
            "email": email,
            "password": password,
            "username": username,
        }
    )
    assert new_user.status_code == status.HTTP_201_CREATED
    assert new_user.json()['email'] == email
    assert new_user.json()['username'] == username
    assert 'id' in new_user.json()
    assert 'password' not in new_user.json()

    get_access_token = await ac.post(
        '/auth/jwt/login',
        data={
            "username": email,
            "password": password
        }
    )
    assert get_access_token.status_code == status.HTTP_200_OK
    access_token = get_access_token.json()['access_token']
    user_info = await ac.get(
        '/users/me',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert user_info.status_code == status.HTTP_200_OK
    logout = await ac.post(
        '/auth/jwt/logout',
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert logout.status_code == status.HTTP_204_NO_CONTENT
