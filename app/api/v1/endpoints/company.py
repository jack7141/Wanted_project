from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status, Header

from app.core.container import Container
from app.schema.company_schema import CompanyResp
from app.services.company_service import CompanyService

router = APIRouter(
    prefix="/companies",
    tags=["company"],
    redirect_slashes=False,
)


@router.get("/{company_id}",
            summary="기업 조회",
            response_model=CompanyResp
            )
@inject
async def get_company(
    company_id: str,
    x_wanted_language: str = Header("ko"),
    service: CompanyService = Depends(Provide[Container.company_service]),
):
    resp = service.get_company_by_language(company_name_ko=company_id, eager=True, x_wanted_language=x_wanted_language)
    return resp