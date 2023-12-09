from fastapi import Depends, Request
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.lib.database.dependency import get_db


async def health_check(request: Request, session: Session = Depends(get_db)):
    db_status = session.execute(text("SELECT 1")).scalars().first()
    return {"api_status": "ok", "db_status": "ok" if db_status else "error"}
