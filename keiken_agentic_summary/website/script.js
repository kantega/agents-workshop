class AgentDiscussionVisualizer {
    constructor() {
        this.agents = {
            positiv_agent: {
                name: 'Positiv Agent',
                avatar: '😊'
            },
            kritisk_agent: {
                name: 'Kritisk Agent',
                avatar: '🔍'
            },
            kynisk_agent: {
                name: 'Kynisk Agent',
                avatar: '😏'
            },
            morsom_agent: {
                name: 'Morsom Agent',
                avatar: '😂'
            },
            user_proxy: {
                name: 'Bruker Proxy',
                avatar: '👤'
            }
        };

        this.backendUrl = 'http://localhost:5000';
        this.isRunning = false;
        this.isPaused = false;
        this.messagePollingInterval = null;
        this.backendAvailable = false;
        this.currentDiscussion = [];
        this.discussionIndex = 0;

        // Demo responses for fallback mode
        this.demoResponses = {
            positiv_agent: [
                'Presentasjonene var klare og lette å følge - det er flott!',
                'Utmerkede foredragsholdere som virkelig kunne emnet sitt.',
                'Flott mulighet til å knytte kontakter med kolleger.',
                'Lærte mye nytt om nye teknologier - fantastisk!',
                'Den gamifiserte læringsopplevelsen holdt meg engasjert.'
            ],
            kritisk_agent: [
                'Noen økter gikk over tiden, det gjorde timeplanen stressende.',
                'Arrangementet kunne vært bedre organisert praktisk sett.',
                'For mye innhold på for kort tid - vi trenger flere pauser.',
                'Lydkvaliteten var dårlig under digitale økter.',
                'Noen materiell ble ikke delt på forhånd.'
            ],
            kynisk_agent: [
                'Selvfølgelig gikk det over tiden - som alltid.',
                'Organisering? Det er vel å forvente for mye.',
                'Typisk at vi får for mye innhold og for lite tid.',
                'Lydkvalitet? Det er vel ikke prioritert.',
                'Materiell på forhånd? Det hadde vært for enkelt.'
            ],
            morsom_agent: [
                'Øktene gikk så over tiden at vi fikk gratis overtid! ⏰',
                'Organisering? Vi kaller det "spontan eventplanlegging"! 🎲',
                'For mye innhold = mer valuta for pengene! 💰',
                'Dårlig lydkvalitet gir oss øvelse i lipplesing! 👄',
                'Materiell på forhånd? Vi liker overraskelser! 🎁'
            ]
        };

        this.initializeEventListeners();
        this.checkBackendHealth();
    }

    async checkBackendHealth() {
        try {
            const response = await fetch(`${this.backendUrl}/health`);
            if (response.ok) {
                console.log('Backend is running');
                this.showBackendStatus('✅ Connected to AutoGen backend - Real AI responses');
                this.backendAvailable = true;
            } else {
                this.showBackendStatus('❌ Backend not responding - Using demo mode');
                this.backendAvailable = false;
            }
        } catch (error) {
            console.error('Backend health check failed:', error);
            this.showBackendStatus('❌ Backend not available - Using demo mode');
            this.backendAvailable = false;
        }
    }

    showBackendStatus(message) {
        const header = document.querySelector('header p');
        header.textContent = message;
    }

    initializeEventListeners() {
        document.getElementById('startDemo').addEventListener('click', () => this.startDemo());
        document.getElementById('clearChat').addEventListener('click', () => this.clearChat());
        document.getElementById('pauseDemo').addEventListener('click', () => this.togglePause());
        document.getElementById('submitFeedback').addEventListener('click', () => this.submitCustomFeedback());
        document.getElementById('sendUserResponse').addEventListener('click', () => this.submitUserResponse());

        // Agent card click handlers
        document.querySelectorAll('.agent-card').forEach(card => {
            card.addEventListener('click', () => this.highlightAgent(card.dataset.agent));
        });

        // Add Enter key support for user input
        document.getElementById('userResponseInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.submitUserResponse();
            }
        });
    }

    async startDemo() {
        if (this.isRunning && !this.isPaused) return;
        
        this.isRunning = true;
        this.isPaused = false;
        
        document.getElementById('startDemo').textContent = 'Running...';
        document.getElementById('startDemo').disabled = true;
        document.getElementById('pauseDemo').textContent = 'Pause';

        this.clearChat();
        
        if (this.backendAvailable) {
            await this.startBackendDiscussion();
        } else {
            this.startDemoMode();
        }
    }

    async togglePause() {
        if (!this.isRunning) return;

        this.isPaused = !this.isPaused;
        document.getElementById('pauseDemo').textContent = this.isPaused ? 'Resume' : 'Pause';
        
        if (this.backendAvailable) {
            if (this.isPaused) {
                this.stopMessagePolling();
            } else {
                this.startMessagePolling();
            }
        } else {
            // In demo mode, continue the discussion when resumed
            if (!this.isPaused) {
                this.runDemoDiscussion();
            }
        }
    }

    async clearChat() {
        const chatContainer = document.getElementById('chatContainer');
        chatContainer.innerHTML = `
            <div class="welcome-message">
                <p>👋 Welcome to the Agent Discussion Visualizer!</p>
                <p>Click "Start Demo" to see how agents discuss real AI-generated responses.</p>
            </div>
        `;
        
        this.isRunning = false;
        this.isPaused = false;
        
        document.getElementById('startDemo').textContent = 'Start Demo';
        document.getElementById('startDemo').disabled = false;
        document.getElementById('pauseDemo').textContent = 'Pause';

        // Remove speaking indicators
        document.querySelectorAll('.agent-card').forEach(card => {
            card.classList.remove('speaking');
        });

        // Hide user input area
        const userInputArea = document.getElementById('userInputArea');
        userInputArea.style.display = 'none';

        // Stop backend discussion
        try {
            await fetch(`${this.backendUrl}/stop_discussion`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
        } catch (error) {
            console.error('Error stopping backend discussion:', error);
        }

        this.stopMessagePolling();
    }

    async startBackendDiscussion() {
        const feedbackText = document.getElementById('feedbackText').value;
        
        // Validate that feedback is provided (only check if completely empty)
        if (!feedbackText || feedbackText.trim() === '') {
            alert('Please enter some feedback in the text box before starting the discussion!');
            this.resetControls();
            return;
        }
        
        try {
            const response = await fetch(`${this.backendUrl}/start_discussion`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    feedback: feedbackText
                })
            });

            if (response.ok) {
                console.log('Discussion started successfully');
                this.startMessagePolling();
            } else {
                const error = await response.json();
                console.error('Failed to start discussion:', error);
                this.addMessage('system', `❌ Failed to start discussion: ${error.error || 'Unknown error'}`);
                this.resetControls();
            }
        } catch (error) {
            console.error('Error starting discussion:', error);
            this.addMessage('system', '❌ Cannot connect to backend. Please start the backend server.');
            this.resetControls();
        }
    }

    startMessagePolling() {
        if (this.messagePollingInterval) {
            clearInterval(this.messagePollingInterval);
        }

        this.messagePollingInterval = setInterval(async () => {
            if (!this.isPaused) {
                await this.pollMessages();
            }
        }, 1000); // Poll every second
    }

    stopMessagePolling() {
        if (this.messagePollingInterval) {
            clearInterval(this.messagePollingInterval);
            this.messagePollingInterval = null;
        }
    }

    async pollMessages() {
        try {
            const response = await fetch(`${this.backendUrl}/get_messages`);
            if (response.ok) {
                const data = await response.json();
                
                for (const message of data.messages) {
                    await this.handleBackendMessage(message);
                }
            }
        } catch (error) {
            console.error('Error polling messages:', error);
        }
    }

    async handleBackendMessage(message) {
        switch (message.type) {
            case 'task_message':
                // Show the task/question that agents will discuss
                this.addMessage('task', message.message);
                break;
                
            case 'agent_message':
                // Remove any existing typing indicators
                this.hideTypingIndicator();
                
                // Show typing indicator for the agent
                this.showTypingIndicator(message.agent);
                
                // Wait a bit to simulate typing
                await this.sleep(1500);
                
                // Hide typing indicator and show message
                this.hideTypingIndicator();
                this.addMessage(message.agent, message.message);
                break;
                
            case 'user_input_required':
                this.showUserInputPrompt();
                break;
                
            case 'discussion_finished':
                // Don't automatically end - let user proxy control the discussion
                break;
                
            case 'error':
                this.addMessage('system', `❌ Error: ${message.message}`);
                this.resetControls();
                break;
        }
    }

    startDemoMode() {
        console.log('Starting demo mode with simulated responses');
        this.addMessage('system', '🎭 Demo Mode: Using simulated responses (start backend for real AI)');
        this.generateDemoDiscussion();
        this.runDemoDiscussion();
    }

    generateDemoDiscussion() {
        const agentOrder = ['positiv_agent', 'kritisk_agent', 'kynisk_agent', 'morsom_agent'];
        this.currentDiscussion = [];
        this.discussionIndex = 0;

        // Generate initial responses
        agentOrder.forEach((agentId, index) => {
            const responses = this.demoResponses[agentId];
            const response = responses[Math.floor(Math.random() * responses.length)];
            
            this.currentDiscussion.push({
                agent: agentId,
                message: response,
                delay: (index + 1) * 2000
            });
        });

        // Add user interaction point
        this.currentDiscussion.push({
            agent: 'user_input_required',
            message: 'waiting_for_user',
            delay: (this.currentDiscussion.length + 1) * 2000
        });

        // Add second round
        agentOrder.forEach((agentId, index) => {
            const responses = this.demoResponses[agentId];
            const response = responses[Math.floor(Math.random() * responses.length)];
            
            this.currentDiscussion.push({
                agent: agentId,
                message: response,
                delay: (this.currentDiscussion.length + 1) * 2000
            });
        });

        // Add final user interaction
        this.currentDiscussion.push({
            agent: 'user_input_required',
            message: 'waiting_for_user',
            delay: (this.currentDiscussion.length + 1) * 2000
        });
    }

    async runDemoDiscussion() {
        const chatContainer = document.getElementById('chatContainer');
        
        // Clear welcome message if it exists
        const welcomeMessage = chatContainer.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        while (this.discussionIndex < this.currentDiscussion.length && this.isRunning && !this.isPaused) {
            const discussionItem = this.currentDiscussion[this.discussionIndex];
            
            // Check if user input is required
            if (discussionItem.agent === 'user_input_required') {
                this.showUserInputPrompt();
                break;
            }
            
            // Show typing indicator
            this.showTypingIndicator(discussionItem.agent);
            
            // Wait for typing duration
            await this.sleep(1500);
            
            if (this.isPaused || !this.isRunning) break;
            
            // Remove typing indicator and show message
            this.hideTypingIndicator();
            this.addMessage(discussionItem.agent, discussionItem.message);
            
            this.discussionIndex++;
            
            // Wait before next message
            await this.sleep(1000);
        }

        // Discussion finished
        if (this.discussionIndex >= this.currentDiscussion.length) {
            this.resetControls();
        }
    }

    resetControls() {
        this.isRunning = false;
        this.isPaused = false;
        document.getElementById('startDemo').textContent = 'Start Demo';
        document.getElementById('startDemo').disabled = false;
        document.getElementById('pauseDemo').textContent = 'Pause';
        
        // Remove all speaking indicators
        document.querySelectorAll('.agent-card').forEach(card => {
            card.classList.remove('speaking');
        });
        
        this.stopMessagePolling();
    }


    showTypingIndicator(agentId) {
        const chatContainer = document.getElementById('chatContainer');
        const agent = this.agents[agentId];
        
        // Highlight speaking agent
        document.querySelectorAll('.agent-card').forEach(card => {
            card.classList.remove('speaking');
        });
        document.querySelector(`[data-agent="${agentId}"]`).classList.add('speaking');
        
        const typingIndicator = document.createElement('div');
        typingIndicator.className = `typing-indicator ${agentId}`;
        typingIndicator.innerHTML = `
            <div class="message-header">
                <span class="message-avatar">${agent.avatar}</span>
                <span>${agent.name} is typing...</span>
            </div>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        
        chatContainer.appendChild(typingIndicator);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    hideTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    addMessage(agentId, message) {
        const chatContainer = document.getElementById('chatContainer');
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${agentId}`;
        
        if (agentId === 'system' || agentId === 'task') {
            messageElement.innerHTML = `
                <div class="message-content">${message}</div>
            `;
        } else {
            const agent = this.agents[agentId];
            messageElement.innerHTML = `
                <div class="message-header">
                    <span class="message-avatar">${agent.avatar}</span>
                    <span>${agent.name}</span>
                </div>
                <div class="message-content">${message}</div>
            `;
        }
        
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async submitCustomFeedback() {
        const feedbackText = document.getElementById('feedbackText').value.trim();
        if (!feedbackText) {
            alert('Please enter some feedback first!');
            return;
        }

        await this.clearChat();
        
        // Add system message about new feedback instead of user_proxy message
        this.addMessage('system', `🔄 Starting discussion about custom feedback: "${feedbackText}"`);
        
        // Start new discussion with custom feedback
        setTimeout(async () => {
            await this.startDemo();
        }, 1000);
    }

    highlightAgent(agentId) {
        // Remove previous highlights
        document.querySelectorAll('.agent-card').forEach(card => {
            card.style.transform = '';
        });
        
        // Highlight selected agent
        const selectedCard = document.querySelector(`[data-agent="${agentId}"]`);
        selectedCard.style.transform = 'scale(1.05)';
        
        // Reset after 2 seconds
        setTimeout(() => {
            selectedCard.style.transform = '';
        }, 2000);
    }

    showUserInputPrompt() {
        // Show the fixed bottom input area instead of inline prompt
        const userInputArea = document.getElementById('userInputArea');
        userInputArea.style.display = 'block';
        
        // Remove all speaking indicators
        document.querySelectorAll('.agent-card').forEach(card => {
            card.classList.remove('speaking');
        });
        
        // Highlight user proxy
        document.querySelector(`[data-agent="user_proxy"]`).classList.add('speaking');
        
        // Focus on input field
        setTimeout(() => {
            const inputField = document.getElementById('userResponseInput');
            if (inputField) {
                inputField.focus();
            }
        }, 100);
    }

    async submitUserResponse() {
        const userInput = document.getElementById('userResponseInput');
        const response = userInput.value.trim();
        
        if (!response) {
            alert('Please enter a response!');
            return;
        }
        
        // Clear the input field
        userInput.value = '';
        
        // Hide the input area
        const userInputArea = document.getElementById('userInputArea');
        userInputArea.style.display = 'none';
        
        // Add user message
        this.addMessage('user_proxy', response);
        
        if (this.backendAvailable) {
            // Send user input to backend
            try {
                const backendResponse = await fetch(`${this.backendUrl}/send_user_input`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        response: response
                    })
                });

                if (!backendResponse.ok) {
                    console.error('Failed to send user input to backend');
                    this.addMessage('system', '❌ Failed to send response to backend');
                }
            } catch (error) {
                console.error('Error sending user input:', error);
                this.addMessage('system', '❌ Cannot connect to backend');
            }
        } else {
            // Demo mode - continue discussion
            this.discussionIndex++;
            
            // Check if user said APPROVE to end discussion
            if (response.toUpperCase().includes('APPROVE')) {
                this.addMessage('system', '✅ Discussion approved and completed!');
                this.resetControls();
                return;
            }
            
            // Continue the demo discussion
            setTimeout(() => {
                this.runDemoDiscussion();
            }, 1000);
        }
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Initialize the visualizer when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.discussionVisualizer = new AgentDiscussionVisualizer();
});

// Add some fun interactions
document.addEventListener('DOMContentLoaded', () => {
    // Add hover effects to agent cards
    document.querySelectorAll('.agent-card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            const avatar = card.querySelector('.agent-avatar');
            avatar.style.transform = 'scale(1.2) rotate(10deg)';
        });
        
        card.addEventListener('mouseleave', () => {
            const avatar = card.querySelector('.agent-avatar');
            avatar.style.transform = '';
        });
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'Enter':
                    e.preventDefault();
                    document.getElementById('startDemo').click();
                    break;
                case 'Backspace':
                    e.preventDefault();
                    document.getElementById('clearChat').click();
                    break;
            }
        }
    });
});
