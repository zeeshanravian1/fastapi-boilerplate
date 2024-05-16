"""
Test cases for role

Description:
- This module contains test cases for role route.

"""

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from main import app

client = TestClient(app)


# Function to get auth token
def get_auth_token() -> str:
    """
    Get auth token

    Description:
    - Get auth token for testing.

    """

    response: Response = client.post(
        url="/auth/login",
        data={
            "username": "admin",
            "password": "Admin@123",
        },
    )

    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_role() -> None:
    """
    Test create role

    Description:
    - Test create role with valid data.

    Expected Result:
    - Status code should be 201.

    """

    # Update headers with auth token
    client.headers.update(
        {
            "Authorization": f"Bearer {get_auth_token()}",
        }
    )

    json_data: dict[str, str] = {
        "role_name": "test_admin",
        "role_description": "Test administrator role",
    }
    response: Response = client.post(
        url="/v1/role", json=json_data, headers=client.headers
    )
    assert response.status_code == 201
    assert response.json()["role_name"] == "test_admin"


@pytest.mark.asyncio
async def test_get_role_by_id() -> None:
    """
    Test get role by id

    Description:
    - Test get role by id with valid data.

    Expected Result:
    - Status code should be 200.

    """

    response: Response = client.get(url="/v1/role/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


@pytest.mark.asyncio
async def test_get_all_roles() -> None:
    """
    Test get all roles

    Description:
    - Test get all roles with valid data.

    Expected Result:
    - Status code should be 200.

    """

    response: Response = client.get("/v1/role")
    assert response.status_code == 200
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_update_role() -> None:
    """
    Test update role

    Description:
    - Test update role with valid data.

    Expected Result:
    - Status code should be 202.

    """

    # Update headers with auth token
    client.headers.update(
        {
            "Authorization": f"Bearer {get_auth_token()}",
        }
    )

    json_data: dict[str, str] = {
        "role_name": "admin",
        "role_description": "Updated administrator role",
    }
    response: Response = client.put(
        url="/v1/role/1", json=json_data, headers=client.headers
    )
    assert response.status_code == 202
    assert response.json()["role_description"] == "Updated administrator role"


@pytest.mark.asyncio
async def test_delete_role() -> None:
    """
    Test delete role

    Description:
    - Test delete role with valid data.

    Expected Result:
    - Status code should be 204.

    """

    # Update headers with auth token
    client.headers.update(
        {
            "Authorization": f"Bearer {get_auth_token()}",
        }
    )

    response: Response = client.delete(
        url="/v1/role/1", headers=client.headers
    )
    assert response.status_code == 204
