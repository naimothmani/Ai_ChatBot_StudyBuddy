from flask import Flask, render_template, request, jsonify
import random
import datetime
import google.generativeai as genai

app = Flask(__name__)

# Initialize Gemini API
try:
    GEMINI_API_KEY = "AIzaSyAfgRYfuE0Q-dALH6vCcW-wze75oQLeH38"
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    AI_AVAILABLE = True
    print("✅ Gemini API connected!")
except:
    AI_AVAILABLE = False
    print("⚠️ Using smart mock responses")

# Enhanced mock responses
MOCK_RESPONSES = {
    "greeting": [
        "👋 Hello! I'm your Digital Study Buddy! How can I help you today?",
        "🤖 Hi there! Ready to ace your studies? I'm here to help!"
    ],
    "study": [
        "📚 **Pomodoro Technique**: Study 25 minutes, break 5 minutes. Repeat 4 times, then take a 30-minute break!",
        "🧠 **Active Recall**: Close your books and write down everything you remember. Testing yourself beats re-reading!",
        "⏰ **Time Blocking**: Schedule specific hours for each subject. Consistency is key to success!"
    ],
    "exam": [
        "📝 **Exam Strategy**: Start with past papers, identify weak areas, create summary sheets, practice under timed conditions!",
        "🗓️ **Study Schedule**: Begin studying 2 weeks before exams. Review a little every day instead of cramming!"
    ],
    "motivation": [
        "💪 Remember why you started! Every study session brings you closer to your goals!",
        "🌟 You're capable of amazing things! Break big tasks into small, manageable steps."
    ],
    "default": [
        "🎓 I'm here to help with your studies! Ask me about study techniques, time management, or exam preparation!",
        "📖 Try asking me: 'study tips', 'exam help', 'create schedule', or 'motivation'"
    ]
}

def get_gemini_response(user_input):
    """Get response from Gemini AI"""
    if not AI_AVAILABLE:
        return get_mock_response(user_input)
    
    try:
        prompt = f"""You are StudyPal, a friendly study assistant for HIDE engineering students.
        Provide helpful, concise study advice (2-3 sentences).
        Be encouraging and practical.
        
        Student question: {user_input}
        
        Your response:"""
        
        response = model.generate_content(prompt)
        return response.text.strip()
    except:
        return get_mock_response(user_input)

def get_mock_response(user_input):
    """Get smart mock response"""
    user_input = user_input.lower()
    
    if any(word in user_input for word in ["hi", "hello", "hey", "greetings"]):
        return random.choice(MOCK_RESPONSES["greeting"])
    elif any(word in user_input for word in ["study", "learn", "memorize", "technique"]):
        return random.choice(MOCK_RESPONSES["study"])
    elif any(word in user_input for word in ["exam", "test", "final", "midterm"]):
        return random.choice(MOCK_RESPONSES["exam"])
    elif any(word in user_input for word in ["motivate", "encourage", "tired", "stress"]):
        return random.choice(MOCK_RESPONSES["motivation"])
    else:
        return random.choice(MOCK_RESPONSES["default"])

@app.route('/')
def home():
    """Main page"""
    return render_template('index.html', ai_available=AI_AVAILABLE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_input = data.get('message', '').strip()
    
    if not user_input:
        return jsonify({'error': 'Empty message'}), 400
    
    # Get response
    response = get_gemini_response(user_input) if AI_AVAILABLE else get_mock_response(user_input)
    
    return jsonify({
        'response': response,
        'ai_mode': AI_AVAILABLE
    })

@app.route('/create_plan', methods=['POST'])
def create_plan():
    """Create a study plan"""
    data = request.json
    subjects = data.get('subjects', [])
    hours = data.get('hours', 3)
    days = data.get('days', 7)
    
    if not subjects:
        return jsonify({'error': 'No subjects provided'}), 400
    
    # Create study plan
    plan = f"""📚 **Personalized Study Plan**
    
📖 **Subjects**: {', '.join(subjects)}
⏰ **Duration**: {days} days, {hours} hours per day

📅 **Weekly Schedule**:
• Monday/Wednesday: {subjects[0] if len(subjects) > 0 else 'Core subjects'}
• Tuesday/Thursday: {subjects[1] if len(subjects) > 1 else 'Theory subjects'}
• Friday: Review all topics
• Weekend: Rest and preview

💡 **Tips**:
1. Take 10-minute breaks every hour
2. Review previous day's material each morning
3. Practice with past papers
4. Stay hydrated and get enough sleep

🎯 **Success Strategy**: Consistency beats intensity! Study a little every day."""
    
    return jsonify({'plan': plan})

@app.route('/features')
def get_features():
    """Get features list"""
    features = [
        "📅 Personalized Study Schedules",
        "⏰ Smart Reminders & Deadlines",
        "🧠 Proven Study Techniques",
        "💪 Motivation & Stress Management",
        "📚 Exam Preparation Strategies",
        "🎯 Progress Tracking & Analytics"
    ]
    return jsonify({'features': features})

if __name__ == '__main__':
    print("="*60)
    print("🤖 DIGITAL STUDY BUDDY - HIDE HUMANITIES PROJECT")
    print("="*60)
    print(f"🎓 Created by: Naim Othmani & Yassin Oueslati")
    print(f"🤖 AI Mode: {'✅ Enabled' if AI_AVAILABLE else '⚠️ Smart Responses'}")
    print("🌐 Server: http://localhost:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
    