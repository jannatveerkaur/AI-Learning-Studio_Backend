# 📁 Complete Project Structure

## Directory Tree

```
AI Learning Studio/
│
├── 📄 Core Application Files
│   ├── main.py                      # FastAPI application & API endpoints
│   ├── config.py                    # Centralized configuration management
│   ├── models.py                    # Pydantic models for validation
│   └── utils.py                     # Utility functions
│
├── 🔧 Services (Business Logic)
│   └── services/
│       ├── __init__.py
│       ├── transcript_service.py    # YouTube transcript extraction & cleaning
│       └── openai_service.py        # OpenAI GPT-4o processing
│
├── 🧪 Tests
│   └── tests/
│       ├── __init__.py
│       ├── test_transcript_service.py    # Unit tests for transcript service
│       ├── test_openai_service.py        # Unit tests for OpenAI service
│       └── test_api.py                   # Integration tests for API
│
├── 🐳 Docker Configuration
│   ├── Dockerfile                   # Docker image configuration
│   ├── docker-compose.yml           # Docker Compose orchestration
│   └── .dockerignore                # Docker ignore patterns
│
├── ⚙️ Configuration Files
│   ├── .env.example                 # Environment variables template
│   ├── .gitignore                   # Git ignore patterns
│   ├── pyproject.toml               # Pytest configuration
│   ├── requirements.txt             # Production dependencies
│   └── requirements-dev.txt         # Development dependencies
│
├── 🛠️ Development Tools
│   ├── Makefile                     # Common commands (make run, make test)
│   └── example_client.py            # Example CLI client for testing
│
└── 📚 Documentation
    ├── README.md                    # Main documentation
    ├── QUICKSTART.md                # Quick start guide
    ├── CHANGELOG.md                 # Version history
    ├── LICENSE                      # MIT License
    └── PROJECT_STRUCTURE.md         # This file

```

## File Details

### Core Files

#### [main.py](main.py) - 92 lines
- FastAPI application setup
- API endpoint definitions (`/process-video`, `/health`)
- Request/response handling
- Error handling middleware
- CORS configuration

#### [config.py](config.py) - 44 lines
- Centralized configuration using environment variables
- Settings validation
- Default values for all parameters
- OpenAI, server, and processing configurations

#### [models.py](models.py) - 67 lines
- `VideoRequest` - Input validation for YouTube URLs
- `VideoResponse` - Structured output with summary, key points, quiz
- `QuizQuestion` - Individual quiz question model
- `HealthResponse` - Health check response
- `ErrorResponse` - Error message model

#### [utils.py](utils.py) - 65 lines
- `sanitize_filename()` - Clean filenames for saving
- `format_duration()` - Human-readable time format
- `truncate_text()` - Text truncation utility
- `extract_youtube_id()` - Extract video ID from URLs

### Services

#### [services/transcript_service.py](services/transcript_service.py) - 120 lines
**Responsibilities:**
- Extract video ID from various YouTube URL formats
- Fetch transcripts using `youtube-transcript-api`
- Clean artifacts ([Music], timestamps, etc.)
- Validate transcript length (context window management)
- Get video metadata (title, duration) via YouTube API

**Key Methods:**
- `extract_video_id(url)` - Parse YouTube URLs
- `get_transcript(video_url)` - Fetch and clean transcript
- `_clean_transcript(transcript_list)` - Remove artifacts
- `is_too_long(text)` - Check token limits
- `get_video_metadata(video_id)` - Fetch video info

#### [services/openai_service.py](services/openai_service.py) - 110 lines
**Responsibilities:**
- Process transcripts with OpenAI GPT-4o
- Build strict system prompts for consistent JSON output
- Validate AI responses against schema
- Handle API errors and retries

**Key Methods:**
- `process_transcript(transcript, title)` - Main processing
- `_build_system_prompt()` - Create instruction prompt
- `_build_user_prompt(transcript, title)` - Format input
- `_validate_response(result)` - Validate JSON structure

### Tests

#### [tests/test_transcript_service.py](tests/test_transcript_service.py) - 60 lines
- ✅ Video ID extraction from multiple URL formats
- ✅ Transcript cleaning and validation
- ✅ Length checks for context management
- ✅ Invalid URL handling

#### [tests/test_openai_service.py](tests/test_openai_service.py) - 95 lines
- ✅ Response validation (summary, key points, quiz)
- ✅ Error handling for missing fields
- ✅ Incorrect quiz structure detection
- ✅ Prompt generation testing

