#!/bin/bash
echo "🔑 Update OpenAI API Key"
echo ""
echo "Current key status: QUOTA EXCEEDED ❌"
echo ""
read -p "Enter your new OpenAI API key: " new_key
echo ""
echo "OPENAI_API_KEY=$new_key" > .env
echo "OPENAI_MODEL=gpt-4o" >> .env
echo ""
echo "✅ API key updated! Restart the backend:"
echo "   pkill -f uvicorn"
echo "   python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
