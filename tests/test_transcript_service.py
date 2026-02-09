"""
Unit tests for transcript service
"""
import pytest
from services.transcript_service import TranscriptService


class TestTranscriptService:
    """Test cases for TranscriptService"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = TranscriptService()
    
    def test_extract_video_id_standard_url(self):
        """Test video ID extraction from standard YouTube URL"""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video_id = self.service.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_short_url(self):
        """Test video ID extraction from short YouTube URL"""
        url = "https://youtu.be/dQw4w9WgXcQ"
        video_id = self.service.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_embed_url(self):
        """Test video ID extraction from embed URL"""
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        video_id = self.service.extract_video_id(url)
        assert video_id == "dQw4w9WgXcQ"
    
    def test_extract_video_id_invalid_url(self):
        """Test that invalid URL raises ValueError"""
        url = "https://example.com/video"
        with pytest.raises(ValueError, match="Invalid YouTube URL format"):
            self.service.extract_video_id(url)
    
    def test_clean_transcript(self):
        """Test transcript cleaning"""
        transcript = [
            {"text": "[Music]"},
            {"text": "Hello   world"},
            {"text": "(inaudible)"},
            {"text": "Test  content"}
        ]
        cleaned = self.service._clean_transcript(transcript)
        assert "[Music]" not in cleaned
        assert "(inaudible)" not in cleaned
        assert "Hello world" in cleaned
        assert "  " not in cleaned  # No double spaces
    
    def test_is_too_long(self):
        """Test transcript length validation"""
        short_text = "a" * 1000
        long_text = "a" * 50000
        
        assert not self.service.is_too_long(short_text)
        assert self.service.is_too_long(long_text)
    
    def test_truncate_transcript(self):
        """Test transcript truncation"""
        long_text = "a" * 100000
        truncated = self.service.truncate_transcript(long_text)
        
        assert len(truncated) <= self.service.MAX_TOKENS * 4
        assert truncated.endswith("...")
