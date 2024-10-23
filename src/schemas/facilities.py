from pydantic import BaseModel, ConfigDict


class FacilityBaseRequest(BaseModel):
    title: str


class FacilityResponse(FacilityBaseRequest):
    id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFacilityAddRequest(BaseModel):
    room_id: int
    facility_id: int
