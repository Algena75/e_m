import json

import pytest
from fastapi import status
from httpx import AsyncClient

NEW_OBJECT = dict(name="Any new object")
NEW_USER = dict(email="user@example.com",
                firstname="Richard",
                password="string")


@pytest.mark.anyio
class TestAPI:

    @pytest.mark.parametrize("endpoint", [("put", "/objects/1"),
                                          ("delete", "/objects/1"),
                                          ("post", "/objects")])
    async def test_unauthorized_user_cant_crud(self, client: AsyncClient,
                                               endpoint):
        """
        Неавторизованный пользователь не имеет доступа к небезопасным методам.
        """
        response = await getattr(client, endpoint[0])(endpoint[1])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Unauthorized"}


    @pytest.mark.parametrize("endpoint", [("get", "/objects"),
                                          ("get", "/objects/1")])
    async def test_authorized_user_can_view_objects(
        self, authenticated_client: AsyncClient, endpoint,
    ):
        """
        Авторизованный пользователь может просматривать объекты.
        """
        response = await getattr(authenticated_client,
                                 endpoint[0])(endpoint[1])
        assert response.status_code == status.HTTP_200_OK


    async def test_authorized_user_can_add_object(
        self, authenticated_client: AsyncClient
    ):
        """
        Авторизованный пользователь может добавить запись.
        """
        response = await authenticated_client.post("/objects",
                                                   data=json.dumps(NEW_OBJECT))
        assert response.status_code == status.HTTP_201_CREATED
        assert NEW_OBJECT.get("name") in response.text
