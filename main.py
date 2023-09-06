from fastapi import FastAPI, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from time import sleep
from uuid import uuid4
from random import randint
from models import TaskStatus, TaskStatusEnum, SessionLocal, engine

# Create tables
TaskStatus.__table__.create(bind=engine, checkfirst=True)

app = FastAPI()


# Dependency to get the SQLAlchemy session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def long_running_task(db: Session, job_id: str):
    sleep(10)  # Simulate a long-running operation
    db_task_status = db.query(TaskStatus).filter(TaskStatus.job_id == job_id).first()
    db_task_status.status = TaskStatusEnum.COMPLETED
    db_task_status.result = f"Prompt results are here"
    db.commit()


@app.post("/start-task/")
async def start_task(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    job_id = str(uuid4())
    db_task_status = TaskStatus(job_id=job_id, status=TaskStatusEnum.STARTED)
    db.add(db_task_status)
    db.commit()
    background_tasks.add_task(long_running_task, db, job_id)
    return {
        "job_id": job_id,
        "status": TaskStatusEnum.STARTED,
        "status_url": f"/status/{job_id}",
    }


@app.get("/status/{job_id}/")
async def get_status(job_id: str, db: Session = Depends(get_db)):
    db_task_status = db.query(TaskStatus).filter(TaskStatus.job_id == job_id).first()
    if db_task_status:
        return db_task_status
    else:
        return db_task_status
