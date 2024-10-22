from pydantic import BaseModel


class FacilityBaseRequest(BaseModel):
    title: str


class FacilityResponse(FacilityBaseRequest):
    id: int


class RoomFacilityAddRequest(BaseModel):
    room_id: int
    facility_id: int
