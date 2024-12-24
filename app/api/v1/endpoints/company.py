from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from app.core.container import Container
from app.models.base_model import get_clean_language, LANGUAGE_ACTION_MAP
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
    x_wanted_language: str = Depends(get_clean_language),
    service: CompanyService = Depends(Provide[Container.company_service]),
):
    field = LANGUAGE_ACTION_MAP.get(x_wanted_language)
    resp = service.get_company_by_language(company_id, field, x_wanted_language)
    return resp