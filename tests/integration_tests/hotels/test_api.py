from fastapi import status

async def test_get_hotels(auth_ac):
    result = await auth_ac.get(
        '/hotels',
        params={
            'date_from': '20.11.2024',
            'date_to': '23.11.2024'
        }
    )
    assert result.status_code == status.HTTP_200_OK
