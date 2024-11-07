from sqlalchemy import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

def create(db: Session, sandwich):
    db_sandwich = models.Sandwich(
        #Create a new instance of Sandwich model with orders.py data
        sandwich_name=sandwich.sandwich_name,
        price=sandwich.price
    )

    #Add sandwich object to database
    db.add(db_sandwich)
    #Commit the changes to the database
    db.commit()
    #Return the sandwich object
    return db_sandwich

def read_all(db: Session):
    #Retrieve sandwich records
    return db.query(models.Sandwich).all()

def read_one(db: Session, sandwich_id: int):
    sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id).first()
    if not sandwich:
        raise HTTPException(status_code=status.HTTp_404_NOT_FOUND, detail="Sandwich not found.")
    return sandwich

def update(db: Session, sandwich_id: int, sandwich):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if not db_sandwich.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found.")
    update_data = sandwich.model_dump(exclude_unset=True)
    db_sandwich.update(update_data, synchronize_session=False)
    db.commit()
    return db_sandwich.first()

def delete(db: Session, sandwich_id: int):
    db_sandwich = db.query(models.Sandwich).filter(models.Sandwich.id == sandwich_id)
    if not db_sandwich.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found.")
    db_sandwich.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)