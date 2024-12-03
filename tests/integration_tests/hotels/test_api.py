from fastapi import status
from datetime import date, timedelta


async def test_get_hotels(auth_ac):
    result = await auth_ac.get(
        "/hotels", params={"date_from": f"{date.today()}", "date_to": f"{date.today() + timedelta(days=4)}"}
    )
    assert result.status_code == status.HTTP_200_OK
