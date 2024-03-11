from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request

from config import settings, VERSION, BACKEND_CORS_ORIGINS, METHODS, HEADERS
from utils.log_bot import bot

PROJECT_NAME = settings.PROJECT_NAME
PROJECT_DESCRIPTION = settings.PROJECT_DESCRIPTION
ENVIRONMENT = settings.ENVIRONMENT


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.send_message(f"{PROJECT_NAME} application started.")
    yield
    await bot.send_message(f"{PROJECT_NAME} application finished.")


app = FastAPI(
    title=PROJECT_NAME,
    description=PROJECT_DESCRIPTION,
    version=VERSION,
    lifespan=lifespan,
)

if settings.STAGE == "prod":
    app.openapi_url = ''
    app.docs_url = ''

app.add_middleware(
    CORSMiddleware,
    allow_origins=BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=METHODS,
    allow_headers=HEADERS,
)


@app.get('/healthcheck')
async def healthcheck():
    return True


# app.mount('/api/v1', apiv1)

# @app.middleware("http")
# async def middleware_events(request: Request, call_next):
#     """fix for sqladmin support"""
#     if ENVIRONMENT != "local":
#         request.scope["scheme"] = "https"
#     response = await call_next(request)
#
#     return response


@app.get('/')
def index():
    return f"{PROJECT_NAME} {ENVIRONMENT} v. {VERSION}"


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8001, reload=True)
