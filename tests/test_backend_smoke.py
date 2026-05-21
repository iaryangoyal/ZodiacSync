from pathlib import Path

from fastapi.testclient import TestClient


def test_auth_protected_chat_and_frontend(monkeypatch):
    db_path = Path("/private/tmp/zodiac_sync_pytest.db")
    db_path.unlink(missing_ok=True)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_path}")
    monkeypatch.setenv("JWT_SECRET_KEY", "test_secret")

    import src.backend.routes.chat as chat_route
    from src.backend.main import app

    monkeypatch.setattr(chat_route, "retrieve_context", lambda message: [])
    monkeypatch.setattr(chat_route, "generate_response", lambda query, context, history: "mock response")

    with TestClient(app) as client:
        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["auth_configured"] is True

        register = client.post(
            "/auth/register",
            json={
                "email": "test@example.com",
                "full_name": "Test User",
                "password": "password123",
            },
        )
        assert register.status_code == 201

        token = register.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        assert client.get("/auth/me", headers=headers).status_code == 200
        assert client.post("/chat", json={"message": "hello"}).status_code == 401

        chat = client.post("/chat", json={"message": "hello"}, headers=headers)
        assert chat.status_code == 200
        assert chat.json()["response"] == "mock response"
        assert chat.json()["session_id"] == 1

        assert client.get("/app/").status_code == 200
