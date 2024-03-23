from fastapi import FastAPI
from dotenv import load_dotenv
from routes.auth import auth

load_dotenv()

app = FastAPI()

app.include_router(auth)