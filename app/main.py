from fastapi import FastAPI
from app.api import user_controller, movie_controller, rating_controller

app = FastAPI(
    title="MovieTracker API",
    description="API RESTful para gerenciar filmes, usuários e avaliações.",
    version="1.0.0"
)

# Inclui as rotas dos controllers
app.include_router(user_controller.router, prefix="/usuarios", tags=["Usuários"])
app.include_router(movie_controller.router, prefix="/filmes", tags=["Filmes"])
app.include_router(rating_controller.router, prefix="/avaliacoes", tags=["Avaliações"])

@app.get("/")
def read_root():
    return {"message": "Bem-vindo à MovieTracker API!"}
