from typing import List, Optional
from uuid import UUID
from datetime import date
from pydantic import BaseModel, EmailStr, Field


# Avaliação Schemas
class AvaliacaoBase(BaseModel):
    nota: int = Field(..., ge=0, le=10)
    comentario: Optional[str] = None

class AvaliacaoCreate(AvaliacaoBase):
    usuario_id: UUID
    filme_id: UUID

class AvaliacaoUpdate(BaseModel):
    nota: Optional[int] = Field(None, ge=0, le=10)
    comentario: Optional[str] = None

class AvaliacaoOut(AvaliacaoBase):
    id: UUID
    usuario_id: UUID
    filme_id: UUID

    class Config:
        from_attributes = True


# Filme Schemas
class FilmeBase(BaseModel):
    titulo: str
    genero: str
    duracao: int
    ano: int
    diretor: str
    elenco: List[str]
    sinopse: Optional[str] = None

class FilmeCreate(FilmeBase):
    pass

class FilmeUpdate(BaseModel):
    titulo: Optional[str] = None
    genero: Optional[str] = None
    duracao: Optional[int] = None
    ano: Optional[int] = None
    diretor: Optional[str] = None
    elenco: Optional[List[str]] = None
    sinopse: Optional[str] = None

class FilmeOut(FilmeBase):
    id: UUID
    avaliacao: Optional[List[AvaliacaoOut]] = []
    usuarios_favoritaram: Optional[List[UUID]] = []

    class Config:
        from_attributes = True


# Usuário Schemas
class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    data_nascimento: date

class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., max_length=72)

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    data_nascimento: Optional[date] = None

class UsuarioOut(UsuarioBase):
    id: UUID
    filmes_favoritos: Optional[List[FilmeOut]] = []
    filmes_assistidos: Optional[List[FilmeOut]] = []
    filmes_em_espera: Optional[List[FilmeOut]] = []

    class Config:
        from_attributes = True
