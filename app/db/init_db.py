from app.core.config import settings
from sqlalchemy.orm import Session
import logging
from app import crud, schemas
from app.db import base
from app.recipe_data import RECIPES

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    if settings.FIRST_SUPERUSER:
        user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = schemas.UserCreate(
                first_name="Initial Super User",
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PW,
                is_superuser=True
            )
            user = crud.user.create(db, obj_in=user_in)
        else:
            logger.warning("Skipping creating superuser. User with email "
                           f"{settings.FIRST_SUPERUSER} already exists. ")
        if not user.recipes:
            for recipe in RECIPES:
                recipe_in = schemas.RecipeCreate(
                    label=recipe["label"],
                    source=recipe["source"],
                    url=recipe["url"],
                    submitter_id=user.id,
                )
                crud.recipe.create(db, obj_in=recipe_in)
