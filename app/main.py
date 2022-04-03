from http import HTTPStatus
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


app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(root_router)
