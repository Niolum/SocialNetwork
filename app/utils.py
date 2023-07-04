import os
from passlib.context import CryptContext
from redis import asyncio as aioredis

from dotenv import load_dotenv


load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")
redis = aioredis.from_url(REDIS_URL)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)