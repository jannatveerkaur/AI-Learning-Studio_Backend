from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models import VideoRequest, TranscriptRequest, VideoResponse, HealthResponse, QuizQuestion
from services.transcript_service import TranscriptService
from services.openai_service import OpenAIService

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# CORS middleware - Allow all origins for deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
transcript_service = TranscriptService()
openai_service = OpenAIService()

@app.get("/")
async def root():
    """API root endpoint"""
    return {"message": "Smart Video Learning Tool API", "status": "running"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy", "service": settings.APP_NAME}

@app.post("/process-transcript", response_model=VideoResponse)
async def process_transcript(request: TranscriptRequest):
    """
    Process a video transcript directly to generate:
    - A 3-paragraph summary
    - 5 key points
    - 10 multiple-choice quiz questions
    """
    try:
        # Validate transcript length
        if len(request.transcript) < 100:
            raise HTTPException(
                status_code=400,
                detail="Transcript is too short. Please provide at least 100 characters."
            )
        
        if len(request.transcript) > 50000:
            raise HTTPException(
                status_code=413,
                detail="Transcript is too long. Please provide a shorter transcript (max 50,000 characters)."
            )
        
        # Process with Groq (synchronous)
        ai_result = openai_service.process_transcript(
            request.transcript,
            request.video_title
        )
        
        # Build response
        return VideoResponse(
            summary=ai_result["summary"],
            key_points=ai_result["key_points"],
            notes=ai_result["notes"],
            quiz=[
                QuizQuestion(
                    question=q["question"],
                    options=q["options"],
                    correct_answer=q["correct_answer"]
                )
                for q in ai_result["quiz"]
            ],
            video_title=request.video_title,
            duration="N/A"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing transcript: {str(e)}"
        )

@app.post("/process-video", response_model=VideoResponse)
async def process_video(request: VideoRequest):
    """
    Process a YouTube video to generate:
    - A 3-paragraph summary
    - 5 key points
    - 10 multiple-choice quiz questions
    """
    try:
        # Extract video ID from URL
        video_url = str(request.youtube_url)
        
        # Step 1: Fetch and clean transcript
        transcript_data = transcript_service.get_transcript(video_url)
        
        if not transcript_data:
            raise HTTPException(
                status_code=404,
                detail="Unable to fetch transcript. Video may not have captions or is unavailable."
            )
        
        # Step 2: Check transcript length (context window management)
        if transcript_service.is_too_long(transcript_data["text"]):
            raise HTTPException(
                status_code=413,
                detail="Video is too long. Please try a video under 60 minutes."
            )
        
        # Step 3: Process with Groq
        ai_result = openai_service.process_transcript(
            transcript_data["text"],
            transcript_data["title"]
        )
        
        # Step 4: Build response
        return VideoResponse(
            summary=ai_result["summary"],
            key_points=ai_result["key_points"],
            notes=ai_result["notes"],
            quiz=[
                QuizQuestion(
                    question=q["question"],
                    options=q["options"],
                    correct_answer=q["correct_answer"]
                )
                for q in ai_result["quiz"]
            ],
            video_title=transcript_data["title"],
            duration=transcript_data["duration"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing video: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
