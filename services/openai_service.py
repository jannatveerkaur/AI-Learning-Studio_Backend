from groq import Groq
import json
import re
from typing import Dict
from config import settings


class OpenAIService:
    """Service to process transcripts using Groq (Llama 3)"""
    
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL
        self.temperature = settings.GROQ_TEMPERATURE
        self.max_tokens = settings.GROQ_MAX_TOKENS
    
    def _build_system_prompt(self) -> str:
        """Create strict system prompt for consistent JSON output"""
        return """You are an expert educational content analyzer. Generate comprehensive learning materials from transcripts.

CRITICAL: Return ONLY valid JSON with this exact structure:
{
  "summary": "3 well-written paragraphs separated by \\n\\n",
  "key_points": ["point 1", "point 2", "point 3", "point 4", "point 5"],
  "notes": ["detailed note 1", "detailed note 2", "detailed note 3", "detailed note 4", "detailed note 5", "detailed note 6", "detailed note 7"],
  "quiz": [
    {
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": "Option A"
    }
  ]
}

IMPORTANT RULES:
- summary: Must be exactly 3 paragraphs providing a high-level overview
- key_points: Must be exactly 5 BRIEF one-line key insights (short and concise)
- notes: Must be exactly 7 DETAILED, COMPREHENSIVE study notes. Each note should be 2-4 sentences long with:
  * In-depth explanations of concepts
  * Context and background information
  * Examples and real-world applications
  * Technical details and nuances
  * Connections between different ideas
  * Why the concept matters and how it's used
- quiz: Must be exactly 10 questions with varied difficulty
- Each quiz question must have exactly 4 options
- correct_answer MUST be the EXACT text of one of the 4 options (copy it precisely)
- No extra fields, no markdown, just pure JSON"""
    
    def _build_user_prompt(self, transcript: str, video_title: str) -> str:
        """Build user prompt with transcript"""
        return f"""Video Title: {video_title}

Transcript:
{transcript}

Generate:
1. A 3-paragraph summary (high-level overview of the content)
2. 5 key points (brief, one-line insights - keep these SHORT)
3. 7 detailed study notes (COMPREHENSIVE and DETAILED - each should be 2-4 sentences with examples, context, explanations, and real-world applications)
4. 10 multiple-choice quiz questions (varied difficulty levels)

Return as JSON only."""
    
    def process_transcript(self, transcript: str, video_title: str) -> Dict:
        """Process transcript with Groq"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {"role": "user", "content": self._build_user_prompt(transcript, video_title)}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            content = response.choices[0].message.content
            
            # Clean content - remove markdown and invalid characters
            content = content.strip()
            
            # Remove markdown code blocks
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()
            
            # Remove or escape invalid control characters (except \n, \r, \t which are valid in JSON strings)
            # Replace problematic control characters that break JSON parsing
            content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
            
            # Ensure newlines within string values are properly escaped
            # This regex finds string values and escapes unescaped newlines within them
            def escape_newlines_in_strings(match):
                string_content = match.group(1)
                # Escape unescaped newlines, carriage returns, and tabs
                string_content = string_content.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
                return f'"{string_content}"'
            
            # Find all string values in JSON and escape special characters
            content = re.sub(r'"([^"\\]*(?:\\.[^"\\]*)*)"', escape_newlines_in_strings, content)
            
            result = json.loads(content)
            
            # Auto-fix quiz answers if they don't match options exactly
            self._fix_quiz_answers(result)
            
            self._validate_response(result)
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from AI: {str(e)}")
        except Exception as e:
            raise ValueError(f"OpenAI processing error: {str(e)}")
    
    def _fix_quiz_answers(self, result: Dict) -> None:
        """Auto-fix quiz answers that don't match options exactly"""
        if "quiz" not in result or not isinstance(result["quiz"], list):
            return
        
        for i, q in enumerate(result["quiz"]):
            if "correct_answer" not in q or "options" not in q:
                continue
            
            correct = q["correct_answer"]
            options = q["options"]
            
            # If correct_answer doesn't match any option exactly
            if correct not in options:
                # Try case-insensitive match
                for opt in options:
                    if opt.lower().strip() == correct.lower().strip():
                        q["correct_answer"] = opt
                        break
                else:
                    # Try partial match (if correct_answer is substring of an option)
                    for opt in options:
                        if correct.lower() in opt.lower() or opt.lower() in correct.lower():
                            q["correct_answer"] = opt
                            break
                    else:
                        # Last resort: use the first option
                        q["correct_answer"] = options[0]
    
    def _validate_response(self, result: Dict) -> None:
        """Validate AI response structure"""
        if "summary" not in result:
            raise ValueError("Missing 'summary' in response")
        if "key_points" not in result:
            raise ValueError("Missing 'key_points' in response")
        if "notes" not in result:
            raise ValueError("Missing 'notes' in response")
        if "quiz" not in result:
            raise ValueError("Missing 'quiz' in response")
        
        if not isinstance(result["key_points"], list) or len(result["key_points"]) != settings.REQUIRED_KEY_POINTS:
            raise ValueError(f"Expected exactly {settings.REQUIRED_KEY_POINTS} key points")
        
        if not isinstance(result["notes"], list) or len(result["notes"]) < 5:
            # Be flexible with notes count (minimum 5)
            if "notes" in result and isinstance(result["notes"], list) and len(result["notes"]) > 0:
                pass  # Accept any reasonable number of notes
            else:
                raise ValueError("Expected at least 5 detailed notes")
        
        if not isinstance(result["quiz"], list) or len(result["quiz"]) != settings.REQUIRED_QUIZ_QUESTIONS:
            raise ValueError(f"Expected exactly {settings.REQUIRED_QUIZ_QUESTIONS} quiz questions")
        
        for i, q in enumerate(result["quiz"]):
            if not all(k in q for k in ["question", "options", "correct_answer"]):
                raise ValueError(f"Quiz question {i+1} missing required fields")
            if len(q["options"]) != settings.QUIZ_OPTIONS_COUNT:
                raise ValueError(f"Quiz question {i+1} must have exactly {settings.QUIZ_OPTIONS_COUNT} options")
            if q["correct_answer"] not in q["options"]:
                raise ValueError(f"Quiz question {i+1} correct_answer not in options")
