from pydantic import BaseModel


class FacilityBaseRequest(BaseModel):
    title: str


class FacilityResponse(FacilityBaseRequest):
    id: int
