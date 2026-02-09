"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, HttpUrl
from typing import List


class VideoRequest(BaseModel):
    """Request model for video processing"""
    youtube_url: HttpUrl
    
    class Config:
        json_schema_extra = {
            "example": {
                "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        }


class TranscriptRequest(BaseModel):
    """Request model for direct transcript processing"""
    transcript: str
    video_title: str = "Video Learning Materials"
    
    class Config:
        json_schema_extra = {
            "example": {
                "transcript": "This is a sample video transcript about machine learning...",
                "video_title": "Introduction to Machine Learning"
            }
        }


class QuizQuestion(BaseModel):
    """Model for a single quiz question"""
    question: str
    options: List[str]
    correct_answer: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is the main topic of this video?",
                "options": ["Machine Learning", "Web Development", "Data Science", "Cloud Computing"],
                "correct_answer": "Machine Learning"
            }
        }


class VideoResponse(BaseModel):
    """Response model for processed video"""
    summary: str
    key_points: List[str]
    notes: List[str]
    quiz: List[QuizQuestion]
    video_title: str
    duration: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary": "This video provides an introduction to machine learning...",
                "key_points": [
                    "Machine learning is a subset of AI",
                    "Supervised learning uses labeled data",
                    "Neural networks mimic brain structure",
                    "Feature engineering is crucial",
                    "Model validation prevents overfitting"
                ],
                "notes": [
                    "Machine learning enables computers to learn from data without explicit programming",
                    "The three main types are supervised, unsupervised, and reinforcement learning",
                    "Common algorithms include decision trees, neural networks, and support vector machines",
                    "Data preprocessing and feature selection are critical steps in the ML pipeline",
                    "Model evaluation metrics vary based on the problem type (classification vs regression)",
                    "Overfitting occurs when a model performs well on training data but poorly on new data",
                    "Cross-validation helps assess model performance on unseen data"
                ],
                "quiz": [
                    {
                        "question": "What is machine learning?",
                        "options": ["A type of AI", "A database", "A programming language", "An operating system"],
                        "correct_answer": "A type of AI"
                    }
                ],
                "video_title": "Introduction to Machine Learning",
                "duration": "0:15:30"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str


class ErrorResponse(BaseModel):
    """Error response model"""
    detail: str
