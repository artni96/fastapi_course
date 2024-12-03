from src.schemas.facilities import FacilityBaseRequest
from fastapi import status


async def test_facilities_crud(ac):
    facility_data = FacilityBaseRequest(title="Wi-Fi")
    new_facility = await ac.post("/facilities", json=facility_data.model_dump())
    assert new_facility.status_code == status.HTTP_201_CREATED
    get_facility = await ac.get(f'/facilities/{new_facility.json()["id"]}')
    assert get_facility.status_code == status.HTTP_200_OK
    assert new_facility.json()["title"] == get_facility.json()["title"]
