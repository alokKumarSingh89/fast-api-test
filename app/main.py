from http import HTTPStatus
import time
from typing import List

from fastapi import Depends, FastAPI, APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from app import crud
from app.api import deps
from app.api.api_v1.api import api_router
from app.core.config import settings

BASE_PATH = Path(__file__).resolve().parent
TEMPLATE = Jinja2Templates(directory=str(BASE_PATH/"templates"))

app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)


root_router = APIRouter()


@root_router.get("/", status_code=200)
def root(req: Request, db: Session = Depends(deps.get_db)) -> dict:
    """
    Root Get
    """
    recipes = crud.recipe.get_multi(db=db)
    return TEMPLATE.TemplateResponse("index.html", {"request": req, "recipes": recipes})


@app.middleware("http")
async def add_process_time(req: Request, call_next):
    start_time = time.time()
    res = await call_next(req)
    process_time = time.time() - start_time
    res.headers["X-Process-Time"] = str(process_time)
    return res

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)
