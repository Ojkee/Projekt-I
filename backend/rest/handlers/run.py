from pydantic import BaseModel

from dataclasses import dataclass

from fastapi import APIRouter
from backend.pkg.api import run_code

class RunRequest(BaseModel):
    code: str

class RunResponse(BaseModel):
    result: list[str]

router = APIRouter()

@router.post("/interpret", response_model=RunResponse)
def interpret(req: RunRequest):
    try:
        result = run_code(req.code)
        return RunResponse(result=result)
    except Exception as e:
        return RunResponse(result=[f"Error: {str(e)}"])