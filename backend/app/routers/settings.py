from fastapi import APIRouter
from pydantic import BaseModel

from app.repositories import settings_repo

router = APIRouter(tags=["settings"])


class SettingsUpdate(BaseModel):
    waste_pct: float | None = None
    max_mode: bool | None = None


@router.get("/settings")
def get_settings():
    return settings_repo.get_all()


@router.put("/settings")
def update_settings(body: SettingsUpdate):
    values = {}
    if body.waste_pct is not None:
        values["waste_pct"] = body.waste_pct
    if body.max_mode is not None:
        values["max_mode"] = "1" if body.max_mode else "0"
    if values:
        return settings_repo.set_values(values)
    return settings_repo.get_all()
