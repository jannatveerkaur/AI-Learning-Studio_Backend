# API Documentation

Complete API reference for the Smart Video Learning Tool.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, no authentication is required. For production deployment, consider adding:
- API keys
- JWT tokens
- OAuth 2.0

---

## Endpoints

### 1. Root Endpoint

**GET** `/`

Get API information and available endpoints.

**Response 200**
```json
{
  "message": "Smart Video Learning Tool API",
  "endpoints": {
    "process_video": "/process-video (POST)",
    "health": "/health (GET)"
  }
}
```

---

### 2. Health Check

**GET** `/health`

Check API health status.

**Response 200**
```json
{
  "status": "healthy",
  "service": "Smart Video Learning Tool"
}
```

---

### 3. Process Video ⭐

**POST** `/process-video`

Process a YouTube video and generate learning materials.

#### Request Body

```json
{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Fields:**
- `youtube_url` (string, required): Valid YouTube URL

**Accepted URL Formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

#### Success Response 200

```json
{
  "summary": "This is a comprehensive three-paragraph summary...\n\nSecond paragraph continues the discussion...\n\nThird paragraph concludes the summary.",
  "key_points": [
    "First important concept from the video",
    "Second key takeaway or learning point",
    "Third critical insight discussed",
    "Fourth major topic or principle",
    "Fifth essential understanding"
  ],
  "quiz": [
    {
      "question": "What is the main topic discussed in the video?",
      "options": [
        "Machine Learning",
        "Web Development",
        "Data Science",
        "Cloud Computing"
      ],
      "correct_answer": "Machine Learning"
    },
    // ... 9 more questions
  ],
  "video_title": "Introduction to Machine Learning",
  "duration": "0:15:30"
}
```

**Response Fields:**
- `summary` (string): 3-paragraph summary of video content
- `key_points` (array[string]): Exactly 5 key concepts
- `quiz` (array[object]): Exactly 10 quiz questions
  - `question` (string): The question text
  - `options` (array[string]): 4 possible answers
  - `correct_answer` (string): The correct option
- `video_title` (string): Title of the YouTube video
- `duration` (string): Video length (HH:MM:SS or MM:SS)

#### Error Responses

**404 - Transcript Not Available**
```json
{
  "detail": "Unable to fetch transcript. Video may not have captions or is unavailable."
}
```

**Causes:**
- Video has no captions/subtitles
- Captions are disabled
- Video is private/deleted
- Invalid video ID

**413 - Video Too Long**
```json
{
  "detail": "Video is too long. Please try a video under 60 minutes."
}
```

**Causes:**
- Video transcript exceeds token limit (default: 12,000 tokens)
- Approximately videos over 60 minutes

**422 - Validation Error**
```json
{
  "detail": [
    {
      "loc": ["body", "youtube_url"],
      "msg": "invalid or missing URL scheme",
      "type": "value_error.url.scheme"
    }
  ]
}
```

**Causes:**
- Invalid URL format
- Missing `youtube_url` field
- Not a valid YouTube URL

**500 - Server Error**
```json
{
  "detail": "Error processing video: [error message]"
}
```

**Causes:**
- OpenAI API error
- Network issues
- Invalid API key
- Rate limiting

---

## Examples

### cURL

```bash
curl -X POST "http://localhost:8000/process-video" \
  -H "Content-Type: application/json" \
  -d '{
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }'
```

### Python (requests)

```python
import requests

url = "http://localhost:8000/process-video"
payload = {
    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Summary: {data['summary']}")
print(f"Quiz: {len(data['quiz'])} questions")
```

### JavaScript (fetch)

```javascript
const url = 'http://localhost:8000/process-video';
const data = {
  youtube_url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
};

fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
.then(response => response.json())
.then(data => {
  console.log('Summary:', data.summary);
  console.log('Quiz:', data.quiz);
})
.catch(error => console.error('Error:', error));
```

### Python (CLI Example)

```python
python example_client.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

---

## Rate Limits

Currently no rate limiting is implemented. For production:

**Recommended Limits:**
- 10 requests per minute per IP
- 100 requests per hour per IP
- Consider implementing with libraries like `slowapi`

---

## CORS

CORS is enabled for all origins by default (`*`).

**Production Configuration:**
Update `CORS_ORIGINS` in `.env`:
```
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

---

## Response Times

**Typical Processing Times:**
- Transcript extraction: 2-5 seconds
- OpenAI processing: 10-30 seconds
- **Total:** 15-35 seconds

**Factors affecting speed:**
- Video length
- Transcript complexity
- OpenAI API load
- Network latency

---

## Error Handling Best Practices

### Client-Side

```python
try:
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out. Video may be too long.")
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("No transcript available for this video.")
    elif e.response.status_code == 413:
        print("Video is too long. Try a shorter one.")
    else:
        print(f"Error: {e.response.json()['detail']}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

---

## OpenAPI/Swagger Documentation

Interactive API documentation is available at:

**Swagger UI:**  
http://localhost:8000/docs

**ReDoc:**  
http://localhost:8000/redoc

**OpenAPI JSON:**  
http://localhost:8000/openapi.json

---

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 404 | Not Found | Transcript unavailable |
| 413 | Payload Too Large | Video too long |
| 422 | Unprocessable Entity | Validation error |
| 500 | Internal Server Error | Server/API error |

---

## Testing

### Using Swagger UI

1. Navigate to http://localhost:8000/docs
2. Click on `/process-video` endpoint
3. Click "Try it out"
4. Enter a YouTube URL
5. Click "Execute"
6. View response

### Using Example Client

```bash
# Test with a valid video
python example_client.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Test with different API URL
python example_client.py "VIDEO_URL" "http://production-server:8000"
```

---

## Webhooks (Future)

Not currently implemented. Future versions may support:
- Webhook callbacks when processing completes
- Async processing with job IDs
- Server-Sent Events for progress updates

---

## Versioning

Current Version: **v1.0.0**

Future versions will use URL versioning:
- `/v1/process-video`
- `/v2/process-video`

---

## Support

For issues or questions:
- Check the [README.md](README.md)
- Review [QUICKSTART.md](QUICKSTART.md)
- See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

---

**Last Updated:** February 9, 2026  
**API Version:** 1.0.0
