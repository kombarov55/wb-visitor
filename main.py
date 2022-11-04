import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import database
from endpoint import task_group_endpoint

database.base.metadata.create_all(bind=database.engine)
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

app = FastAPI()

app.include_router(task_group_endpoint.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)