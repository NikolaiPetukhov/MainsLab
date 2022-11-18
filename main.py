from typing import Union

from fastapi import Depends, FastAPI, UploadFile
from sqlalchemy.orm import Session
import pandas as pd

import models
import services
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/bills")
async def upload(file: UploadFile, db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    result = services.save_bills(df, db)
    return {"result": result}


@app.get("/bills")
def read_item(org: Union[str, None] = None, client: Union[str, None] = None, db: Session = Depends(get_db)):
    return services.get_bills_dto(db, org, client)
