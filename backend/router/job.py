from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.dependencies import (
    get_db,
)  # Asegúrate de tener una función get_db que gestiona la sesión de SQLAlchemy
from controllers.job import update_job_postings

router_job = APIRouter()


@router_job.post("/jobs/", status_code=status.HTTP_201_CREATED)
def update_jobs(db: Session = Depends(get_db)):
    url = "https://jobicy.com/api/v2/remote-jobs?count=20&tag=business%20intelligence&count=1"
    success = update_job_postings(db, url)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se pudo obtener datos de la API",
        )
    return {"message": "Jobs updated successfully!"}
