# IQStorm
IQStorm is an AI-powered IQ testing web app built with Flask and Google Gemini. It features real-time question generation, dynamic IQ scoring, user profiles with JSON storage, and a responsive UI—all in a single Python file. Showcases full-stack dev, AI integration, and prompt engineering.
#  IQ Storm

IQ Storm is an AI-powered web application that dynamically generates playful IQ-style questions using Google Gemini and evaluates user answers to adjust IQ scores in real time. The app supports multiple users, tracks their scores, and delivers an engaging experience through a clean, responsive UI.

##  Features

-  Real-time IQ question generation via Google Gemini
- Adaptive IQ scoring based on user answers
- Multi-user support with persistent score tracking
- Markdown-rendered questions for rich formatting
- Responsive and styled UI using HTML/CSS
- Simple and secure data handling using JSON

##  Tech Stack

- **Frontend**: HTML, CSS (inline styling with basic responsiveness)
- **Backend**: Python, Flask
- **AI Integration**: Google Gemini API
- **Data Storage**: JSON file-based persistence
- **Others**: Markdown parsing, API prompt engineering

## How It Works

1. Users can register with their name.
2. Clicking "Generate New Question" fetches a new AI-generated IQ test prompt.
3. Submitting an answer sends it to Gemini to determine IQ change.
4. Updated scores are displayed and stored for each user.

##  Security Note

Make sure to store your Gemini API key securely:
```bash
export GEMINI_API_KEY=your_key_here
