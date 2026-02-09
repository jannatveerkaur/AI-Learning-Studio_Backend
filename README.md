# Smart Video Learning Tool

A powerful FastAPI backend that transforms YouTube videos into structured learning materials using OpenAI's GPT-4o.

## 🚀 Features

- **Transcript Extraction**: Automatically fetches YouTube video transcripts
- **AI-Powered Analysis**: Generates comprehensive summaries using GPT-4o
- **Key Concepts**: Extracts 5 most important takeaways
- **Interactive Quizzes**: Creates 10 multiple-choice questions to test understanding
- **Context Management**: Handles long videos with smart truncation
- **Error Handling**: Robust validation for missing transcripts and API errors

## 📁 Project Structure

```
AI Learning Studio/
├── main.py                          # FastAPI application & API endpoints
├── config.py                        # Centralized configuration settings
├── models.py                        # Pydantic models for validation
├── services/
│   ├── __init__.py
│   ├── transcript_service.py        # YouTube transcript extraction & cleaning
│   └── openai_service.py            # OpenAI GPT-4o processing logic
├── tests/
│   ├── __init__.py
│   ├── test_transcript_service.py   # Unit tests for transcript service
│   ├── test_openai_service.py       # Unit tests for OpenAI service
│   └── test_api.py                  # Integration tests for API endpoints
├── example_client.py                # Example CLI client for testing
├── requirements.txt                 # Production dependencies
├── requirements-dev.txt             # Development & testing dependencies
├── pyproject.toml                   # Pytest configuration
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore patterns
└── README.md                        # This file
```

## 🛠️ Setup Instructions

### 1. Prerequisites

- Python 3.9 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- (Optional) YouTube Data API key for enhanced metadata

### 2. Installation

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# REQUIRED:
OPENAI_API_KEY=sk-...

# OPTIONAL (for better video metadata):
YOUTUBE_API_KEY=AIza...
```

### 4. Run the Server

**Option 1: Direct Python**
```bash
# Development mode with auto-reload
uvicorn main:app --reload

# Production mode
python main.py

# Using make command
make run
```

**Option 2: Docker**
```bash
# Build and run with docker-compose
docker-compose up --build

# Run in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

The API will be available at: **http://localhost:8000**

## 📚 API Documentation

### Interactive Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Endpoints

#### `POST /process-video`

Process a YouTube video and generate learning materials.

**Request Body:**
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "summary": "Three-paragraph summary of the video...",
  "key_points": [
    "First key concept",
    "Second key concept",
    "Third key concept",
    "Fourth key concept",
    "Fifth key concept"
  ],
  "quiz": [
    {
      "question": "What is the main topic?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A"
    }
    // ... 9 more questions
  ],
  "video_title": "Video Title",
  "duration": "0:15:30"
}
```

**Error Responses:**
- `404`: Transcript unavailable (no captions)
- `413`: Video too long (>60 minutes)
- `500`: Processing error

#### `GET /health`

Check API health status.

## 🔧 Configuration

### Environment Variables

All configuration is managed through [config.py](config.py) and can be customized via environment variables:

- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `YOUTUBE_API_KEY` - YouTube Data API key (optional)
- `OPENAI_MODEL` - Model to use (default: "gpt-4o")
- `OPENAI_TEMPERATURE` - Temperature for responses (default: 0.7)
- `MAX_TRANSCRIPT_TOKENS` - Max transcript length (default: 12000)
- `HOST` - Server host (default: "0.0.0.0")
- `PORT` - Server port (default: 8000)
- `CORS_ORIGINS` - Allowed CORS origins (default: "*")

### Transcript Length Limits

By default, videos are limited to ~12,000 tokens (~48,000 characters) to fit within GPT-4o's context window.

Modify in [config.py](config.py) or set environment variable:
```bash
MAX_TRANSCRIPT_TOKENS=15000
```

### OpenAI Model

Using GPT-4o by default. Switch to GPT-4o-mini for faster/cheaper processing:

```bash
OPENAI_MODEL=gpt-4o-mini
```

## 🧪 Testing

### Example cURL Request

```bash
curl -X POST "http://localhost:8000/process-video" \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }'
```

### Example Python Client

Use the included example client:

```bash
# Basic usage
python example_client.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Custom API URL
python example_client.py "https://www.youtube.com/watch?v=VIDEO_ID" "http://localhost:8000"
```

Or use the requests library directly:

```python
import requests

response = requests.post(
    "http://localhost:8000/process-video",
    json={"youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"}
)

data = response.json()
print(f"Summary: {data['summary']}")
print(f"Quiz Questions: {len(data['quiz'])}")
```

## 🧪 Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=services --cov=. --cov-report=html

# Run specific test file
pytest tests/test_transcript_service.py

# Run with verbose output
pytest -v
```

## 🎯 Use Cases

- **Students**: Generate study materials from lecture videos
- **Educators**: Create quizzes from educational content
- **Content Creators**: Analyze and summarize video content
- **Researchers**: Extract key insights from conference talks

## ⚠️ Limitations

- Requires videos to have captions/subtitles
- Max video length: ~60 minutes (configurable)
- Rate limited by OpenAI API quotas
- English transcripts work best (multilingual support varies)

## 🔐 Security Notes

- Never commit `.env` file to version control
- Use environment variables for all API keys
- Consider rate limiting in production
- Implement authentication for public deployments

## 📝 License

MIT License - Feel free to use and modify as needed!

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Frontend UI (React/Next.js)
- Database integration for caching results
- Support for multiple languages
- Batch processing of playlists
- Export to PDF/Markdown

---

**Built with FastAPI + OpenAI GPT-4o** 🚀
