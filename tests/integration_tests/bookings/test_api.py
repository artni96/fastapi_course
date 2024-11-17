async def test_get_bookings(auth_ac):
    result = await auth_ac.get(
        '/bookings'
    )
    assert result.status_code == 200
    isinstance(result.json(), list)