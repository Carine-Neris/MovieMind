# MovieTracker API

API RESTful para gerenciar filmes, usuários e avaliações. Desenvolvida com FastAPI, SQLAlchemy e PostgreSQL.

## Requisitos

- Python 3.10+
- PostgreSQL 12+
- (Opcional) [Poetry](https://python-poetry.org/) ou [pipenv](https://pipenv.pypa.io/en/latest/) para gerenciamento de ambiente

## Instalação

1. **Clone o repositório**

```sh
git clone https://github.com/Carine-Neris/MovieMind.git
cd movietracker
```

2. **Crie e ative um ambiente virtual**

```sh
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. **Instale as dependências**

```sh
pip install -r requirements.txt
```

4. **Configure o banco de dados**

Crie um banco de dados PostgreSQL chamado `movietracker` (ou outro nome de sua preferência):

```sh
# No terminal do psql:
CREATE DATABASE movietracker;
```

Configure as variáveis no arquivo `.env` na raiz do projeto:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/movietracker
JWT_SECRET_KEY=sua_chave_secreta_supersegura
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Altere usuário, senha e host conforme sua configuração.  
Defina uma chave secreta forte para `JWT_SECRET_KEY`.

## Migrações de Banco de Dados

O projeto utiliza Alembic para controle de migrações.

1. **Inicialize o Alembic (se necessário):**

```sh
alembic init alembic
```

2. **Edite o arquivo `alembic.ini`** e configure a variável `sqlalchemy.url` com a mesma URL do seu `.env`.

3. **Gere uma nova migração:**

```sh
alembic revision --autogenerate -m "Criação das tabelas iniciais"
```

4. **Aplique as migrações:**

```sh
alembic upgrade head
```

## Executando o Projeto

Com as dependências instaladas e o banco migrado, rode o servidor:

```sh
uvicorn app.main:app --reload
```

Acesse a documentação interativa em: [http://localhost:8000/docs](http://localhost:8000/docs)

## Autenticação JWT

A API utiliza autenticação baseada em JWT para proteger rotas de usuário.

### Como obter um token

Faça uma requisição `POST` para `/usuarios/login` com os campos `username` (email) e `password`:

```sh
curl -X POST http://localhost:8000/usuarios/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=seu@email.com&password=suasenha"
```

A resposta será:

```json
{
  "access_token": "SEU_TOKEN_JWT",
  "token_type": "bearer"
}
```

### Como acessar rotas protegidas

Inclua o token JWT no header `Authorization`:

```sh
curl http://localhost:8000/usuarios/me \
  -H "Authorization: Bearer SEU_TOKEN_JWT"
```

A rota `/usuarios/me` retorna os dados do usuário autenticado.

### Variáveis de ambiente para JWT

No arquivo `.env`:

```
JWT_SECRET_KEY=sua_chave_secreta_supersegura
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Rodando os Testes

Os testes unitários estão em `app/tests/`. Para executá-los:

```sh
pytest app/tests/
```

## Estrutura do Projeto

```
app/
  ├── api/           # Controllers (rotas FastAPI)
  ├── crud/          # Operações CRUD (opcional)
  ├── models.py      # Modelos SQLAlchemy
  ├── schemas.py     # Schemas Pydantic (DTOs)
  ├── services/      # Camada de serviços (lógica de negócio)
  ├── database.py    # Configuração do banco de dados
  ├── main.py        # Inicialização do FastAPI
  └── tests/         # Testes unitários
```

## Observações

- Para produção, configure variáveis de ambiente seguras e utilize hash de senha (bcrypt já incluso).
- JWT e autenticação podem ser facilmente adicionados usando `python-jose`.
- O projeto já está preparado para deploy em serviços como Heroku, Railway, Render, etc.

---

Desenvolvido por [Carine Neris](https://github.com/Carine-Neris).  
Contribuições são bem-vindas!
