from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import StatsRead
from .. import services


router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/stats", response_model=StatsRead)
def get_stats(db: Session = Depends(get_db)) -> dict:
    return services.get_stats(db)
