import asyncio
import json
import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import queue
import time

# Add the parent directory to the path to import the autogen modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import UserProxyAgent
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variables to manage the discussion
current_discussion = None
message_queue = queue.Queue()
user_input_queue = queue.Queue()
discussion_active = False

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")

# Initialize the model client
model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="gpt-4.1-nano",
    model="gpt-4.1-nano",
    api_version="2024-10-21",
    azure_endpoint="https://kjzopenai.openai.azure.com/",
    api_key=api_key,
)

class WebUserProxy(UserProxyAgent):
    """Custom UserProxy that gets input from the web interface"""
    
    def __init__(self, name):
        super().__init__(name, input_func=self.web_input)
    
    def web_input(self, prompt):
        """Wait for user input from the web interface"""
        # Signal that user input is needed
        message_queue.put({
            'type': 'user_input_required',
            'prompt': prompt
        })
        
        # Wait for user input
        user_response = user_input_queue.get()
        return user_response

class DiscussionManager:
    def __init__(self):
        self.agents = {}
        self.team = None
        self.setup_agents()
    
    def setup_agents(self):
        """Initialize all the agents"""
        self.agents['positiv_agent'] = AssistantAgent(
            "positiv_agent",
            model_client=model_client,
            system_message="Fokus på alt som gikk bra. Svar kort (max 1 setning).",
        )
        
        self.agents['kritisk_agent'] = AssistantAgent(
            "kritisk_agent",
            model_client=model_client,
            system_message="Fokus på ting som kan forbedres. Svar kort (max 1 setning).",
        )
        
        self.agents['kynisk_agent'] = AssistantAgent(
            "kynisk_agent",
            model_client=model_client,
            system_message="Kommenter alt på en kynisk måte. Svar kort (max 1 setning).",
        )
        
        self.agents['morsom_agent'] = AssistantAgent(
            "morsom_agent",
            model_client=model_client,
            system_message="Lag en spøk ut av diskusjon. Svar kort (max 1 setning).",
        )
        
        self.agents['user_proxy'] = WebUserProxy("user_proxy")
        
        # Create termination condition - only terminate on APPROVE, increase message limit
        termination = TextMentionTermination("APPROVE") | MaxMessageTermination(max_messages=100)
        
        # Create the team
        self.team = RoundRobinGroupChat(
            [
                self.agents['positiv_agent'],
                self.agents['kritisk_agent'], 
                self.agents['kynisk_agent'],
                self.agents['morsom_agent'],
                self.agents['user_proxy']
            ],
            termination_condition=termination,
        )
    
    async def start_discussion(self, feedback_text):
        """Start the discussion with the given feedback"""
        global discussion_active
        discussion_active = True
        
        try:
            # Use only the feedback provided from the web interface
            if not feedback_text or not feedback_text.strip():
                raise ValueError("No feedback provided. Please enter feedback in the text box.")
            
            # Debug: Print the received feedback to verify newlines are preserved
            print(f"Received feedback with {feedback_text.count(chr(10))} newlines:")
            print(repr(feedback_text))
            
            task = f"Diskuter kort (max 1 setning) feedback fra brukere fra ditt perspektiv. Feedback:\n{feedback_text}"
            
            # Send the initial user_proxy message manually to ensure it appears
            message_queue.put({
                'type': 'agent_message',
                'agent': 'user_proxy',
                'message': task
            })
            
            # Track which agents have responded to avoid duplicates
            responded_agents = set()
            
            # Run the discussion
            stream = self.team.run_stream(task=task)
            
            async for message in stream:
                if not discussion_active:
                    break
                    
                # Extract message information
                if hasattr(message, 'source') and hasattr(message, 'content'):
                    agent_name = message.source
                    content = message.content
                    
                    print(f"Received message from {agent_name}: {content}")
                    
                    # Skip duplicate user_proxy messages (we already sent the initial one)
                    if agent_name == 'user_proxy':
                        if 'user_proxy' in responded_agents:
                            print(f"Skipping duplicate user_proxy message: {content}")
                            continue
                        else:
                            print(f"Skipping AutoGen user_proxy message, using our manual one: {content}")
                            responded_agents.add(agent_name)
                            continue
                    
                    # Track that this agent has responded
                    responded_agents.add(agent_name)
                    
                    # Put message in queue for the web interface
                    message_queue.put({
                        'type': 'agent_message',
                        'agent': agent_name,
                        'message': content
                    })
                    
                    # Small delay to make it feel more natural
                    await asyncio.sleep(1)
                else:
                    print(f"Received message without source/content: {message}")
            
            # Discussion finished - check if it was terminated by condition
            print("Discussion stream ended - checking termination reason")
            
            # If discussion is still active, it means the stream ended unexpectedly
            # Keep the discussion active so user can continue
            if discussion_active:
                print("Discussion stream ended but discussion_active is still True - keeping discussion open")
                # Don't set discussion_active to False here
                return
            
        except Exception as e:
            message_queue.put({
                'type': 'error',
                'message': str(e)
            })
        finally:
            discussion_active = False

# Global discussion manager
discussion_manager = DiscussionManager()

@app.route('/start_discussion', methods=['POST'])
def start_discussion():
    """Start a new discussion"""
    global discussion_active
    
    if discussion_active:
        return jsonify({'error': 'Discussion already active'}), 400
    
    data = request.get_json()
    feedback_text = data.get('feedback', '')
    
    # Clear the message queue
    while not message_queue.empty():
        message_queue.get()
    
    # Start discussion in a separate thread
    def run_discussion():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(discussion_manager.start_discussion(feedback_text))
        loop.close()
    
    thread = threading.Thread(target=run_discussion)
    thread.daemon = True
    thread.start()
    
    return jsonify({'status': 'Discussion started'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    """Get new messages from the discussion"""
    messages = []
    
    # Get all available messages
    while not message_queue.empty():
        try:
            message = message_queue.get_nowait()
            messages.append(message)
        except queue.Empty:
            break
    
    return jsonify({'messages': messages})

@app.route('/send_user_input', methods=['POST'])
def send_user_input():
    """Send user input to the discussion"""
    data = request.get_json()
    user_response = data.get('response', '')
    
    if not user_response:
        return jsonify({'error': 'No response provided'}), 400
    
    # Put user response in the queue
    user_input_queue.put(user_response)
    
    return jsonify({'status': 'User input sent'})

@app.route('/stop_discussion', methods=['POST'])
def stop_discussion():
    """Stop the current discussion"""
    global discussion_active
    discussion_active = False
    
    # Clear queues
    while not message_queue.empty():
        message_queue.get()
    while not user_input_queue.empty():
        user_input_queue.get()
    
    return jsonify({'status': 'Discussion stopped'})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'Backend is running'})

if __name__ == '__main__':
    print("Starting AutoGen Discussion Backend...")
    print("Make sure you have the required environment variables set:")
    print("- API_KEY: Your Azure OpenAI API key")
    app.run(debug=True, port=5000, host='0.0.0.0')
