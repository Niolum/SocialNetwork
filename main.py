import uvicorn
from fastapi import FastAPI

from app.routers import user_router, post_router, like_dislike_router
from app.exceptions import (
    Exception_404, 
    ExceptionOwnerUserID,
    ExceptionTitleExists,
    ExceptionOwnPost,
    ExceptionEqualLikeDislike,
    exception_404_handler, 
    owner_user_id_exception,
    title_exists_exception,
    own_post_exception,
    equal_like_dislike_exception
)


app = FastAPI()

app.include_router(user_router)
app.include_router(post_router)
app.include_router(like_dislike_router)

app.add_exception_handler(Exception_404, exception_404_handler)
app.add_exception_handler(ExceptionOwnerUserID, owner_user_id_exception)
app.add_exception_handler(ExceptionTitleExists, title_exists_exception)
app.add_exception_handler(ExceptionOwnPost, own_post_exception)
app.add_exception_handler(ExceptionEqualLikeDislike, equal_like_dislike_exception)


if __name__ == "__main__":
    uvicorn.run()