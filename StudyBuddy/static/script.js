// Global variables
let messageCount = 0;
let planCount = 0;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    updateTime();
    loadFeatures();
    loadStats();
    
    // Focus on input
    document.getElementById('message-input').focus();
    
    // Update time every minute
    setInterval(updateTime, 60000);
});

// Update time in messages
function updateTime() {
    const messages = document.querySelectorAll('.message-time');
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
    
    // Update only the last message if needed
    if (messages.length > 0) {
        messages[messages.length - 1].textContent = timeString;
    }
}

// Load features from server
function loadFeatures() {
    fetch('/features')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('features-list');
            container.innerHTML = '';
            
            data.features.forEach(feature => {
                const div = document.createElement('div');
                div.className = 'feature-item';
                div.innerHTML = `<i class="fas fa-check"></i><span>${feature}</span>`;
                container.appendChild(div);
            });
        })
        .catch(error => {
            console.error('Error loading features:', error);
        });
}

// Load stats from localStorage
function loadStats() {
    const savedMessages = localStorage.getItem('studyBuddyMessages');
    const savedPlans = localStorage.getItem('studyBuddyPlans');
    
    if (savedMessages) messageCount = parseInt(savedMessages);
    if (savedPlans) planCount = parseInt(savedPlans);
    
    updateStatsDisplay();
}

// Save stats to localStorage
function saveStats() {
    localStorage.setItem('studyBuddyMessages', messageCount.toString());
    localStorage.setItem('studyBuddyPlans', planCount.toString());
}

// Update stats display
function updateStatsDisplay() {
    document.getElementById('message-count').textContent = messageCount;
    document.getElementById('plan-count').textContent = planCount;
    saveStats();
}

// Send message to chatbot
function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    input.value = '';
    
    // Update stats
    messageCount++;
    updateStatsDisplay();
    
    // Show typing indicator
    showTypingIndicator();
    
    // Send to server
    fetch('/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    })
    .then(response => response.json())
    .then(data => {
        removeTypingIndicator();
        addMessage(data.response, 'bot');
    })
    .catch(error => {
        removeTypingIndicator();
        addMessage("Sorry, I'm having trouble connecting. Please try again!", 'bot');
    });
}

// Send quick message from button
function sendQuickMessage(message) {
    document.getElementById('message-input').value = message;
    sendMessage();
}

// Add message to chat
function addMessage(text, sender) {
    const container = document.getElementById('chat-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatarIcon = sender === 'bot' ? 'fa-robot' : 'fa-user';
    const senderName = sender === 'bot' ? 'StudyBuddy' : 'You';
    const time = new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${avatarIcon}"></i>
        </div>
        <div class="message-content">
            <div class="message-sender">${senderName}</div>
            <div class="message-text">${formatMessage(text)}</div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}

// Format message text
function formatMessage(text) {
    // Convert markdown-like formatting
    return text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
}

// Show typing indicator
function showTypingIndicator() {
    const container = document.getElementById('chat-messages');
    
    const typingDiv = document.createElement('div');
    typingDiv.id = 'typing-indicator';
    typingDiv.className = 'message bot-message';
    
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-sender">StudyBuddy</div>
            <div class="message-text">
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>
            <div class="message-time">typing...</div>
        </div>
    `;
    
    container.appendChild(typingDiv);
    container.scrollTop = container.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const typing = document.getElementById('typing-indicator');
    if (typing) typing.remove();
}

// Handle Enter key
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Clear chat
function clearChat() {
    if (confirm('Are you sure you want to clear the chat?')) {
        const container = document.getElementById('chat-messages');
        container.innerHTML = '';
        messageCount = 0;
        planCount = 0;
        updateStatsDisplay();
    }   } 