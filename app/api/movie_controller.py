from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database, models, schemas
from app.services.movie_service import MovieService

router = APIRouter()


def get_db():
    db = next(database.get_db())
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.FilmeOut, status_code=status.HTTP_201_CREATED)
def criar_filme(filme: schemas.FilmeCreate, db: Session = Depends(database.get_db)):
    return MovieService.create_movie(db, filme)


@router.get("/", response_model=List[schemas.FilmeOut])
def listar_filmes(skip: int = 0, limit: int = 20, db: Session = Depends(database.get_db)):
    return MovieService.list_movies(db, skip=skip, limit=limit)


@router.get("/{filme_id}", response_model=schemas.FilmeOut)
def obter_filme(filme_id: UUID, db: Session = Depends(database.get_db)):
    filme = MovieService.get_movie(db, filme_id)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme


@router.put("/{filme_id}", response_model=schemas.FilmeOut)
def atualizar_filme(filme_id: UUID, filme_update: schemas.FilmeUpdate, db: Session = Depends(database.get_db)):
    filme = MovieService.update_movie(db, filme_id, filme_update)
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return filme


@router.delete("/{filme_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_filme(filme_id: UUID, db: Session = Depends(database.get_db)):
    deleted = MovieService.delete_movie(db, filme_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return None
