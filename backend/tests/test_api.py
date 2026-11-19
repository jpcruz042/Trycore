import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.mark.asyncio
async def test_project_and_activity_transactions():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        health = await client.get("/health")
        assert health.status_code == 200

        project_response = await client.post("/projects", json={
            "name": "API Test Project",
            "description": "Integration test",
        })
        assert project_response.status_code == 201
        project_id = project_response.json()["id"]

        list_projects = await client.get("/projects")
        assert list_projects.status_code == 200

        get_project = await client.get(f"/projects/{project_id}")
        assert get_project.status_code == 200

        updated_project = await client.put(f"/projects/{project_id}", json={
            "name": "API Test Project Updated",
        })
        assert updated_project.status_code == 200

        activity_response = await client.post(f"/projects/{project_id}/activities", json={
            "name": "Design",
            "bac": 10000,
            "planned_progress": 60,
            "actual_progress": 50,
            "actual_cost": 7000,
        })
        assert activity_response.status_code == 201
        activity_id = activity_response.json()["id"]

        list_activities = await client.get(f"/projects/{project_id}/activities")
        assert list_activities.status_code == 200

        get_activity = await client.get(f"/projects/{project_id}/activities/{activity_id}")
        assert get_activity.status_code == 200

        updated_activity = await client.put(f"/projects/{project_id}/activities/{activity_id}", json={
            "actual_progress": 55,
            "actual_cost": 6500,
        })
        assert updated_activity.status_code == 200

        evm_response = await client.get(f"/projects/{project_id}/evm")
        assert evm_response.status_code == 200
        assert evm_response.json()["indicators"]["cpi_status"] == "over_budget"

        deleted_activity = await client.delete(f"/projects/{project_id}/activities/{activity_id}")
        assert deleted_activity.status_code == 204

        deleted_project = await client.delete(f"/projects/{project_id}")
        assert deleted_project.status_code == 204
