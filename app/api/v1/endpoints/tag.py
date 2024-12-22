from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container

router = APIRouter(
    prefix="/tag",
    tags=["tag"],
    redirect_slashes=False,
)


@router.get("/{tag_id}", status_code=status.HTTP_200_OK)
@inject
async def get_tag(
    tag_id: int,
):
    return None
