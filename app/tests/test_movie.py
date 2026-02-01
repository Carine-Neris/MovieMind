import pytest
from uuid import uuid4
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Filme
from app.schemas import FilmeCreate, FilmeUpdate
from app.services.movie_service import MovieService

# Configuração de banco de dados em memória para testes
DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine(DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_movie(db_session):
    filme_data = FilmeCreate(
        titulo="Matrix",
        genero="Ficção Científica",
        duracao=136,
        ano=1999,
        diretor="Lana Wachowski, Lilly Wachowski",
        elenco=["Keanu Reeves", "Laurence Fishburne", "Carrie-Anne Moss"],
        sinopse="Um hacker descobre a verdade sobre sua realidade."
    )
    filme = MovieService.create_movie(db_session, filme_data)
    assert filme.id is not None
    assert filme.titulo == "Matrix"
    assert "Keanu Reeves" in filme.elenco

def test_get_movie(db_session):
    filme_data = FilmeCreate(
        titulo="Interestelar",
        genero="Ficção Científica",
        duracao=169,
        ano=2014,
        diretor="Christopher Nolan",
        elenco=["Matthew McConaughey", "Anne Hathaway"],
        sinopse="Uma equipe viaja por um buraco de minhoca em busca de um novo lar para a humanidade."
    )
    filme = MovieService.create_movie(db_session, filme_data)
    fetched = MovieService.get_movie(db_session, filme.id)
    assert fetched is not None
    assert fetched.titulo == "Interestelar"

def test_list_movies(db_session):
    filmes = [
        FilmeCreate(
            titulo="Filme 1",
            genero="Ação",
            duracao=100,
            ano=2020,
            diretor="Diretor 1",
            elenco=["Ator 1"],
            sinopse="Sinopse 1"
        ),
        FilmeCreate(
            titulo="Filme 2",
            genero="Drama",
            duracao=120,
            ano=2021,
            diretor="Diretor 2",
            elenco=["Ator 2"],
            sinopse="Sinopse 2"
        ),
    ]
    for f in filmes:
        MovieService.create_movie(db_session, f)
    lista = MovieService.list_movies(db_session)
    assert len(lista) == 2
    titulos = [f.titulo for f in lista]
    assert "Filme 1" in titulos
    assert "Filme 2" in titulos

def test_update_movie(db_session):
    filme_data = FilmeCreate(
        titulo="Antigo",
        genero="Ação",
        duracao=90,
        ano=2010,
        diretor="Diretor Antigo",
        elenco=["Ator Antigo"],
        sinopse="Sinopse antiga"
    )
    filme = MovieService.create_movie(db_session, filme_data)
    update_data = FilmeUpdate(
        titulo="Novo",
        genero="Comédia",
        duracao=95,
        ano=2011,
        diretor="Diretor Novo",
        elenco=["Ator Novo"],
        sinopse="Sinopse nova"
    )
    updated = MovieService.update_movie(db_session, filme.id, update_data)
    assert updated.titulo == "Novo"
    assert updated.genero == "Comédia"
    assert "Ator Novo" in updated.elenco

def test_delete_movie(db_session):
    filme_data = FilmeCreate(
        titulo="Para Deletar",
        genero="Terror",
        duracao=80,
        ano=2005,
        diretor="Diretor X",
        elenco=["Ator X"],
        sinopse="Sinopse X"
    )
    filme = MovieService.create_movie(db_session, filme_data)
    deleted = MovieService.delete_movie(db_session, filme.id)
    assert deleted is True
    assert MovieService.get_movie(db_session, filme.id) is None

def test_delete_movie_inexistente(db_session):
    fake_id = uuid4()
    deleted = MovieService.delete_movie(db_session, fake_id)
    assert deleted is False
