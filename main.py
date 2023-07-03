import uvicorn
from fastapi import FastAPI

from app.routers import user_router, post_router, like_dislike_router


app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(like_dislike_router)


if __name__ == "__main__":
    uvicorn.run()