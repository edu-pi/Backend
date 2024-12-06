from pydantic import BaseModel


class CodeRequest(BaseModel):
    source_code: str
    input: str = ""
    