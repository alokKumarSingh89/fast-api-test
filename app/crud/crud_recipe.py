from app.models.recipe import Recipe
from app.schemas.recipe import RecipeCreate, RecipeUpdate
from .base import CRUDBase


class CRUDRecipe(CRUDBase[Recipe, RecipeCreate, RecipeUpdate]):
    ...


recipe = CRUDRecipe(Recipe)
