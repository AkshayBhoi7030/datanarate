import pytest
from uuid import uuid4
from app.models.audit_log import AuditAction


def test_get_saved_queries(client):
    response = client.get("/api/v1/saved-queries")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


def test_create_saved_query(client):
    response = client.post("/api/v1/saved-queries", json={
        "name": "Monthly Revenue",
        "description": "Get monthly revenue",
        "natural_language_query": "Show me monthly revenue",
        "generated_sql": "SELECT * FROM orders",
        "tags": ["revenue", "monthly"]
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Monthly Revenue"


def test_update_saved_query(client):
    # First create
    create_response = client.post("/api/v1/saved-queries", json={
        "name": "Test Query",
        "natural_language_query": "Test",
        "generated_sql": "SELECT 1"
    })
    query_id = create_response.json()["data"]["id"]
    
    # Then update
    update_response = client.put(f"/api/v1/saved-queries/{query_id}", json={
        "name": "Updated Query"
    })
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Updated Query"


def test_toggle_favorite(client):
    create_response = client.post("/api/v1/saved-queries", json={
        "name": "Test Query",
        "natural_language_query": "Test",
        "generated_sql": "SELECT 1"
    })
    query_id = create_response.json()["data"]["id"]
    
    toggle_response = client.patch(f"/api/v1/saved-queries/{query_id}/favorite")
    assert toggle_response.status_code == 200
    data = toggle_response.json()
    assert data["success"] is True
    assert data["data"]["is_favorite"] is True


def test_delete_saved_query(client):
    create_response = client.post("/api/v1/saved-queries", json={
        "name": "Test Query",
        "natural_language_query": "Test",
        "generated_sql": "SELECT 1"
    })
    query_id = create_response.json()["data"]["id"]
    
    delete_response = client.delete(f"/api/v1/saved-queries/{query_id}")
    assert delete_response.status_code == 200


def test_get_query_history(client):
    response = client.get("/api/v1/history")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


def test_create_query_history(client):
    response = client.post("/api/v1/history", json={
        "database_connection_id": str(uuid4()),
        "natural_language_query": "Show me data",
        "generated_sql": "SELECT * FROM table",
        "execution_time_ms": 100,
        "row_count": 5,
        "success": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_delete_query_history(client):
    create_response = client.post("/api/v1/history", json={
        "database_connection_id": str(uuid4()),
        "natural_language_query": "Show me data",
        "generated_sql": "SELECT * FROM table"
    })
    history_id = create_response.json()["data"]["id"]
    
    delete_response = client.delete(f"/api/v1/history/{history_id}")
    assert delete_response.status_code == 200


def test_get_audit_logs(client):
    response = client.get("/api/v1/audit-logs")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


def test_create_audit_log(client):
    response = client.post("/api/v1/audit-logs", json={
        "action": AuditAction.LOGIN.value,
        "ip_address": "127.0.0.1",
        "user_agent": "Test Agent"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_get_preferences(client):
    response = client.get("/api/v1/preferences")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "theme" in data["data"]


def test_update_preferences(client):
    response = client.put("/api/v1/preferences", json={
        "theme": "dark",
        "preferred_chart_type": "pie"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["theme"] == "dark"


def test_export_csv(client):
    response = client.post("/api/v1/exports/csv", json={
        "data": [{"name": "John", "age": 30}],
        "filename": "test.csv"
    })
    assert response.status_code == 200


def test_export_excel(client):
    response = client.post("/api/v1/exports/excel", json={
        "data": [{"name": "John", "age": 30}],
        "filename": "test.xlsx"
    })
    assert response.status_code == 200


def test_export_pdf(client):
    response = client.post("/api/v1/exports/pdf", json={
        "data": [{"name": "John", "age": 30}],
        "question": "Who is John?",
        "sql": "SELECT * FROM users",
        "insight": "John is 30 years old",
        "filename": "test.pdf"
    })
    assert response.status_code == 200
