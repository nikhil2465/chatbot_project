class ChatWidget {
    constructor() {
        this.sessionId = null;
        this.isTyping = false;
        this.initializeElements();
        this.setupEventListeners();
        this.loadSession();
    }

    initializeElements() {
        // Main elements
        this.widget = document.getElementById('chatWidget');
        this.messagesContainer = document.getElementById('chatMessages');
        this.chatInput = document.getElementById('chatInput');
        this.sendButton = document.getElementById('sendButton');
        this.floatingButton = document.getElementById('floatingButton');
        this.quickRepliesContainer = document.getElementById('quickReplies');
        this.closeButton = document.getElementById('closeChat');
    }

    setupEventListeners() {
        // Toggle chat
        this.floatingButton.addEventListener('click', () => this.toggleChat());
        
        // Close chat
        this.closeButton.addEventListener('click', () => this.closeChat());
        
        // Send message on button click
        this.sendButton.addEventListener('click', () => this.handleUserInput());
        
        // Send message on Enter key
        this.chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.handleUserInput();
            }
        });
        
        // Add quick replies
        this.addQuickReplies([
            { text: 'Show me your products', payload: 'Show me your products' },
            { text: 'Track my order', payload: 'How can I track my order?' },
            { text: 'Contact support', payload: 'I need to contact support' }
        ]);
    }

    loadSession() {
        // Try to load session from localStorage
        const savedSession = localStorage.getItem('ullasChatSession');
        if (savedSession) {
            const sessionData = JSON.parse(savedSession);
            this.sessionId = sessionData.sessionId;
            
            // If session is recent (less than 1 hour old), load messages
            const oneHourAgo = new Date();
            oneHourAgo.setHours(oneHourAgo.getHours() - 1);
            
            if (new Date(sessionData.timestamp) > oneHourAgo) {
                this.loadMessages(sessionData.messages || []);
            } else {
                // Session expired, clear it
                this.clearSession();
            }
        }
    }

    saveSession() {
        if (this.sessionId) {
            const sessionData = {
                sessionId: this.sessionId,
                timestamp: new Date().toISOString(),
                messages: this.getCurrentMessages()
            };
            localStorage.setItem('ullasChatSession', JSON.stringify(sessionData));
        }
    }

    clearSession() {
        this.sessionId = null;
        localStorage.removeItem('ullasChatSession');
        this.messagesContainer.innerHTML = '';
    }

    getCurrentMessages() {
        const messages = [];
        const messageElements = this.messagesContainer.querySelectorAll('.message');
        
        messageElements.forEach(el => {
            messages.push({
                sender: el.classList.contains('user') ? 'user' : 'bot',
                content: el.textContent.trim(),
                timestamp: el.dataset.timestamp
            });
        });
        
        return messages;
    }

    loadMessages(messageHistory) {
        this.messagesContainer.innerHTML = '';
        
        messageHistory.forEach(msg => {
            this.addMessage(msg.sender, msg.content, msg.timestamp);
        });
        
        this.scrollToBottom();
    }

    toggleChat() {
        this.widget.classList.toggle('active');
        this.floatingButton.style.display = this.widget.classList.contains('active') ? 'none' : 'flex';
        
        if (this.widget.classList.contains('active')) {
            this.chatInput.focus();
        }
    }

    closeChat() {
        this.widget.classList.remove('active');
        this.floatingButton.style.display = 'flex';
    }

    async handleUserInput() {
        const message = this.chatInput.value.trim();
        if (!message) return;
        
        // Clear input
        this.chatInput.value = '';
        
        // Add user message to chat
        this.addMessage('user', message);
        
        // Show typing indicator
        this.showTypingIndicator();
        
        try {
            // Send message to server
            const response = await this.sendMessageToServer(message);
            
            // Remove typing indicator
            this.hideTypingIndicator();
            
            // Add bot response to chat
            if (response && response.response) {
                this.addMessage('bot', response.response);
            }
            
            // Save session
            this.saveSession();
            
        } catch (error) {
            console.error('Error:', error);
            this.hideTypingIndicator();
            this.addMessage('bot', 'Sorry, I encountered an error. Please try again later.');
        }
    }

    async sendMessageToServer(message) {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: this.sessionId,
                message: message
            })
        });
        
        const data = await response.json();
        
        // If this is a new session, store the session ID
        if (data.is_new_session) {
            this.sessionId = data.session_id;
            this.addNewSessionIndicator();
        }
        
        return data;
    }

    addMessage(sender, content, timestamp = null) {
        if (!timestamp) {
            timestamp = new Date().toISOString();
        }
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}`;
        messageElement.textContent = content;
        messageElement.dataset.timestamp = timestamp;
        
        this.messagesContainer.appendChild(messageElement);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        this.isTyping = true;
        
        const typingElement = document.createElement('div');
        typingElement.className = 'typing-indicator';
        typingElement.id = 'typingIndicator';
        typingElement.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        
        this.messagesContainer.appendChild(typingElement);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isTyping = false;
        const typingElement = document.getElementById('typingIndicator');
        if (typingElement) {
            typingElement.remove();
        }
    }

    addQuickReplies(replies) {
        this.quickRepliesContainer.innerHTML = '';
        
        replies.forEach(reply => {
            const button = document.createElement('button');
            button.className = 'quick-reply';
            button.textContent = reply.text;
            button.addEventListener('click', () => {
                this.chatInput.value = reply.payload;
                this.handleUserInput();
            });
            this.quickRepliesContainer.appendChild(button);
        });
    }

    addNewSessionIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'new-session-indicator';
        indicator.textContent = 'New conversation started';
        this.messagesContainer.appendChild(indicator);
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
}

// Initialize the chat widget when the page loads
document.addEventListener('DOMContentLoaded', () => {
    window.chatWidget = new ChatWidget();
    
    // Auto-open the chat after a short delay
    setTimeout(() => {
        window.chatWidget.toggleChat();
    }, 1500);
});