#### [tests/test_api.py](tests/test_api.py) - 45 lines
- ✅ Health endpoint functionality
- ✅ URL validation on `/process-video`
- ✅ Error response codes (422, 404, 500)

### Docker

#### [Dockerfile](Dockerfile) - 30 lines
- Base: Python 3.11-slim
- Non-root user for security
- Health check integration
- Optimized layer caching

#### [docker-compose.yml](docker-compose.yml) - 25 lines
- Service orchestration
- Environment variable mapping
- Volume mounting for development
- Network configuration
- Health checks

### Configuration

#### [requirements.txt](requirements.txt) - 8 lines
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-dotenv==1.0.1
pydantic==2.5.3
youtube-transcript-api==0.6.2
openai==1.12.0
google-api-python-client==2.116.0
isodate==0.6.1
```

#### [requirements-dev.txt](requirements-dev.txt) - 3 lines
```
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

#### [.env.example](.env.example)
All configurable environment variables with defaults

### Tools

#### [Makefile](Makefile) - 40 lines
Convenient commands:
- `make install` - Install dependencies
- `make run` - Start server
- `make test` - Run tests
- `make test-cov` - Generate coverage report
- `make clean` - Clean cache files

#### [example_client.py](example_client.py) - 90 lines
CLI tool to test the API with real YouTube videos

## Architecture Overview

```
┌─────────────┐
│   Client    │
│ (Browser/   │
│  CLI/API)   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│        main.py (FastAPI)        │
│  ┌───────────────────────────┐  │
│  │  POST /process-video      │  │
│  │  GET /health              │  │
│  └───────────┬───────────────┘  │
└──────────────┼──────────────────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌─────────────┐ ┌──────────────┐
│ Transcript  │ │   OpenAI     │
│   Service   │ │   Service    │
│             │ │              │
│ • Extract   │ │ • Process    │
│ • Clean     │ │ • Validate   │
│ • Validate  │ │ • Generate   │
└─────────────┘ └──────────────┘
```

## Data Flow

```
1. User Input
   └─> YouTube URL

2. Transcript Extraction
   └─> services/transcript_service.py
       ├─> Extract video ID
       ├─> Fetch transcript
       ├─> Clean text
       └─> Validate length

3. AI Processing
   └─> services/openai_service.py
       ├─> Build prompts
       ├─> Call OpenAI API
       ├─> Parse JSON response
       └─> Validate structure

4. Response
   └─> VideoResponse model
       ├─> summary (3 paragraphs)
       ├─> key_points (5 items)
       └─> quiz (10 questions)
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | FastAPI 0.109.0 |
| **Server** | Uvicorn (ASGI) |
| **AI** | OpenAI GPT-4o |
| **Validation** | Pydantic v2 |
| **Transcript** | youtube-transcript-api |
| **YouTube API** | google-api-python-client |
| **Testing** | Pytest |
| **Containerization** | Docker + Docker Compose |

## Lines of Code Summary

| Component | Files | Lines | Purpose |
|-----------|-------|-------|---------|
| Core | 4 | ~270 | Main app, config, models |
| Services | 2 | ~230 | Business logic |
| Tests | 3 | ~200 | Unit & integration tests |
| Tools | 2 | ~130 | Dev tools & examples |
| Docker | 3 | ~85 | Containerization |
| **Total** | **14** | **~915** | Production code |

## Design Principles

✅ **Separation of Concerns**
- Services handle specific responsibilities
- Models separated from business logic
- Configuration centralized

✅ **Type Safety**
- Pydantic models for validation
- Type hints throughout
- Runtime validation

✅ **Error Handling**
- Comprehensive try-catch blocks
- Meaningful error messages
- HTTP status codes

✅ **Testability**
- Unit tests for each service
- Integration tests for API
- Mock-friendly design

✅ **Configurability**
- Environment-based settings
- Easy customization
- Docker-ready

✅ **Documentation**
- Inline comments
- Docstrings
- Comprehensive README

## Next Steps

- ✅ Core backend complete
- ⬜ Frontend UI (React/Next.js)
- ⬜ Database for caching
- ⬜ User authentication
- ⬜ Rate limiting
- ⬜ Batch processing
- ⬜ Multi-language support

---

**Total Project Files:** 20+  
**Ready for Production:** ✅  
**Docker Ready:** ✅  
**Test Coverage:** 🧪 Comprehensive
