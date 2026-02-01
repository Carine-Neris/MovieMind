import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import date
from uuid import uuid4

from app.models import Base, Usuario, Filme
from app.schemas import UsuarioCreate, UsuarioUpdate
from app.services.user_service import UserService

# Configuração do banco de dados em memória para testes
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_create_user(db):
    user_data = UsuarioCreate(
        nome="Usuário Teste",
        email="teste@exemplo.com",
        senha="senha123",
        data_nascimento=date(1990, 1, 1)
    )
    user = UserService.create_user(db, user_data)
    assert user.id is not None
    assert user.nome == "Usuário Teste"
    assert user.email == "teste@exemplo.com"

def test_create_user_duplicate_email(db):
    user_data = UsuarioCreate(
        nome="Outro Usuário",
        email="teste@exemplo.com",
        senha="outrasenha",
        data_nascimento=date(1992, 2, 2)
    )
    with pytest.raises(Exception):
        UserService.create_user(db, user_data)

def test_get_user(db):
    user = db.query(Usuario).filter(Usuario.email == "teste@exemplo.com").first()
    fetched = UserService.get_user(db, user.id)
    assert fetched.email == "teste@exemplo.com"

def test_list_users(db):
    users = UserService.list_users(db)
    assert len(users) >= 1

def test_update_user(db):
    user = db.query(Usuario).filter(Usuario.email == "teste@exemplo.com").first()
    update_data = UsuarioUpdate(nome="Nome Atualizado")
    updated = UserService.update_user(db, user.id, update_data)
    assert updated.nome == "Nome Atualizado"

def test_add_and_remove_favorite(db):
    # Cria um filme para testar favoritos
    filme = Filme(
        id=uuid4(),
        titulo="Filme Teste",
        genero="Ação",
        duracao=120,
        ano=2022,
        diretor="Diretor Teste",
        elenco="Ator 1, Ator 2",
        sinopse="Sinopse teste"
    )
    db.add(filme)
    db.commit()
    db.refresh(filme)

    user = db.query(Usuario).filter(Usuario.email == "teste@exemplo.com").first()
    # Adiciona aos favoritos
    user = UserService.add_favorite(db, user.id, filme.id)
    assert any(f.id == filme.id for f in user.filmes_favoritos)
    # Remove dos favoritos
    user = UserService.remove_favorite(db, user.id, filme.id)
    assert all(f.id != filme.id for f in user.filmes_favoritos)

def test_add_and_remove_watched(db):
    filme = db.query(Filme).first()
    user = db.query(Usuario).filter(Usuario.email == "teste@exemplo.com").first()
    # Adiciona aos assistidos
    user = UserService.add_watched(db, user.id, filme.id)
    assert any(f.id == filme.id for f in user.filmes_assistidos)
    # Remove dos assistidos
    user = UserService.remove_watched(db, user.id, filme.id)
    assert all(f.id != filme.id for f in user.filmes_assistidos)

def test_add_and_remove_waiting(db):
    filme = db.query(Filme).first()
    user = db.query(Usuario).filter(Usuario.email == "teste@exemplo.com").first()
    # Adiciona à lista de espera
    user = UserService.add_waiting(db, user.id, filme.id)
    assert any(f.id == filme.id for f in user.filmes_em_espera)
    # Remove da lista de espera
    user = UserService.remove_waiting(db, user.id, filme.id)
    assert all(f.id != filme.id for f in user.filmes_em_espera)

def test_delete_user(db):
    user = db.query(Usuario).filter(Usuario.email == "teste@exemplo.com").first()
    UserService.delete_user(db, user.id)
    with pytest.raises(Exception):
        UserService.get_user(db, user.id)
