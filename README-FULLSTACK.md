# SmartLearn AI - Full Stack Project

A professional-grade AI-powered video learning platform with React frontend and FastAPI backend.

## 🌟 Features

### Frontend (React + Tailwind)
- 🎨 Modern landing page with glassmorphism effects
- 🔐 Authentication UI with social login
- 📊 Dashboard with learning statistics
- 🎯 Interactive learning workspace
- 🌓 Dark/Light mode toggle
- 📱 Fully responsive design

### Backend (FastAPI + OpenAI)
- 🤖 GPT-4o powered content processing
- 📺 YouTube transcript extraction
- 📝 Direct transcript input support
- ✅ Auto-generated quizzes
- 🔍 AI summaries and key insights
- 🐳 Docker deployment ready

## 🚀 Quick Start

### Backend Setup

1. **Install Python dependencies:**
```bash
pip install --break-system-packages -r requirements.txt
```

2. **Configure OpenAI API Key:**
```bash
echo "OPENAI_API_KEY=your-key-here" > .env
```

3. **Start the backend:**
```bash
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Frontend Setup

1. **Run the setup script:**
```bash
chmod +x setup-frontend.sh
./setup-frontend.sh
```

2. **Start the React app:**
```bash
cd frontend
npm start
```

Frontend will open at: http://localhost:3000

## 📁 Project Structure

```
AI Learning Studio/
├── frontend/                    # React + Tailwind frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── LandingPage.js   # Hero & features
│   │   │   ├── AuthCard.js      # Login/Signup
│   │   │   ├── Dashboard.js     # Main dashboard
│   │   │   └── LearningWorkspace.js  # Video processing
│   │   ├── App.js               # Router & auth
│   │   ├── index.js
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
│
├── services/                    # Backend services
│   ├── transcript_service.py    # YouTube extraction
│   └── openai_service.py        # GPT-4o processing
│
├── tests/                       # Test suite
├── docs/                        # Documentation
├── static/                      # Legacy HTML UI
├── main.py                      # FastAPI app
├── models.py                    # Pydantic models
├── config.py                    # Configuration
├── requirements.txt             # Python dependencies
└── .env                         # Environment variables
```

## 🎯 Usage

### For End Users:
1. Visit http://localhost:3000
2. Click "Get Started" to create an account
3. Login with email/password or social login
4. Navigate to "New Learning" in the dashboard
5. Choose input mode:
   - **YouTube URL**: Paste a YouTube video URL
   - **Paste Transcript**: Copy/paste any transcript
6. Click "Generate Learning Materials"
7. Explore the 3 tabs:
   - **Summary**: 3-paragraph overview
   - **Key Insights**: 5 main takeaways
   - **Quiz**: 10 interactive questions

### For Developers:

**API Endpoints:**
- `POST /process-video` - Process YouTube URL
- `POST /process-transcript` - Process raw transcript
- `GET /docs` - Interactive API documentation

**Example API Request:**
```bash
curl -X POST "http://localhost:8000/process-transcript" \
  -H "Content-Type: application/json" \
  -d '{
    "transcript": "Your video transcript here...",
    "video_title": "My Video"
  }'
```

## 🎨 Design System

- **Primary Color**: Indigo (#6366f1)
- **Font**: Inter
- **Icons**: Lucide React
- **Framework**: Tailwind CSS 3
- **Dark Mode**: Class-based toggle

## 🛠 Technologies

### Frontend
- React 18.2
- React Router 6
- Tailwind CSS 3
- Axios
- Lucide React Icons

### Backend
- FastAPI 0.109.0
- OpenAI 2.17.0 (GPT-4o)
- Pydantic 2.5.3
- youtube-transcript-api 0.6.2
- Uvicorn 0.27.0

## 📝 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o
```

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

Services:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📊 Features Breakdown

| Feature | Frontend | Backend | Status |
|---------|----------|---------|--------|
| Landing Page | ✅ | N/A | Complete |
| Authentication UI | ✅ | 🚧 | Frontend Only |
| Dashboard | ✅ | N/A | Complete |
| YouTube Processing | ✅ | ✅ | Complete |
| Transcript Processing | ✅ | ✅ | Complete |
| AI Summaries | ✅ | ✅ | Complete |
| Quiz Generation | ✅ | ✅ | Complete |
| Dark Mode | ✅ | N/A | Complete |
| History Tracking | 🚧 | 🚧 | In Progress |

## 🔒 Authentication Note

The current authentication is **frontend-only** (localStorage based). For production:
- Implement JWT tokens in FastAPI backend
- Add database for user management
- Secure social OAuth flows

## 📚 Documentation

- [API Documentation](docs/API_DOCS.md)
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Quick Start Guide](docs/QUICKSTART.md)
- [Frontend README](frontend/README.md)

## 🎓 Use Cases

- **Students**: Transform lecture videos into study materials
- **Professionals**: Quick insights from conference talks
- **Educators**: Generate quiz content from video lessons
- **Researchers**: Extract key points from presentations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🌟 Credits

- Built with OpenAI GPT-4o
- Powered by FastAPI & React
- Designed with Tailwind CSS
- Icons by Lucide

---

**Made with ❤️ for better learning experiences**
