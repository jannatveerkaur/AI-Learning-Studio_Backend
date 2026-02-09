#!/bin/bash

# Smart Video Learning Tool - Frontend Setup Script

echo "🚀 Setting up SmartLearn AI Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo "✓ Node.js version: $(node -v)"
echo "✓ npm version: $(npm -v)"

# Navigate to frontend directory
cd frontend

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
npm install

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Frontend setup complete!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Make sure the backend is running on port 8000"
    echo "   2. Start the frontend development server:"
    echo ""
    echo "      cd frontend"
    echo "      npm start"
    echo ""
    echo "   3. Open http://localhost:3000 in your browser"
    echo ""
    echo "🎨 Features:"
    echo "   ✓ Modern landing page with glassmorphism"
    echo "   ✓ Authentication UI (Login/Signup)"
    echo "   ✓ Dashboard with stats & history"
    echo "   ✓ Learning workspace with 3-tab interface"
    echo "   ✓ Dark mode support"
    echo "   ✓ Fully responsive design"
    echo ""
else
    echo "❌ Installation failed. Please check the errors above."
    exit 1
fi
