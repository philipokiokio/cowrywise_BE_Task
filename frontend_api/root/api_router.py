from fastapi import APIRouter
from routers.user_route import api_router as user_router
from routers.book_route import api_router as book_router

router = APIRouter()

router.include_router(router=user_router)
router.include_router(router=book_router)
