"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint returns correct info"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
    
    def test_process_video_invalid_url(self):
        """Test process-video with invalid URL format"""
        response = client.post(
            "/process-video",
            json={"youtube_url": "not-a-valid-url"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_process_video_missing_url(self):
        """Test process-video with missing URL"""
        response = client.post(
            "/process-video",
            json={}
        )
        assert response.status_code == 422  # Validation error
    
    def test_process_video_valid_format(self):
        """Test that valid URL format is accepted (may fail on actual processing)"""
        # This will likely fail during transcript fetch, but URL validation should pass
        response = client.post(
            "/process-video",
            json={"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        )
        # We expect either success or a specific error (404, 500), not validation error (422)
        assert response.status_code in [200, 404, 500, 413]
