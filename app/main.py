# src/main.py

from fastapi import FastAPI, Request, APIRouter
from routers.reviews import router
from logging_config import LoggerSetup
import logging
import database

# Cria um logger raiz
logger_setup = LoggerSetup()

# Adiciona o logger para o módulo
LOGGER = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup():
    LOGGER.info("Starting up...")
    database.Base.metadata.create_all(bind=database.engine)


api_router = APIRouter(prefix="/reviews")

api_router.include_router(router)

app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8003)
