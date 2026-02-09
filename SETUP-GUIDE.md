# 🚀 SmartLearn AI - Complete Setup Guide

## Overview
This guide will help you set up both the **React frontend** and **FastAPI backend** for SmartLearn AI.

---

## Prerequisites

### Required Software
- **Python 3.10+** - Backend runtime
- **Node.js 16+** - Frontend runtime  
- **npm 8+** - Package manager
- **Git** - Version control

### Check Installations
```bash
python3 --version  # Should be 3.10+
node --version     # Should be 16+
npm --version      # Should be 8+
```

---

## 🔧 Backend Setup (FastAPI)

### Step 1: Install Python Dependencies

```bash
cd "/home/navgurukul/AI Learning Studio"
pip install --break-system-packages -r requirements.txt
```

**Packages installed:**
- `fastapi==0.109.0` - Web framework
- `uvicorn==0.27.0` - ASGI server
- `openai==2.17.0` - GPT-4o integration
- `youtube-transcript-api==0.6.2` - YouTube support
- `pydantic==2.5.3` - Data validation
- `python-dotenv==1.0.0` - Environment config

### Step 2: Configure OpenAI API Key

Create a `.env` file in the project root:

```bash
echo 'OPENAI_API_KEY=sk-proj-your-actual-key-here' > .env
```

Or manually create `.env`:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o
```

### Step 3: Start the Backend Server

```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Server will start at:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Legacy UI: http://localhost:8000 (old HTML interface)

✅ **Backend is now running!**

---

## 🎨 Frontend Setup (React + Tailwind)

### Step 1: Run the Automated Setup Script

```bash
cd "/home/navgurukul/AI Learning Studio"
chmod +x setup-frontend.sh
./setup-frontend.sh
```

This script will:
1. Check Node.js installation
2. Install all npm dependencies
3. Configure Tailwind CSS
4. Provide next steps

### Step 2: Manual Setup (Alternative)

If the script doesn't work, install manually:

```bash
cd frontend
npm install
```

**Packages installed:**
- `react@18.2` - UI framework
- `react-router-dom@6.20` - Routing
- `tailwindcss@3.3` - Styling
- `axios@1.6` - HTTP client
- `lucide-react@0.292` - Icons

### Step 3: Start the React Development Server

```bash
cd frontend
npm start
```

**Frontend will open at:**
- Development: http://localhost:3000
- Automatically opens in browser

✅ **Frontend is now running!**

---

## 🌐 Access the Application

### For End Users

1. **Open Browser**: http://localhost:3000
2. **Landing Page**: Click "Get Started"
3. **Sign Up**: Create account (frontend-only auth)
4. **Login**: Access dashboard
5. **Start Learning**: 
   - Go to "New Learning"
   - Choose input mode (URL or Transcript)
   - Generate materials

### For Developers

**Backend API:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

**Frontend Dev Tools:**
- React DevTools (browser extension)
- Tailwind CSS IntelliSense (VS Code)

---

## 📁 File Structure

```
AI Learning Studio/
│
├── frontend/                        # React Application
│   ├── public/
│   │   └── index.html              # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── LandingPage.js      # Hero section
│   │   │   ├── AuthCard.js         # Login/Signup
│   │   │   ├── Dashboard.js        # Main dashboard
│   │   │   └── LearningWorkspace.js # Video processing
│   │   ├── App.js                  # Router & auth logic
│   │   ├── index.js                # Entry point
│   │   └── index.css               # Global styles
│   ├── package.json                # Dependencies
│   └── tailwind.config.js          # Tailwind config
│
├── services/                        # Backend Services
│   ├── transcript_service.py       # YouTube extraction
│   └── openai_service.py           # GPT-4o processing
│
├── static/                          # Legacy HTML UI
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── main.py                          # FastAPI app
├── config.py                        # Settings
├── models.py                        # Data models
├── requirements.txt                 # Python deps
├── .env                             # API keys (create this)
└── setup-frontend.sh                # Frontend installer
```

---

## 🎯 Testing the Application

### Test Backend API

```bash
# Health check
curl http://localhost:8000/health

# Process transcript
curl -X POST http://localhost:8000/process-transcript \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "This is a test transcript about machine learning. Artificial intelligence is transforming education. Students can learn faster with AI tools. GPT models help generate quizzes automatically. This technology makes learning more accessible for everyone.",
    "video_title": "AI in Education Test"
  }'
```

