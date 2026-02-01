import uuid

from sqlalchemy import (
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Tabelas de associação para listas de filmes do usuário
usuario_filmes_favoritos = Table(
    "usuario_filmes_favoritos",
    Base.metadata,
    Column("usuario_id", UUID(as_uuid=True), ForeignKey("usuarios.id"), primary_key=True),
    Column("filme_id", UUID(as_uuid=True), ForeignKey("filmes.id"), primary_key=True),
)

usuario_filmes_assistidos = Table(
    "usuario_filmes_assistidos",
    Base.metadata,
    Column("usuario_id", UUID(as_uuid=True), ForeignKey("usuarios.id"), primary_key=True),
    Column("filme_id", UUID(as_uuid=True), ForeignKey("filmes.id"), primary_key=True),
)

usuario_filmes_em_espera = Table(
    "usuario_filmes_em_espera",
    Base.metadata,
    Column("usuario_id", UUID(as_uuid=True), ForeignKey("usuarios.id"), primary_key=True),
    Column("filme_id", UUID(as_uuid=True), ForeignKey("filmes.id"), primary_key=True),
)


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    data_nascimento = Column(Date, nullable=False)

    filmes_favoritos = relationship(
        "Filme",
        secondary=usuario_filmes_favoritos,
        back_populates="usuarios_favoritaram",
        lazy="joined",
    )
    filmes_assistidos = relationship(
        "Filme",
        secondary=usuario_filmes_assistidos,
        back_populates="usuarios_assistiram",
        lazy="joined",
    )
    filmes_em_espera = relationship(
        "Filme",
        secondary=usuario_filmes_em_espera,
        back_populates="usuarios_em_espera",
        lazy="joined",
    )

    avaliacoes = relationship("Avaliacao", back_populates="usuario", cascade="all, delete-orphan")


class Filme(Base):
    __tablename__ = "filmes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String(200), nullable=False)
    genero = Column(String(100), nullable=False)
    duracao = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)
    diretor = Column(String(100), nullable=False)
    elenco = Column(Text, nullable=True)
    sinopse = Column(Text, nullable=True)

    avaliacoes = relationship("Avaliacao", back_populates="filme", cascade="all, delete-orphan")

    usuarios_favoritaram = relationship(
        "Usuario",
        secondary=usuario_filmes_favoritos,
        back_populates="filmes_favoritos",
        lazy="joined",
    )
    usuarios_assistiram = relationship(
        "Usuario",
        secondary=usuario_filmes_assistidos,
        back_populates="filmes_assistidos",
        lazy="joined",
    )
    usuarios_em_espera = relationship(
        "Usuario",
        secondary=usuario_filmes_em_espera,
        back_populates="filmes_em_espera",
        lazy="joined",
    )


class Avaliacao(Base):
    __tablename__ = "avaliacoes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nota = Column(Float, nullable=False)
    comentario = Column(Text, nullable=True)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)
    filme_id = Column(UUID(as_uuid=True), ForeignKey("filmes.id"), nullable=False)

    usuario = relationship("Usuario", back_populates="avaliacoes")
    filme = relationship("Filme", back_populates="avaliacoes")

    __table_args__ = (
        UniqueConstraint("usuario_id", "filme_id", name="unique_usuario_filme_avaliacao"),
    )
