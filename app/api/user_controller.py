from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import database, models, schemas
from app.services.user_service import UserService
from app.services.auth_service import authenticate_user, create_access_token
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Security
from jose import JWTError
from typing import Optional
import os

router = APIRouter()

# Dependency
def get_db():
    db = next(database.get_db())
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Security(oauth2_scheme), db: database.SessionLocal = Depends(database.get_db)) -> models.Usuario:
    from app.services.auth_service import decode_access_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_access_token(token)
    if payload is None or "sub" not in payload:
        raise credentials_exception
    user_id = payload["sub"]
    user = db.query(models.Usuario).filter(models.Usuario.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

@router.post("/", response_model=schemas.UsuarioOut, status_code=status.HTTP_201_CREATED)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    # Hash da senha ao criar usuário
    from app.services.auth_service import get_password_hash
    usuario_dict = usuario.dict()
    usuario_dict["senha"] = get_password_hash(usuario.senha)
    usuario_hashed = schemas.UsuarioCreate(**usuario_dict)
    return UserService.create_user(db, usuario_hashed)

@router.get("/", response_model=List[schemas.UsuarioOut])
def list_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return UserService.list_users(db, skip, limit)

@router.post("/login", summary="Autenticação de usuário")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UsuarioOut)
def read_users_me(current_user: models.Usuario = Depends(get_current_user)):
    return current_user

@router.get("/{usuario_id}", response_model=schemas.UsuarioOut)
def get_usuario(usuario_id: UUID, db: Session = Depends(database.get_db)):
    return UserService.get_user(db, usuario_id)

@router.put("/{usuario_id}", response_model=schemas.UsuarioOut)
def update_usuario(usuario_id: UUID, usuario_update: schemas.UsuarioUpdate, db: Session = Depends(database.get_db)):
    return UserService.update_user(db, usuario_id, usuario_update)

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: UUID, db: Session = Depends(database.get_db)):
    UserService.delete_user(db, usuario_id)
    return None

# Rotas para manipular listas de filmes do usuário (favoritos, assistidos, em espera)
@router.post("/{usuario_id}/favoritos/{filme_id}", response_model=schemas.UsuarioOut)
def add_favorito(usuario_id: UUID, filme_id: UUID, db: Session = Depends(database.get_db)):
    return UserService.add_favorite(db, usuario_id, filme_id)

@router.post("/{usuario_id}/assistidos/{filme_id}", response_model=schemas.UsuarioOut)
def add_assistido(usuario_id: UUID, filme_id: UUID, db: Session = Depends(database.get_db)):
    return UserService.add_watched(db, usuario_id, filme_id)

@router.post("/{usuario_id}/em_espera/{filme_id}", response_model=schemas.UsuarioOut)
def add_em_espera(usuario_id: UUID, filme_id: UUID, db: Session = Depends(database.get_db)):
    return UserService.add_waiting(db, usuario_id, filme_id)

@router.delete("/{usuario_id}/favoritos/{filme_id}", response_model=schemas.UsuarioOut)
def remove_favorito(usuario_id: UUID, filme_id: UUID, db: Session = Depends(database.get_db)):
    return UserService.remove_favorite(db, usuario_id, filme_id)

@router.delete("/{usuario_id}/assistidos/{filme_id}", response_model=schemas.UsuarioOut)
def remove_assistido(usuario_id: UUID, filme_id: UUID, db: Session = Depends(database.get_db)):
    return UserService.remove_watched(db, usuario_id, filme_id)

@router.delete("/{usuario_id}/em_espera/{filme_id}", response_model=schemas.UsuarioOut)
def remove_em_espera(usuario_id: UUID, filme_id: UUID, db: Session = Depends(database.get_db)):
    return UserService.remove_waiting(db, usuario_id, filme_id)
