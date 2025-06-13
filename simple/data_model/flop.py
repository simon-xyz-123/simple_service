from pydantic import BaseModel


class FlopRequest(BaseModel):
    data: dict