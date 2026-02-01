from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas


class UserService:
    @staticmethod
    def create_user(db: Session, user: schemas.UsuarioCreate) -> models.Usuario:
        db_user = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
        # Em produção, faça hash da senha!
        new_user = models.Usuario(
            nome=user.nome,
            email=user.email,
            senha=user.senha,
            data_nascimento=user.data_nascimento
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def get_user(db: Session, user_id: UUID) -> models.Usuario:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[models.Usuario]:
        return db.query(models.Usuario).filter(models.Usuario.email == email).first()

    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.Usuario]:
        return db.query(models.Usuario).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_update: schemas.UsuarioUpdate) -> models.Usuario:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        for var, value in vars(user_update).items():
            if value is not None:
                setattr(user, var, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> None:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        db.delete(user)
        db.commit()

    @staticmethod
    def add_favorite(db: Session, user_id: UUID, movie_id: UUID) -> models.Usuario:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        movie = db.query(models.Filme).filter(models.Filme.id == movie_id).first()
        if not user or not movie:
            raise HTTPException(status_code=404, detail="Usuário ou filme não encontrado")
        if movie not in user.filmes_favoritos:
            user.filmes_favoritos.append(movie)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def remove_favorite(db: Session, user_id: UUID, movie_id: UUID) -> models.Usuario:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        movie = db.query(models.Filme).filter(models.Filme.id == movie_id).first()
        if not user or not movie:
            raise HTTPException(status_code=404, detail="Usuário ou filme não encontrado")
        if movie in user.filmes_favoritos:
            user.filmes_favoritos.remove(movie)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def add_watched(db: Session, user_id: UUID, movie_id: UUID) -> models.Usuario:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        movie = db.query(models.Filme).filter(models.Filme.id == movie_id).first()
        if not user or not movie:
            raise HTTPException(status_code=404, detail="Usuário ou filme não encontrado")
        if movie not in user.filmes_assistidos:
            user.filmes_assistidos.append(movie)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def remove_watched(db: Session, user_id: UUID, movie_id: UUID) -> models.Usuario:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        movie = db.query(models.Filme).filter(models.Filme.id == movie_id).first()
        if not user or not movie:
            raise HTTPException(status_code=404, detail="Usuário ou filme não encontrado")
        if movie in user.filmes_assistidos:
            user.filmes_assistidos.remove(movie)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def add_waiting(db: Session, user_id: UUID, movie_id: UUID) -> models.Usuario:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        movie = db.query(models.Filme).filter(models.Filme.id == movie_id).first()
        if not user or not movie:
            raise HTTPException(status_code=404, detail="Usuário ou filme não encontrado")
        if movie not in user.filmes_em_espera:
            user.filmes_em_espera.append(movie)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def remove_waiting(db: Session, user_id: UUID, movie_id: UUID) -> models.Usuario:
        user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
        movie = db.query(models.Filme).filter(models.Filme.id == movie_id).first()
        if not user or not movie:
            raise HTTPException(status_code=404, detail="Usuário ou filme não encontrado")
        if movie in user.filmes_em_espera:
            user.filmes_em_espera.remove(movie)
            db.commit()
            db.refresh(user)
        return user
