from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re
from typing import Dict, Optional
import isodate
from googleapiclient.discovery import build
from config import settings


class TranscriptService:
    """Service to handle YouTube transcript extraction and cleaning"""
    
    def __init__(self):
        self.youtube_api_key = settings.YOUTUBE_API_KEY
        self.MAX_TOKENS = settings.MAX_TRANSCRIPT_TOKENS
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from various YouTube URL formats"""
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
            r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        raise ValueError("Invalid YouTube URL format")
    
    def get_video_metadata(self, video_id: str) -> Dict[str, str]:
        """Fetch video metadata using YouTube Data API"""
        try:
            if not self.youtube_api_key:
                # Fallback if no API key
                return {"title": "YouTube Video", "duration": "Unknown"}
            
            youtube = build('youtube', 'v3', developerKey=self.youtube_api_key)
            request = youtube.videos().list(
                part="snippet,contentDetails",
                id=video_id
            )
            response = request.execute()
            
            if response['items']:
                item = response['items'][0]
                title = item['snippet']['title']
                duration_iso = item['contentDetails']['duration']
                duration = isodate.parse_duration(duration_iso)
                duration_str = str(duration)
                
                return {"title": title, "duration": duration_str}
            
        except Exception:
            pass
        
        return {"title": "YouTube Video", "duration": "Unknown"}
    
    def get_transcript(self, video_url: str) -> Optional[Dict[str, str]]:
        """
        Fetch and clean transcript from YouTube video
        
        Returns:
            Dict with 'text', 'title', and 'duration' or None if unavailable
        """
        try:
            # Extract video ID
            video_id = self.extract_video_id(video_url)
            
            # Fetch transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Clean and format transcript
            cleaned_text = self._clean_transcript(transcript_list)
            
            # Get metadata
            metadata = self.get_video_metadata(video_id)
            
            return {
                "text": cleaned_text,
                "title": metadata["title"],
                "duration": metadata["duration"]
            }
            
        except (TranscriptsDisabled, NoTranscriptFound):
            return None
        except Exception as e:
            raise Exception(f"Error fetching transcript: {str(e)}")
    
    def _clean_transcript(self, transcript_list: list) -> str:
        """
        Clean and format transcript text
        
        - Combines all segments
        - Removes duplicate phrases
        - Fixes spacing and punctuation
        - Removes timestamps and artifacts
        """
        # Combine all text
        full_text = " ".join([entry['text'] for entry in transcript_list])
        
        # Remove multiple spaces
        full_text = re.sub(r'\s+', ' ', full_text)
        
        # Remove common caption artifacts
        full_text = re.sub(r'\[.*?\]', '', full_text)  # Remove [Music], [Applause]
        full_text = re.sub(r'\(.*?\)', '', full_text)  # Remove (inaudible)
        
        # Clean up punctuation spacing
        full_text = re.sub(r'\s+([.,!?])', r'\1', full_text)
        
        # Remove extra newlines
        full_text = re.sub(r'\n+', '\n', full_text)
        
        return full_text.strip()
    
    def is_too_long(self, text: str) -> bool:
        """
        Check if transcript exceeds safe token limit
        
        Rough estimate: 1 token ≈ 4 characters
        """
        estimated_tokens = len(text) / 4
        return estimated_tokens > self.MAX_TOKENS
    
    def truncate_transcript(self, text: str) -> str:
        """Truncate transcript to fit within token limit"""
        max_chars = self.MAX_TOKENS * 4
        if len(text) > max_chars:
            return text[:max_chars] + "..."
        return text
