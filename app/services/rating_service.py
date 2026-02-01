from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


class RatingService:
    @staticmethod
    def create_rating(db: Session, rating_data: schemas.AvaliacaoCreate) -> models.Avaliacao:
        # Verifica se o usuário existe
        usuario = db.query(models.Usuario).filter(models.Usuario.id == rating_data.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        # Verifica se o filme existe
        filme = db.query(models.Filme).filter(models.Filme.id == rating_data.filme_id).first()
        if not filme:
            raise HTTPException(status_code=404, detail="Filme não encontrado")
        # Verifica se já existe avaliação desse usuário para esse filme
        avaliacao_existente = db.query(models.Avaliacao).filter(
            models.Avaliacao.usuario_id == rating_data.usuario_id,
            models.Avaliacao.filme_id == rating_data.filme_id
        ).first()
        if avaliacao_existente:
            raise HTTPException(
                status_code=400,
                detail="Avaliação já existe para este usuário e filme"
            )
        nova_avaliacao = models.Avaliacao(
            nota=rating_data.nota,
            comentario=rating_data.comentario,
            usuario_id=rating_data.usuario_id,
            filme_id=rating_data.filme_id
        )
        db.add(nova_avaliacao)
        db.commit()
        db.refresh(nova_avaliacao)
        return nova_avaliacao

    @staticmethod
    def get_rating(db: Session, rating_id: UUID) -> Optional[models.Avaliacao]:
        avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id == rating_id).first()
        if not avaliacao:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        return avaliacao

    @staticmethod
    def list_ratings(db: Session, skip: int = 0, limit: int = 100) -> List[models.Avaliacao]:
        return db.query(models.Avaliacao).offset(skip).limit(limit).all()

    @staticmethod
    def update_rating(db: Session, rating_id: UUID, rating_update: schemas.AvaliacaoUpdate) -> models.Avaliacao:
        avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id == rating_id).first()
        if not avaliacao:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        if rating_update.nota is not None:
            avaliacao.nota = rating_update.nota
        if rating_update.comentario is not None:
            avaliacao.comentario = rating_update.comentario
        db.commit()
        db.refresh(avaliacao)
        return avaliacao

    @staticmethod
    def delete_rating(db: Session, rating_id: UUID) -> None:
        avaliacao = db.query(models.Avaliacao).filter(models.Avaliacao.id == rating_id).first()
        if not avaliacao:
            raise HTTPException(status_code=404, detail="Avaliação não encontrada")
        db.delete(avaliacao)
        db.commit()
