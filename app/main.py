from http import HTTPStatus

from fastapi import Depends, FastAPI, APIRouter, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from app.schemas import Recipe, RecipeCreate

RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

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
    recipes = crud.recipe.get_multi(db=db, limit=10)
    return TEMPLATE.TemplateResponse("index.html", {"request": req, "recipes": recipes})


@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int):
    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"Recipe with ID {recipe_id} not found"
        )
    return result[0]


@api_router.post("/recipe/", status_code=HTTPStatus.CREATED, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate):
    new_entry_id = len(RECIPES)+1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url
    )
    RECIPES.append(recipe_entry.dict())
    return recipe_entry


app.include_router(api_router)
