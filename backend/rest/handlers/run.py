from pydantic import BaseModel

from fastapi import APIRouter
from backend.pkg.api import run_code

# TODO
class RunRequest(BaseModel):
    code: str

class RunResponse(BaseModel):
    steps: list[str]
    final: str

router = APIRouter()

@router.post("/interpret", response_model=RunResponse)
def interpret(req: RunRequest):
    try:
        result = run_code(req.code)
        return RunResponse(steps=result[:-1], final=result[-1])
    except Exception as e:
        return RunResponse(steps=[f"Error: {str(e)}"], final="")