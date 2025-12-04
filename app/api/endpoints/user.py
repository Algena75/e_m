from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.crud import user_crud
from app.core.db import get_async_session
from app.core.user import (auth_backend, current_superuser, current_user,
                           fastapi_users)
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@router.get('/users', tags=['users'],
            response_model=List[UserRead],
            dependencies=[Depends(current_user)])
async def get_users_list(
    session: AsyncSession = Depends(get_async_session),
) -> List[UserRead]:
    """Возвращает список пользователей."""
    all_users = await user_crud.get_multi(session)
    if len(all_users) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Список пользователей пуст!'
        )
    return all_users


@router.delete(
    '/users/{id}',
    tags=['users'], dependencies=[Depends(current_superuser)]
)
async def delete_user(
    id: int, session: AsyncSession = Depends(get_async_session),
):
    """Don't delete users - just deactivate."""
    user_to_deactivate = await user_crud.get(id, session)
    if not user_to_deactivate:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Пользователь с id={id} не найден!'
        )
    if user_to_deactivate.is_active:
        await user_crud.update(user_to_deactivate, UserUpdate(is_active=False), session)
    return {'message': f'Пользователь с id={id} деактивирован'}


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'], dependencies=[Depends(current_user)]
)
