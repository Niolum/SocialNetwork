from fastapi import Request, status
from fastapi.responses import JSONResponse


class Exception_404(Exception):
    def __init__(self, name: str):
        self.name = name


async def exception_404_handler(request: Request, exc: Exception_404):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"{exc.name} cannot be Found"}
    )


class ExceptionOwnerUserID(Exception):
    def __init__(self, name: str):
        self.name = name


async def owner_user_id_exception(request: Request, exc: ExceptionOwnerUserID):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"{exc.name} must be equal to the id of the current user"}
    )


class ExceptionTitleExists(Exception):
    pass


async def title_exists_exception(request: Request, exc: ExceptionTitleExists):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "There is already a Post with this title"}
    )


class ExceptionOwnPost(Exception):
    pass


async def own_post_exception(request: Request, exc: ExceptionOwnPost):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "The post must be owned by the current user"}
    )


class ExceptionEqualLikeDislike(Exception):
    pass


async def equal_like_dislike_exception(request: Request, exc: ExceptionEqualLikeDislike):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": "Dislike and Like cannot be True or False at the same time"}
    )