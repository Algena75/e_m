import json

import pytest
from fastapi import status
from httpx import AsyncClient

from .fixtures.fixture_data import app

NEW_USER = dict(email="new_user@example.com",
                firstname="Username",
                password="string")


@pytest.mark.anyio
class TestAuth:

    async def test_any_user_can_register(self, client: AsyncClient):
        """
        Любой пользователь может зарегистрироваться.
        """
        response = await client.post("/auth/register",
                                     data=json.dumps(NEW_USER))
        assert response.status_code == status.HTTP_201_CREATED
        assert NEW_USER.get("email") in response.text


    async def test_new_user_can_get_token(self, client: AsyncClient):
        """
        Пользователь при аутентификации получает действительный токен.
        """
        new_user_token = await client.post(
            "/auth/jwt/login",
            data={'username': NEW_USER["email"],
                  'password': NEW_USER['password']}
        )
        assert new_user_token.status_code == status.HTTP_200_OK
        assert "access_token" in new_user_token.json()
        NEW_USER['access_token'] = (
            f'Bearer {new_user_token.json().get("access_token")}'
        )


    @pytest.mark.parametrize("endpoint", [("get", "/users"),
                                          ("get", "/users/me")])
    async def test_new_user_can_view_users(self, 
                                           client: AsyncClient, endpoint):
        """
        Пользователь по токену получает доступ к списку пользователей и личной
        странице.
        """
        response = await getattr(
            client, endpoint[0]
        )(endpoint[1], headers={'Authorization': NEW_USER["access_token"]})
        assert response.status_code == status.HTTP_200_OK


    @pytest.mark.parametrize("endpoint", [("delete", "/users/1")])
    async def test_superuser_can_delete_users(self,
                                              superuser_client: AsyncClient,
                                              endpoint):
        """
        Суперпользователь может удалять пользователей.

        """
        print(app.dependency_overrides)
        response = await getattr(superuser_client, endpoint[0])(endpoint[1])
        assert response.status_code == status.HTTP_200_OK
        assert 'Пользователь с id=1 деактивирован' in response.text
