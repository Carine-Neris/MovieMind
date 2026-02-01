from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database, models, schemas
from app.services.rating_service import RatingService

router = APIRouter()

def get_db():
    db = next(database.get_db())
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.AvaliacaoOut, status_code=status.HTTP_201_CREATED)
def criar_avaliacao(avaliacao: schemas.AvaliacaoCreate, db: Session = Depends(database.get_db)):
    return RatingService.create_rating(db, avaliacao)

@router.get("/", response_model=List[schemas.AvaliacaoOut])
def listar_avaliacoes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return RatingService.list_ratings(db, skip, limit)

@router.get("/{avaliacao_id}", response_model=schemas.AvaliacaoOut)
def obter_avaliacao(avaliacao_id: UUID, db: Session = Depends(database.get_db)):
    return RatingService.get_rating(db, avaliacao_id)

@router.put("/{avaliacao_id}", response_model=schemas.AvaliacaoOut)
def atualizar_avaliacao(avaliacao_id: UUID, avaliacao_update: schemas.AvaliacaoUpdate, db: Session = Depends(database.get_db)):
    return RatingService.update_rating(db, avaliacao_id, avaliacao_update)

@router.delete("/{avaliacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_avaliacao(avaliacao_id: UUID, db: Session = Depends(database.get_db)):
    RatingService.delete_rating(db, avaliacao_id)
    return None
