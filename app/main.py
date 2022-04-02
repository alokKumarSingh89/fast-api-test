from http import HTTPStatus
from typing import List

from fastapi import Depends, FastAPI, APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from app.schemas import Recipe, RecipeCreate
from app import deps
from app import crud

BASE_PATH = Path(__file__).resolve().parent
TEMPLATE = Jinja2Templates(directory=str(BASE_PATH/"templates"))

app = FastAPI(
    title="Recipe API", openapi_url="/openapi.json"
)


api_router = APIRouter()


@api_router.get("/", status_code=200)
def root(req: Request, db: Session = Depends(deps.get_db)) -> dict:
    """
    Root Get
    """
    recipes = crud.recipe.get_multi(db=db)
    return TEMPLATE.TemplateResponse("index.html", {"request": req, "recipes": recipes})


@api_router.get("/recipes/", status_code=200)
def all(*, db: Session = Depends(deps.get_db)):
    return crud.recipe.get_multi(db=db)


@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int, db: Session = Depends(deps.get_db)):
    result = crud.recipe.get(db=db, id=recipe_id)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with ID {recipe_id} not found"
        )
    return result


@api_router.post("/recipe/", status_code=HTTPStatus.CREATED, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate, db: Session = Depends(deps.get_db)):
    recipe_entry = crud.recipe.create(db=db, obj_in=recipe_in)
    return recipe_entry


app.include_router(api_router)