### Test Frontend

1. Navigate to http://localhost:3000
2. Click "Get Started"
3. Login with any email (demo@test.com)
4. Go to "New Learning"
5. Switch to "Paste Transcript" mode
6. Paste a sample transcript (100+ chars)
7. Click "Generate Learning Materials"
8. Verify all 3 tabs work:
   - Summary
   - Key Insights  
   - Quiz (submit and check score)

---

## 🚨 Troubleshooting

### Backend Issues

**Problem:** `OPENAI_API_KEY not set`
```bash
# Solution: Create .env file
echo 'OPENAI_API_KEY=your-key' > .env
```

**Problem:** `Port 8000 already in use`
```bash
# Solution: Kill existing process
lsof -i :8000 | grep LISTEN
kill -9 <PID>
```

**Problem:** `Module not found`
```bash
# Solution: Reinstall dependencies
pip install --break-system-packages -r requirements.txt
```

### Frontend Issues

**Problem:** `npm: command not found`
```bash
# Solution: Install Node.js
# Visit: https://nodejs.org/
```

**Problem:** `Cannot connect to backend`
```bash
# Solution: Check backend is running
curl http://localhost:8000/health

# Update API_BASE in frontend/src/components/LearningWorkspace.js if needed
```

**Problem:** `Port 3000 already in use`
```bash
# Solution: Use different port
PORT=3001 npm start
```

**Problem:** Dependencies won't install
```bash
# Solution: Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

## 🔒 Environment Variables

### Backend (.env)

```env
# Required
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx

# Optional
OPENAI_MODEL=gpt-4o
OPENAI_TEMPERATURE=0.7
OPENAI_MAX_TOKENS=4000
HOST=0.0.0.0
PORT=8000
DEBUG=False
```

### Frontend

No `.env` needed for frontend in development. The API endpoint is hardcoded in `LearningWorkspace.js`:

```javascript
const API_BASE = 'http://localhost:8000';
```

For production, create `frontend/.env`:
```env
REACT_APP_API_URL=https://your-production-api.com
```

---

## 🐳 Docker Deployment (Optional)

### Build and Run

```bash
docker-compose up -d
```

### Services

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000

### Stop Services

```bash
docker-compose down
```

---

## 📚 Next Steps

1. **Customize Design**: Edit Tailwind colors in `frontend/tailwind.config.js`
2. **Add Features**: Implement backend authentication
3. **Deploy**: Use Vercel (frontend) + Railway (backend)
4. **Database**: Add PostgreSQL for user history
5. **Analytics**: Track learning progress

---

## 🎓 Learning Resources

### React + Tailwind
- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [React Router](https://reactrouter.com)

### FastAPI + OpenAI
- [FastAPI Docs](https://fastapi.tiangolo.com)
- [OpenAI API](https://platform.openai.com/docs)
- [Pydantic](https://docs.pydantic.dev)

---

## 💡 Tips

1. **Backend Auto-Reload**: Changes to Python files automatically restart server
2. **Frontend Hot Reload**: React updates instantly without refresh
3. **Debugging**: Use browser DevTools for frontend, `/docs` for backend
4. **Performance**: Use `npm run build` for production-optimized frontend
5. **Security**: Never commit `.env` file to Git

---

## ✅ Verification Checklist

- [ ] Python 3.10+ installed
- [ ] Node.js 16+ installed
- [ ] Backend dependencies installed
- [ ] `.env` file created with API key
- [ ] Backend running on port 8000
- [ ] Frontend dependencies installed
- [ ] Frontend running on port 3000
- [ ] Can access landing page
- [ ] Can login/signup
- [ ] Can process transcript
- [ ] All 3 tabs working
- [ ] Quiz submission works

---

## 🆘 Getting Help

**Issues?** Check:
1. Terminal output for errors
2. Browser console (F12)
3. API docs at /docs
4. This setup guide

**Still stuck?** Common solutions:
- Restart both servers
- Clear browser cache
- Check firewall settings
- Verify all dependencies installed

---

**🎉 Congratulations! You now have a fully functional AI learning platform!**
