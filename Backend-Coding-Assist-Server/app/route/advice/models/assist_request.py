from pydantic import BaseModel


class AssistRequest(BaseModel):
    line: int
    source_code: str
