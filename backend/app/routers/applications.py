from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import ApplicationRead, StatusUpdate
from .. import services


router = APIRouter(prefix="/api/applications", tags=["applications"])


@router.patch("/{application_id}/status", response_model=ApplicationRead)
def update_application_status(
    application_id: int,
    payload: StatusUpdate,
    db: Session = Depends(get_db),
):
    return services.update_status(db, application_id, payload)
