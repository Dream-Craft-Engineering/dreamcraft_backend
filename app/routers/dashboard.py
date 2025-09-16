from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..deps import get_db, get_current_admin

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats", response_model=schemas.DashboardStats)
def get_stats_for_dashboard(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_admin)
):
    """
    Retrieve aggregated statistics for the admin dashboard.
    Requires admin privileges.
    """
    return crud.get_dashboard_stats(db=db)