from fastapi import FastAPI
from routers.sign import sign

app = FastAPI()

app.include_router(sign)