from http import HTTPStatus
from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud import some_model_crud
from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.schemas.object import ObjectCreate, ObjectRead, ObjectUpdate

router = APIRouter(tags=['objects'])


@router.get('/objects', response_model=List[ObjectRead])
async def get_objects_list(
    session: AsyncSession = Depends(get_async_session),
) -> List[ObjectRead]:
    """Возвращает список объектов."""
    all_objects = await some_model_crud.get_multi(session)
    if len(all_objects) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Список объектов пуст!'
        )
    return all_objects


@router.post('/objects', response_model=(Dict | ObjectRead),
             dependencies=[Depends(current_user)],
             status_code=HTTPStatus.CREATED)
async def create_new_object(
    new_object: Dict | ObjectCreate,
    session: AsyncSession = Depends(get_async_session),
) -> Dict:
    """Создаёт новый объект."""
    return {'message': 'Объект создан', 'Объект': new_object}


@router.get('/objects/{id}', response_model=(Dict | ObjectRead))
async def get_object(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> (Dict | ObjectRead):
    """Возвращает объект по id."""
    return {'message': f'Объект {id} извлечён из БД.'}


@router.put('/objects/{id}',
            dependencies=[Depends(current_superuser)],
            response_model=(Dict | ObjectRead))
async def update_object(
    id: int,
    data_to_update: ObjectUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> (Dict | ObjectRead):
    """Superuser обновляет ранее созданную запись об объекте."""
    data_to_update = data_to_update.model_dump()
    return {'message': f'Объект {id} обновлён в БД.'}


@router.delete('/objects/{id}',
               dependencies=[Depends(current_superuser)],
               status_code=HTTPStatus.NO_CONTENT)
async def delete_object(
    id: int,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    """Superuser удаляет ранее созданную запись об объекте."""
    pass
