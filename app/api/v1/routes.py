from fastapi import APIRouter

from app.api.v1.endpoints.tag import router as tag_router

routers = APIRouter()
router_list = [
    tag_router
]


for router in router_list:
    router.tags = routers.tags.append("v1")
    routers.include_router(router)