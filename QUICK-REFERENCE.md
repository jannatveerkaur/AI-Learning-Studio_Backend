# 🎯 Quick Reference Card

## One-Command Start

```bash
./start.sh
```

This starts both backend and frontend automatically!

---

## Individual Commands

### Backend Only
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Only
```bash
cd frontend
npm start
```

---

## URLs

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Interactive Swagger UI |
| **Legacy UI** | http://localhost:8000 | Old HTML interface |

---

## Common Tasks

### Install Dependencies

```bash
# Backend
pip install --break-system-packages -r requirements.txt

# Frontend
cd frontend && npm install
```

### Configure API Key

```bash
echo 'OPENAI_API_KEY=your-key' > .env
```

### Build for Production

```bash
# Frontend
cd frontend
npm run build
```

### Run Tests

```bash
# Backend
pytest tests/

# Frontend
cd frontend
npm test
```

---

## File Locations

| What | Where |
|------|-------|
| **Frontend Code** | `frontend/src/` |
| **Backend API** | `main.py` |
| **Services** | `services/` |
| **Models** | `models.py` |
| **Config** | `config.py` |
| **Environment** | `.env` |

---

## Key Features

### Frontend (React)
- ✅ Landing page with glassmorphism
- ✅ Authentication UI (Login/Signup)
- ✅ Dashboard with stats
- ✅ Learning workspace (3 tabs)
- ✅ Dark/Light mode
- ✅ Fully responsive

### Backend (FastAPI)
- ✅ YouTube transcript extraction
- ✅ Direct transcript input
- ✅ GPT-4o AI processing
- ✅ Auto-generated summaries
- ✅ 5 key insights
- ✅ 10-question quizzes

---

## Input Modes

### 1. YouTube URL
```
https://www.youtube.com/watch?v=xxxxx
```

### 2. Paste Transcript
```
Minimum 100 characters
Maximum 50,000 characters
```

---

## API Endpoints

### Process Video
```bash
POST /process-video
{
  "youtube_url": "https://youtube.com/watch?v=..."
}
```

### Process Transcript
```bash
POST /process-transcript
{
  "transcript": "Your transcript here...",
  "video_title": "Optional Title"
}
```

### Health Check
```bash
GET /health
```

---

## Output Format

All requests return:

```json
{
  "video_title": "String",
  "summary": "3-paragraph text",
  "key_points": ["Point 1", "Point 2", ...],
  "quiz": [
    {
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "correct_answer": "Correct option"
    }
  ],
  "duration": "Optional duration"
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Port 8000 in use** | `lsof -i :8000` then `kill -9 <PID>` |
| **Port 3000 in use** | `PORT=3001 npm start` |
| **Module not found** | Reinstall dependencies |
| **API key error** | Check `.env` file |
| **CORS error** | Backend must be running |

---

## Tech Stack

**Frontend:**
- React 18.2
- Tailwind CSS 3
- React Router 6
- Axios
- Lucide Icons

**Backend:**
- FastAPI 0.109
- OpenAI 2.17 (GPT-4o)
- Pydantic 2.5
- Uvicorn 0.27

---

## Environment Variables

**Backend (.env):**
```env
OPENAI_API_KEY=sk-proj-xxxxx
OPENAI_MODEL=gpt-4o
```

**Frontend (.env):**
```env
REACT_APP_API_URL=http://localhost:8000
```

---

## Design System

- **Primary Color:** Indigo (#6366f1)
- **Font:** Inter
- **Icons:** Lucide React
- **Dark Mode:** Class-based toggle

---

## Next Steps

1. ✅ Backend running? → http://localhost:8000/docs
2. ✅ Frontend running? → http://localhost:3000
3. 📝 Login to dashboard
4. 🎯 Process your first video
5. 🏆 Take a quiz!

---

**Need help?** See [SETUP-GUIDE.md](SETUP-GUIDE.md)
