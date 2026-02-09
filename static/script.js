let currentResults = null;
let currentMode = 'url';

function switchMode(mode) {
    currentMode = mode;
    
    // Update toggle buttons
    document.getElementById('urlModeBtn').classList.toggle('active', mode === 'url');
    document.getElementById('transcriptModeBtn').classList.toggle('active', mode === 'transcript');
    
    // Show/hide input modes
    document.getElementById('urlMode').style.display = mode === 'url' ? 'block' : 'none';
    document.getElementById('transcriptMode').style.display = mode === 'transcript' ? 'block' : 'none';
    
    // Update button text
    const btnText = document.querySelector('.btn-text');
    btnText.textContent = 'Generate Learning Materials';
}

document.getElementById('videoForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const loader = submitBtn.querySelector('.loader');
    
    let requestBody;
    
    if (currentMode === 'url') {
        const youtubeUrl = document.getElementById('youtubeUrl').value.trim();
        if (!youtubeUrl) {
            showError('Please enter a YouTube URL');
            return;
        }
        requestBody = { youtube_url: youtubeUrl };
    } else {
        const transcript = document.getElementById('transcriptText').value.trim();
        const title = document.getElementById('videoTitle').value.trim() || 'Video Learning Materials';
        
        if (!transcript) {
            showError('Please paste a video transcript');
            return;
        }
        
        if (transcript.length < 100) {
            showError('Transcript is too short. Please provide a longer transcript (at least 100 characters)');
            return;
        }
        
        requestBody = { 
            transcript: transcript,
            video_title: title
        };
    }
    
    // Hide previous results/errors
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    
    // Disable button
    submitBtn.disabled = true;
    btnText.textContent = 'Processing...';
    loader.style.display = 'inline-block';
    
    try {
        const endpoint = currentMode === 'url' ? '/process-video' : '/process-transcript';
        
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestBody)
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'An error occurred while processing');
        }
        
        currentResults = data;
        displayResults(data);
        
    } catch (error) {
        showError(error.message);
    } finally {
        document.getElementById('loading').style.display = 'none';
        submitBtn.disabled = false;
        btnText.textContent = 'Generate Learning Materials';
        loader.style.display = 'none';
    }
});

function displayResults(data) {
    // Set video info
    document.getElementById('videoTitle').textContent = data.video_title;
    document.getElementById('videoDuration').textContent = `⏱️ ${data.duration}`;
    
    // Set summary
    document.getElementById('summary').textContent = data.summary;
    
    // Set key points
    const keyPointsList = document.getElementById('keyPoints');
    keyPointsList.innerHTML = '';
    data.key_points.forEach(point => {
        const li = document.createElement('li');
        li.textContent = point;
        keyPointsList.appendChild(li);
    });
    
    // Set quiz
    const quizContainer = document.getElementById('quiz');
    quizContainer.innerHTML = '';
    data.quiz.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.className = 'quiz-question';
        
        const questionTitle = document.createElement('h4');
        questionTitle.textContent = `${index + 1}. ${question.question}`;
        questionDiv.appendChild(questionTitle);
        
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'quiz-options';
        
        question.options.forEach(option => {
            const optionDiv = document.createElement('div');
            optionDiv.className = 'quiz-option';
            if (option === question.correct_answer) {
                optionDiv.classList.add('correct');
            }
            optionDiv.textContent = option;
            optionsDiv.appendChild(optionDiv);
        });
        
        questionDiv.appendChild(optionsDiv);
        quizContainer.appendChild(questionDiv);
    });
    
    // Show results
    document.getElementById('results').style.display = 'block';
    
    // Scroll to results
    document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function showError(message) {
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('error').style.display = 'block';
    document.getElementById('error').scrollIntoView({ behavior: 'smooth' });
}

function fillExample(url) {
    document.getElementById('youtubeUrl').value = url;
}

function resetForm() {
    document.getElementById('videoForm').reset();
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function downloadResults() {
    if (!currentResults) return;
    
    const content = `
Smart Video Learning Tool - Results
====================================

Video: ${currentResults.video_title}
Duration: ${currentResults.duration}

SUMMARY
-------
${currentResults.summary}

KEY POINTS
----------
${currentResults.key_points.map((point, i) => `${i + 1}. ${point}`).join('\n')}

QUIZ QUESTIONS
--------------
${currentResults.quiz.map((q, i) => `
${i + 1}. ${q.question}

Options:
${q.options.map((opt, j) => `   ${String.fromCharCode(65 + j)}. ${opt}${opt === q.correct_answer ? ' ✓ (Correct)' : ''}`).join('\n')}

`).join('\n')}

Generated by Smart Video Learning Tool
Powered by OpenAI GPT-4o
    `.trim();
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${currentResults.video_title.replace(/[^a-z0-9]/gi, '_')}_learning_materials.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}
