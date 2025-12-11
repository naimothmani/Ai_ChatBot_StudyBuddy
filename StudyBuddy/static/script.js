<script>
    // Initialize Particle Background
    tsParticles.load('particles-js', {
        background: { color: "#0a0a0f" },
        fpsLimit: 120,
        interactivity: {
            events: {
                onHover: { enable: true, mode: "repulse" },
                onClick: { enable: true, mode: "push" }
            }
        },
        particles: {
            color: { value: ["#00bcd4", "#9c27b0", "#00ff88", "#e91e63"] },
            links: {
                color: "#ffffff",
                distance: 150,
                enable: true,
                opacity: 0.2,
                width: 1
            },
            move: {
                direction: "none",
                enable: true,
                outModes: "bounce",
                speed: 1
            },
            number: { value: 60 },
            opacity: { value: 0.3 },
            shape: { type: "circle" },
            size: { value: { min: 1, max: 5 } }
        }
    });

    // Always show Smart Mode in status
    document.getElementById('aiStatus').innerHTML = `
        <i class="fas fa-circle" style="color: #ffc107"></i>
        SMART MODE (Always Available)
    `;
    document.getElementById('aiStatus').className = 'ai-status offline';

    // Chat Functions
    function sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Add user message
        addMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        showTyping();
        
        // Always use smart mode - no API errors
        setTimeout(() => {
            removeTyping();
            const smartResponse = generateSmartResponse(message);
            addMessage(smartResponse, 'bot');
        }, 800); // Simulate thinking time
    }

    // Smart response generator (client-side fallback)
    function generateSmartResponse(userInput) {
        const responses = {
            greeting: [
                "✨ Hello! I'm Aura Study Buddy in Smart Mode! Ready to optimize your learning?",
                "🌟 Welcome! I'm here with enhanced smart responses to help you study better!",
                "🚀 Hey there! Smart Mode activated - let's make studying efficient and effective!"
            ],
            study: [
                "📚 **Smart Study Tip**: Use the Pomodoro technique - 25 min focus, 5 min break!",
                "🧠 **Memory Hack**: Teach what you learn to someone else (real or imaginary)!",
                "⚡ **Focus Boost**: Eliminate digital distractions - phone on airplane mode!"
            ],
            exam: [
                "🔥 **Exam Strategy**: Start with past papers, focus on high-yield topics!",
                "📊 **Test Prep**: Create summary sheets for each chapter - condense key points!"
            ],
            default: [
                "🎓 I'm in Smart Mode! Ask me about study techniques, time management, or motivation!",
                "💡 Try: 'How to focus better?' or 'Best study schedule for exams?'"
            ]
        };
        
        const input = userInput.toLowerCase();
        
        if (input.includes('hi') || input.includes('hello') || input.includes('hey')) {
            return responses.greeting[Math.floor(Math.random() * responses.greeting.length)];
        }
        else if (input.includes('study') || input.includes('learn')) {
            return responses.study[Math.floor(Math.random() * responses.study.length)];
        }
        else if (input.includes('exam') || input.includes('test')) {
            return responses.exam[Math.floor(Math.random() * responses.exam.length)];
        }
        else {
            return responses.default[Math.floor(Math.random() * responses.default.length)];
        }
    }

    function addMessage(text, sender) {
        const container = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const time = new Date().toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const avatarIcon = sender === 'bot' ? 'fa-robot' : 'fa-user';
        const senderName = sender === 'bot' ? 'Aura AI' : 'You';
        
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas ${avatarIcon}"></i>
            </div>
            <div class="message-content">
                <div class="message-sender">${senderName}</div>
                <div class="message-text">${formatText(text)}</div>
                <div class="message-time">${time}</div>
            </div>
        `;
        
        container.appendChild(messageDiv);
        container.scrollTop = container.scrollHeight;
    }

    function showTyping() {
        const container = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'message bot-message';
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="message-content">
                <div class="message-sender">Aura AI</div>
                <div class="message-text">
                    <div style="display: flex; gap: 5px;">
                        <div style="width: 8px; height: 8px; background: var(--accent-color); border-radius: 50%; animation: bounce 1.4s infinite;"></div>
                        <div style="width: 8px; height: 8px; background: var(--accent-color); border-radius: 50%; animation: bounce 1.4s infinite 0.2s;"></div>
                        <div style="width: 8px; height: 8px; background: var(--accent-color); border-radius: 50%; animation: bounce 1.4s infinite 0.4s;"></div>
                    </div>
                </div>
                <div class="message-time">thinking...</div>
            </div>
        `;
        
        container.appendChild(typingDiv);
        container.scrollTop = container.scrollHeight;
    }

    function removeTyping() {
        const typing = document.getElementById('typingIndicator');
        if (typing) typing.remove();
    }

    function formatText(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n/g, '<br>');
    }

    function handleKeyPress(event) {
        if (event.key === 'Enter') {
            sendMessage();
        }
    }

    function quickQuestion(question) {
        document.getElementById('messageInput').value = question;
        sendMessage();
    }

    async function createStudyPlan() {
        const subjectsInput = document.getElementById('planSubjects');
        const hoursInput = document.getElementById('planHours');
        const daysInput = document.getElementById('planDays');
        const output = document.getElementById('planOutput');
        
        const subjects = subjectsInput.value.split(',').map(s => s.trim()).filter(s => s);
        const hours = parseInt(hoursInput.value);
        const days = parseInt(daysInput.value);
        
        if (!subjects.length) {
            alert('Please enter at least one subject');
            return;
        }
        
        output.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Generating smart study plan...</p>';
        output.style.display = 'block';
        
        try {
            const response = await fetch('/create_plan', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    subjects: subjects,
                    hours: hours,
                    days: days
                })
            });
            
            const data = await response.json();
            
            output.innerHTML = `
                <h4 style="color: var(--accent-color); margin-bottom: 10px;">✨ Your Smart Study Plan</h4>
                <p style="white-space: pre-line;">${data.plan}</p>
                <button class="btn-aura" style="margin-top: 10px;" onclick="savePlan('${data.id}')">
                    <i class="fas fa-save"></i> Save This Plan
                </button>
            `;
            
        } catch (error) {
            // Fallback to client-side plan generation
            output.innerHTML = `
                <h4 style="color: var(--accent-color); margin-bottom: 10px;">✨ Generated Smart Plan</h4>
                <p style="white-space: pre-line;">
                📚 **QUICK STUDY PLAN**

                Subjects: ${subjects.join(', ')}
                Schedule: ${hours} hours/day for ${days} days
                
                💡 **Smart Tips**:
                1. Study ${subjects[0]} in the morning when fresh
                2. Review all subjects every 3 days
                3. Take 10-min breaks every hour
                4. Practice past papers weekly
                
                🎯 **Success Formula**: Consistency + Smart Techniques = Results!
                </p>
            `;
        }
    }

    function savePlan(planId) {
        alert(`Plan ${planId} saved! (In a real app, this would save to your profile)`);
    }

    // Load quick tips on startup
    async function loadQuickTips() {
        try {
            const response = await fetch('/quick_tips');
            const data = await response.json();
            
            // Add tips to chat
            setTimeout(() => {
                addMessage(`💡 **Quick Study Tips**: ${data.tips.join(' • ')}`, 'bot');
            }, 1500);
        } catch (error) {
            // Fallback tips
            setTimeout(() => {
                addMessage("💡 **Pro Tip**: Study in focused blocks with regular breaks for best results!", 'bot');
            }, 1500);
        }
    }

    // Focus on input when page loads
    document.addEventListener('DOMContentLoaded', () => {
        document.getElementById('messageInput').focus();
        loadQuickTips();
    });
</script>