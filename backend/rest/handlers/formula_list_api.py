from pydantic import BaseModel

from fastapi import APIRouter
from backend.pkg.api import get_implemented_formulas_json


# TODO
class RunRequest(BaseModel): ...


class RunResponse(BaseModel):
    formulas: bytes


router = APIRouter()


@router.post("/get_formulas_json", response_model=RunResponse)
def get_formulas_json(req: RunRequest):
    _ = req
    try:
        result = get_implemented_formulas_json()
        return RunResponse(formulas=result)
    except Exception as e:
        return RunResponse(formulas=f"ERROR {e}".encode("utf-8"))
