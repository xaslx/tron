from fastapi import APIRouter, Query, HTTPException, status
from typing import Annotated
from dishka.integrations.fastapi import inject, FromDishka as Depends
from src.use_cases.get_tron_info import GetTronInfoUseCase
from src.use_cases.get_all_requests import ListRequestsUseCase
from src.schemas.tron import TronInfo, TronRequestOut
from src.schemas.pagination import PaginationOut
from src.exceptions.tron import InvalidTronAddressException



router: APIRouter = APIRouter()



@router.get(
        '/tron',
        status_code=status.HTTP_200_OK,
        responses={
        status.HTTP_200_OK: {'model': TronInfo},
        status.HTTP_400_BAD_REQUEST: {'description': 'Неверный Tron-адрес'},
    },
)
@inject
async def get_tron_data(
    address: Annotated[str, Query(description='Tron адрес')],
    use_case: Depends[GetTronInfoUseCase],
) -> TronInfo:
    
    try:
        return await use_case.execute(address=address)
    except InvalidTronAddressException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Неверный Tron адрес')
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ошибка при получении информации о Tron адресе'
        )


@router.get(
        '/requests',
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_200_OK: {'model': PaginationOut[TronRequestOut]},
        },
)
@inject
async def get_list_requests(
    use_case: Depends[ListRequestsUseCase],
    skip: Annotated[int, Query(ge=0)]=0,
    limit: Annotated[int, Query( ge=1)]=20,
) -> PaginationOut[TronRequestOut]:
    
    return await use_case.execute(skip=skip, limit=limit)