from typing import List, Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app import models, schemas


class MovieService:
    @staticmethod
    def create_movie(db: Session, filme: schemas.FilmeCreate) -> models.Filme:
        elenco_str = ", ".join(filme.elenco) if filme.elenco else ""
        db_filme = models.Filme(
            titulo=filme.titulo,
            genero=filme.genero,
            duracao=filme.duracao,
            ano=filme.ano,
            diretor=filme.diretor,
            elenco=elenco_str,
            sinopse=filme.sinopse,
        )
        db.add(db_filme)
        db.commit()
        db.refresh(db_filme)
        return db_filme

    @staticmethod
    def get_movie(db: Session, filme_id: UUID) -> Optional[models.Filme]:
        return db.query(models.Filme).filter(models.Filme.id == filme_id).first()

    @staticmethod
    def list_movies(db: Session, skip: int = 0, limit: int = 20) -> List[models.Filme]:
        return db.query(models.Filme).offset(skip).limit(limit).all()

    @staticmethod
    def update_movie(db: Session, filme_id: UUID, filme_update: schemas.FilmeUpdate) -> Optional[models.Filme]:
        filme = db.query(models.Filme).filter(models.Filme.id == filme_id).first()
        if not filme:
            return None
        for field, value in filme_update.dict(exclude_unset=True).items():
            if field == "elenco" and value is not None:
                setattr(filme, field, ", ".join(value))
            elif value is not None:
                setattr(filme, field, value)
        db.commit()
        db.refresh(filme)
        return filme

    @staticmethod
    def delete_movie(db: Session, filme_id: UUID) -> bool:
        filme = db.query(models.Filme).filter(models.Filme.id == filme_id).first()
        if not filme:
            return False
        db.delete(filme)
        db.commit()
        return True
