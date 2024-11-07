from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.clients.schema import (
    PredictionInput, PredictionOutput,
    ClientCreate, ClientUpdate, ClientOut
)
from app.database import get_db
from app.clients.service.logic import interpret_and_calculate
from app.clients import models

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/predictions", response_model=PredictionOutput)
async def predict(data: PredictionInput):
    """
    Accepts client data and returns prediction results.
    """
    try:
        # Perform prediction using the provided data
        result = interpret_and_calculate(data.model_dump())
        return result
    except Exception as e:
        # Handle exceptions and return an appropriate HTTP error
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=ClientOut)
def get_client(id: int, db: Session = Depends(get_db)):
    """
    Retrieves client information by ID.
    """
    client = db.query(models.Client).filter(models.Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{id}", response_model=ClientOut)
def update_client(id: int, client_update: ClientUpdate, db: Session = Depends(get_db)):
    """
    Updates client information by ID.
    """
    client = db.query(models.Client).filter(models.Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    # Update client fields with the provided data
    for key, value in client_update.model_dump(exclude_unset=True).items():
        setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(id: int, db: Session = Depends(get_db)):
    """
    Deletes client data by ID.
    """
    client = db.query(models.Client).filter(models.Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(client)
    db.commit()
    return
