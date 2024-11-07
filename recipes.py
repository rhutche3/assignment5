from sqlalchemy.orm import Session
from fastapi import HTTPException, status, responses
from ..models import models, schemas

def create(db: Session, recipe):
    db_recipe = models.Recipe(
        sandwich_id=recipe.sandwich_id,
        resource_id=recipe.resource_id,
        amount=recipe.amount
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def read_all(db: Session):
    return db.query(models.Recipe).all()

def read_one(db: Session, recipe_id: int):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="Recipe not found.")
    return recipe

def update(db: Session, recipe_id: int, recipe):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if not db_recipe.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found.")
    update_data = recipe.model_dump(exclude_unset=True)
    db_recipe.update(update_data, synchronize_session=False)
    db.commit()
    return db_recipe.first()

def delete(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id)
    if not db_recipe.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    db_recipe.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)