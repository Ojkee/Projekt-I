from pydantic import BaseModel

from fastapi import APIRouter
from backend.pkg.api import compile_math_input


# TODO
class RunRequest(BaseModel):
    code: str


class RunResponse(BaseModel):
    steps: list[str]


router = APIRouter()


@router.post("/interpret", response_model=RunResponse)
def interpret(req: RunRequest):
    try:
        result = compile_math_input(req.code)
        return RunResponse(steps=result)
    except Exception as e:
        return RunResponse(steps=[f"Error: {str(e)}"])

