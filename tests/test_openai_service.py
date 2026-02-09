"""
Unit tests for OpenAI service
"""
import pytest
from services.openai_service import OpenAIService


class TestOpenAIService:
    """Test cases for OpenAIService"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.service = OpenAIService()
    
    def test_validate_response_valid(self):
        """Test validation of valid response"""
        valid_response = {
            "summary": "Test summary paragraph one.\n\nParagraph two.\n\nParagraph three.",
            "key_points": [
                "Point 1",
                "Point 2",
                "Point 3",
                "Point 4",
                "Point 5"
            ],
            "quiz": [
                {
                    "question": f"Question {i}?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A"
                }
                for i in range(1, 11)
            ]
        }
        
        # Should not raise any exception
        self.service._validate_response(valid_response)
    
    def test_validate_response_missing_summary(self):
        """Test validation fails when summary is missing"""
        invalid_response = {
            "key_points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
            "quiz": []
        }
        
        with pytest.raises(ValueError, match="Missing required key: summary"):
            self.service._validate_response(invalid_response)
    
    def test_validate_response_wrong_key_points_count(self):
        """Test validation fails with wrong number of key points"""
        invalid_response = {
            "summary": "Summary",
            "key_points": ["Point 1", "Point 2", "Point 3"],  # Only 3 instead of 5
            "quiz": []
        }
        
        with pytest.raises(ValueError, match="key_points must be a list of exactly 5 items"):
            self.service._validate_response(invalid_response)
    
    def test_validate_response_wrong_quiz_count(self):
        """Test validation fails with wrong number of quiz questions"""
        invalid_response = {
            "summary": "Summary",
            "key_points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
            "quiz": [
                {
                    "question": "Q1?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "A"
                }
            ]  # Only 1 instead of 10
        }
        
        with pytest.raises(ValueError, match="quiz must be a list of exactly 10 questions"):
            self.service._validate_response(invalid_response)
    
    def test_validate_response_invalid_quiz_structure(self):
        """Test validation fails with invalid quiz question structure"""
        invalid_response = {
            "summary": "Summary",
            "key_points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
            "quiz": [
                {
                    "question": "Q?",
                    "options": ["A", "B"],  # Only 2 options instead of 4
                    "correct_answer": "A"
                }
                for _ in range(10)
            ]
        }
        
        with pytest.raises(ValueError, match="must have exactly 4 options"):
            self.service._validate_response(invalid_response)
    
    def test_validate_response_incorrect_answer(self):
        """Test validation fails when correct_answer not in options"""
        invalid_response = {
            "summary": "Summary",
            "key_points": ["Point 1", "Point 2", "Point 3", "Point 4", "Point 5"],
            "quiz": [
                {
                    "question": "Q?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "E"  # Not in options
                }
                for _ in range(10)
            ]
        }
        
        with pytest.raises(ValueError, match="correct_answer must be one of the options"):
            self.service._validate_response(invalid_response)
    
    def test_build_system_prompt(self):
        """Test system prompt generation"""
        prompt = self.service._build_system_prompt()
        
        assert "JSON" in prompt
        assert "summary" in prompt
        assert "key_points" in prompt
        assert "quiz" in prompt
        assert "10" in prompt  # 10 questions
        assert "5" in prompt   # 5 key points
    
    def test_build_user_prompt(self):
        """Test user prompt generation"""
        transcript = "This is a test transcript"
        title = "Test Video"
        
        prompt = self.service._build_user_prompt(transcript, title)
        
        assert "Test Video" in prompt
        assert "This is a test transcript" in prompt
