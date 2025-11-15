from pydantic import BaseModel

from fastapi import APIRouter
from backend.pkg.api import get_implemented_formulas_json


class RunRequest(BaseModel): ...


class RunResponse(BaseModel):
    formulas: dict[str, list[dict[str, str]]]


router = APIRouter()


@router.get("/get_formulas_json", response_model=RunResponse)
def get_formulas_json(req: RunRequest):
    _ = req
    try:
        result = get_implemented_formulas_json()
        return RunResponse(formulas=result)
    except Exception as e:
        return RunResponse(formulas={f"ERROR {e}": []})
