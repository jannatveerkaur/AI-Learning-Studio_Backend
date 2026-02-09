# Quick Start Guide

Get your Smart Video Learning Tool up and running in 5 minutes! 🚀

## Prerequisites
- Python 3.9+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

## Installation (3 steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env  # or use your preferred editor
```

Add your key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Start the Server
```bash
uvicorn main:app --reload
```

✅ **That's it!** Your API is running at http://localhost:8000

## Test It

### Option 1: Interactive API Docs
Visit http://localhost:8000/docs

### Option 2: Example Client
```bash
python example_client.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

### Option 3: cURL
```bash
curl -X POST "http://localhost:8000/process-video" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

## Docker Alternative

If you prefer Docker:

```bash
# 1. Configure .env file (same as above)
cp .env.example .env

# 2. Run with docker-compose
docker-compose up --build
```

## Next Steps

- Check the [README.md](README.md) for detailed documentation
- Run tests: `pytest`
- Customize settings in [config.py](config.py)
- Explore API endpoints at http://localhost:8000/docs

## Common Issues

**"OPENAI_API_KEY environment variable is required"**
- Make sure you created `.env` file and added your API key

**"Unable to fetch transcript"**
- Video must have captions/subtitles enabled
- Try a different video

**"Video too long"**
- Videos are limited to ~60 minutes by default
- Adjust `MAX_TRANSCRIPT_TOKENS` in .env

## Support

For detailed information, see [README.md](README.md)

---
Happy learning! 🎓
