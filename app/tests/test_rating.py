import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Usuario, Filme, Avaliacao
from app.schemas import AvaliacaoCreate, AvaliacaoUpdate
from app.services.rating_service import RatingService

# Configuração de banco de dados em memória para testes
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def usuario(db):
    user = Usuario(
        id=uuid4(),
        nome="Usuário Teste",
        email="teste@exemplo.com",
        senha="senha123",
        data_nascimento="1990-01-01"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def filme(db):
    movie = Filme(
        id=uuid4(),
        titulo="Filme Teste",
        genero="Ação",
        duracao=120,
        ano=2022,
        diretor="Diretor Teste",
        elenco="Ator 1, Ator 2",
        sinopse="Sinopse do filme teste"
    )
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

def test_create_rating(db, usuario, filme):
    data = AvaliacaoCreate(
        nota=8,
        comentario="Muito bom!",
        usuario_id=usuario.id,
        filme_id=filme.id
    )
    avaliacao = RatingService.create_rating(db, data)
    assert avaliacao.nota == 8
    assert avaliacao.comentario == "Muito bom!"
    assert avaliacao.usuario_id == usuario.id
    assert avaliacao.filme_id == filme.id

def test_create_duplicate_rating_raises(db, usuario, filme):
    data = AvaliacaoCreate(
        nota=7,
        comentario="Gostei!",
        usuario_id=usuario.id,
        filme_id=filme.id
    )
    # Já existe uma avaliação para esse usuário e filme
    with pytest.raises(Exception):
        RatingService.create_rating(db, data)

def test_get_rating(db, usuario, filme):
    avaliacao = db.query(Avaliacao).filter_by(usuario_id=usuario.id, filme_id=filme.id).first()
    result = RatingService.get_rating(db, avaliacao.id)
    assert result.id == avaliacao.id

def test_list_ratings(db):
    ratings = RatingService.list_ratings(db)
    assert len(ratings) >= 1

def test_update_rating(db, usuario, filme):
    avaliacao = db.query(Avaliacao).filter_by(usuario_id=usuario.id, filme_id=filme.id).first()
    update_data = AvaliacaoUpdate(nota=9, comentario="Excelente!")
    updated = RatingService.update_rating(db, avaliacao.id, update_data)
    assert updated.nota == 9
    assert updated.comentario == "Excelente!"

def test_delete_rating(db, usuario, filme):
    avaliacao = db.query(Avaliacao).filter_by(usuario_id=usuario.id, filme_id=filme.id).first()
    RatingService.delete_rating(db, avaliacao.id)
    deleted = db.query(Avaliacao).filter_by(id=avaliacao.id).first()
    assert deleted is None
