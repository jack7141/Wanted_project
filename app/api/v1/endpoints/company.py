from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.core.container import Container
from app.services.company_service import CompanyService

router = APIRouter(
    prefix="/companies",
    tags=["company"],
    redirect_slashes=False,
)

# 검색된 회사가 없는경우 404를 리턴합니다.
# resp = api.get(
#     "/companies/없는회사", headers=[("x-wanted-language", "ko")]
# )
#
# assert resp.status_code == 404
@router.get("/{company_id}", status_code=status.HTTP_200_OK)
@inject
async def get_company(
    company_id: str,
    service: CompanyService = Depends(Provide[Container.company_service]),
):
    return service.get_by_id(company_id)
