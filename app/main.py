from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import settings
from app.core.init_db import create_db_if_not_exists, create_first_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Запускает процесс создания первого суперпользователя при запуске проекта.
    """
    print("starting up")
    await create_db_if_not_exists()
    await create_first_superuser()
    yield
    print("shutting down")

app = FastAPI(title=settings.APP_TITLE, description=settings.APP_DESCRIPTION,
              lifespan=lifespan)
app.include_router(main_router)


def run():
    """Функция программного запуска проекта для poetry."""
    uvicorn.run("web.main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == '__main__':
    run()
