from fastapi import FastAPI

from config import database
from endpoint import task_group_endpoint

database.base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(task_group_endpoint.router)
