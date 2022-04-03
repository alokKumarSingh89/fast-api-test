from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Any, Optional

from app import crud
from app.api import deps

from app.schemas.recipe import Recipe, RecipeCreate, RecipeSearchResults

router = APIRouter()


@router.get("/", status_code=200)
def all(*, db: Session = Depends(deps.get_db)):
    return crud.recipe.get_multi(db=db)


@router.get("/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int, db: Session = Depends(deps.get_db)):
    """
     Fetch a single recipe by ID
     """
    result = crud.recipe.get(db, id=recipe_id)
    if not result:
        raise HTTPException(
            status_code=400, detail=f"Recipe with ID {recipe_id} not found")
    return result


@router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipe(*,
                  keyword: Optional[str] = Query(
                      None, min_length=3, example="chicken"),
                  max_result: Optional[int] = 10,
                  db: Session = Depends(deps.get_db)):
    """
     Search for recipes based on label keyword
     """
    recipes = crud.recipe.get_multi(db=db, limit=max_result)
    if not keyword:
        return {"result": recipes}

    results = filter(lambda recipe: keyword.lower()
                     in recipe.label.lower(), recipes)
    return {"result": list(results)[:max_result]}


@router.post("/", status_code=201, response_model=Recipe)
def create_recipe(
    *, recipe_in: RecipeCreate, db: Session = Depends(deps.get_db)
) -> dict:
    """
    Create a new recipe in the database.
    """
    recipe = crud.recipe.create(db=db, obj_in=recipe_in)

    return recipe
