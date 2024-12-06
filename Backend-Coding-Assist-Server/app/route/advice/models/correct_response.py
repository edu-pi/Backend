from pydantic import BaseModel


class ModifiedCode(BaseModel):
    line: int
    code: str


class CorrectResponse(BaseModel):
    reason: str
    modified_codes: list[ModifiedCode]

    @classmethod
    async def of(cls, response_data: dict, line: int):
        modified_codes_data = response_data.get("code", "")
        reason = response_data.get("reason", "틀린 원인을 찾을 수 없습니다.")
        return CorrectResponse(reason=reason, modified_codes=[ModifiedCode(line=line, code=modified_codes_data)])
