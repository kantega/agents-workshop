# Agent Discussion Visualizer

A web application that visualizes real multi-agent conversations about user feedback, powered by the AutoGen framework and Azure OpenAI.

## Features

- **Real AI-Generated Responses**: Connects to actual AutoGen agents with Azure OpenAI
- **Visual Agent Representation**: Each agent has a unique avatar and color scheme
- **Real-time Discussion**: Watch agents discuss user feedback with genuine AI responses
- **Interactive User Participation**: Real human input required for User Proxy responses
- **Custom Feedback Input**: Enter your own feedback for agents to discuss
- **Responsive Design**: Works on desktop and mobile devices
- **Typing Indicators**: Shows when agents are "thinking" and typing responses
- **Backend Integration**: Flask backend connects to AutoGen framework

## Architecture

The system consists of two parts:
1. **Frontend**: HTML/CSS/JavaScript web interface
2. **Backend**: Flask server that runs AutoGen agents with Azure OpenAI

## Agents

The visualizer includes 5 agents that mirror the Python implementation:

1. **😊 Positiv Agent** - Focuses on what went well
2. **🔍 Kritisk Agent** - Focuses on things that can be improved
3. **😏 Kynisk Agent** - Comments cynically on everything
4. **😂 Morsom Agent** - Makes jokes out of the discussion
5. **👤 User Proxy** - Represents the user (requires human input)

## Setup Instructions

### Prerequisites

- Python 3.8+
- Azure OpenAI API access
- Modern web browser

### 1. Install Backend Dependencies

```bash
cd keiken_agentic_summary/website
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the project root with your Azure OpenAI credentials:

```env
API_KEY=your_azure_openai_api_key
```

### 3. Start the Backend Server

```bash
python backend.py
```

The backend will start on `http://localhost:5000`

### 4. Open the Frontend

Open `index.html` in your web browser. The page will automatically check backend connectivity.

## How to Use

1. **Start Backend**: Ensure the Flask backend is running
2. **Open Website**: Open `index.html` in your browser
3. **Check Connection**: Look for "✅ Connected to AutoGen backend" status
4. **Start Discussion**: Click "Start Demo" to begin real AI discussion
5. **Participate**: When prompted, enter your responses as the User Proxy
6. **Custom Feedback**: 
   - Edit the feedback text in the textarea
   - Click "Submit to Agents" to discuss custom feedback

## Controls

- **Start Demo**: Begin a new AI-powered discussion
- **Pause/Resume**: Pause or resume the ongoing discussion
- **Clear Chat**: Reset the conversation and stop backend discussion
- **Submit to Agents**: Start discussion with custom feedback

## Technical Details

### Frontend
- **Pure HTML/CSS/JavaScript**: No external dependencies
- **Responsive Grid Layout**: Adapts to different screen sizes
- **Real-time Polling**: Fetches messages from backend every second
- **Modern JavaScript**: Uses ES6+ features like classes and async/await

### Backend
- **Flask API**: RESTful endpoints for discussion management
- **AutoGen Integration**: Real AutoGen agents with Azure OpenAI
- **Async Processing**: Handles concurrent agent conversations
- **CORS Enabled**: Allows frontend-backend communication

## API Endpoints

- `GET /health` - Check backend status
- `POST /start_discussion` - Start new discussion with feedback
- `GET /get_messages` - Poll for new messages from agents
- `POST /send_user_input` - Send user response to discussion
- `POST /stop_discussion` - Stop current discussion

## File Structure

```
website/
├── index.html          # Main HTML structure
├── styles.css          # All styling and animations
├── script.js           # Frontend JavaScript functionality
├── backend.py          # Flask backend server
├── requirements.txt    # Python dependencies
└── README.md          # This documentation
```

## Error Handling

- **Backend Offline**: Frontend shows error messages and falls back gracefully
- **API Errors**: Clear error messages displayed to user
- **Connection Issues**: Automatic retry and status indicators

## Browser Compatibility

- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Responsive design supported

## Connection to Python Implementation

This visualizer directly integrates with the `discuss_user_feedback.py` script:
- Uses the same AutoGen agents and configuration
- Connects to Azure OpenAI with the same credentials
- Maintains the same discussion flow and termination conditions
- Provides real AI responses instead of pre-programmed ones

## Troubleshooting

### Backend Won't Start
- Check if all dependencies are installed: `pip install -r requirements.txt`
- Verify `.env` file contains valid `API_KEY`
- Ensure port 5000 is not in use

### Frontend Shows "Backend Not Available"
- Confirm backend is running on `http://localhost:5000`
- Check browser console for CORS errors
- Verify network connectivity

### Agents Don't Respond
- Check Azure OpenAI API key validity
- Monitor backend console for error messages
- Verify internet connection for API calls
