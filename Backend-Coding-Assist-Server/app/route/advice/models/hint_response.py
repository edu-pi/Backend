from pydantic import BaseModel


class HintResponse(BaseModel):
    line: int
    hint: str

    @classmethod
    async def of(cls, response_data: dict):
        return HintResponse(
            line=response_data.get("line", 0),
            hint=response_data.get("hint", "틀린 원인을 찾을 수 없습니다.")
        )
