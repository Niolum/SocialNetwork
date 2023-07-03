import uvicorn
from fastapi import FastAPI

from app.routers import user_router


app = FastAPI()

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run()