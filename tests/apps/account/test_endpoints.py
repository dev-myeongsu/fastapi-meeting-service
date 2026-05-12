import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from appserver.apps.account.endpoints import user_detail
from appserver.apps.account.models import User


async def test_user_detail(
    db_session: AsyncSession, client: TestClient, host_user: User
):

    result = await user_detail(host_user.username, db_session)
    assert result.id == host_user.id
    assert result.username == host_user.username
    assert result.email == host_user.email
    assert result.display_name == host_user.display_name
    assert result.is_host == host_user.is_host
    assert result.created_at is not None
    assert result.updated_at is not None

    response = client.get(f"/account/users/{host_user.username}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["id"] == host_user.id
    assert data["username"] == host_user.username
    assert data["email"] == host_user.email
    assert data["display_name"] == host_user.display_name
    assert data["is_host"] == host_user.is_host
    assert data["created_at"] is not None
    assert data["updated_at"] is not None

    with pytest.raises(HTTPException) as exc_info:
        await user_detail("not_found", db_session)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

    response = client.get("/account/users/not_found")
    assert response.status_code == status.HTTP_404_NOT_FOUND
