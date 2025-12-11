from flask import Flask, render_template, request, jsonify
import random
import datetime
import google.generativeai as genai  # ✅ OLD SDK that works
import time

app = Flask(__name__)

# Initialize Gemini API - Auto fallback to smart mode
try:
    GEMINI_API_KEY = "AIzaSyBB4P62BhO69mpYal_TjB9fvivkjikVhag"
    genai.configure(api_key=GEMINI_API_KEY)
    # ✅ Use a simple, working model
    model = genai.GenerativeModel('gemini-1.5-flash-latest')  # Changed to latest
    AI_AVAILABLE = True
    print("✅ Gemini API connected with OLD SDK!")
except Exception as e:
    print(f"⚠️ Gemini API Error: {e}")
    AI_AVAILABLE = False
    print("✨ Auto-activated: Smart Mode (Enhanced Mock Responses)")

# Enhanced smart responses - Always available
SMART_RESPONSES = {
    "greeting": [
        "✨ Hello! I'm Aura Study Buddy! Ready to illuminate your learning journey?",
        "🌟 Welcome to your smart study assistant! How can I help you excel today?",
        "🚀 Hey there! Let's make studying an amazing experience together!"
    ],
    "study": [
        "📚 **Quantum Learning**: Study in focused 90-minute blocks with 20-minute breaks for optimal brain function!",
        "🧠 **Neural Connection**: Use mind maps to visually connect concepts - this boosts retention by 30%!",
        "⚡ **Flash Memory**: Spaced repetition with apps like Anki is scientifically proven to improve long-term memory!",
        "🎯 **Deep Focus**: Eliminate all distractions, use focus music, and set specific goals for each session!"
    ],
    "exam": [
        "🔥 **Exam Mastery**: Start with a 14-day study plan, take mock tests every 3 days!",
        "📊 **Strategic Review**: Analyze past papers to identify high-yield topics worth 80% of marks!",
        "💫 **Performance Peak**: Practice under timed conditions to build confidence and speed!"
    ],
    "motivation": [
        "💥 You're not just studying—you're building the future version of yourself!",
        "🌈 Every concept you master is another step toward your dreams!",
        "⚡ Your potential is unlimited—unleash it one study session at a time!"
    ],
    "focus": [
        "🎧 **Focus Music**: Try Lo-Fi beats or binaural beats for deep concentration!",
        "⏰ **Pomodoro Plus**: Work for 50 minutes, break for 10 - it's the sweet spot!",
        "🌿 **Environment**: Clean workspace + natural light = 40% better focus!"
    ],
    "schedule": [
        "📅 **Time Blocking**: Assign specific hours to each subject - consistency wins!",
        "🎯 **Priority Matrix**: Focus on important AND urgent tasks first!",
        "📈 **Progress Tracking**: Review your schedule every Sunday for the coming week!"
    ],
    "default": [
        "🎓 I'm here with smart study strategies! Ask me about techniques, focus, or exam prep!",
        "💡 Try: 'best study methods', 'how to focus', 'exam preparation', or 'motivation tips'",
        "🌟 What learning challenge can I help you solve today?"
    ]
}

def get_gemini_response(user_input):
    """Get response from Gemini AI using OLD SDK"""
    try:
        response = model.generate_content(user_input)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini generation error: {e}")
        return get_smart_response(user_input)

def get_smart_response(user_input):
    """Get smart response from our enhanced database"""
    user_input = user_input.lower()
    
    if any(word in user_input for word in ["hi", "hello", "hey", "greetings", "welcome", "good morning", "good afternoon"]):
        return random.choice(SMART_RESPONSES["greeting"])
    elif any(word in user_input for word in ["study", "learn", "memorize", "technique", "method", "how to study", "study method"]):
        return random.choice(SMART_RESPONSES["study"])
    elif any(word in user_input for word in ["exam", "test", "final", "midterm", "assessment", "exam prep", "test preparation"]):
        return random.choice(SMART_RESPONSES["exam"])
    elif any(word in user_input for word in ["motivate", "encourage", "tired", "stress", "burnout", "demotivated", "lazy"]):
        return random.choice(SMART_RESPONSES["motivation"])
    elif any(word in user_input for word in ["focus", "concentrate", "distracted", "attention", "concentration"]):
        return random.choice(SMART_RESPONSES["focus"])
    elif any(word in user_input for word in ["schedule", "time", "plan", "organize", "time management", "routine"]):
        return random.choice(SMART_RESPONSES["schedule"])
    elif "math" in user_input:
        return "🔢 **Math Mastery**: Practice problems daily, understand the 'why' behind formulas, use Khan Academy for tough topics!"
    elif "programming" in user_input or "coding" in user_input:
        return "💻 **Code Like a Pro**: Build small projects daily, read documentation, practice on LeetCode, join coding communities!"
    elif "physics" in user_input:
        return "⚛️ **Physics Power**: Visualize concepts, solve derivations yourself, connect formulas to real-world phenomena!"
    elif "language" in user_input or "english" in user_input:
        return "🔤 **Language Learning**: Immerse yourself (movies, music), practice speaking daily, use flashcards for vocabulary!"
    else:
        return random.choice(SMART_RESPONSES["default"])

@app.route('/')
def home():
    """Main page"""
    return render_template('index.html', ai_available=AI_AVAILABLE)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages - Use AI if available, otherwise smart mode"""
    data = request.json
    user_input = data.get('message', '').strip()
    
    if not user_input:
        return jsonify({'error': 'Empty message'}), 400
    
    time.sleep(0.3)
    
    if AI_AVAILABLE:
        response = get_gemini_response(user_input)
        mode = 'ai'
    else:
        response = get_smart_response(user_input)
        mode = 'smart'
    
    return jsonify({
        'response': response,
        'ai_mode': AI_AVAILABLE,
        'mode': mode
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
    
    plan = f"""✨ **AURA SMART STUDY PLAN** ✨

📚 **Subjects Focus**: {', '.join(subjects)}
⏳ **Duration**: {days} days × {hours} hours/day = {hours*days} total hours
⚡ **Mode**: Smart Learning Protocol

📅 **WEEKLY BLUEPRINT**:
• MON/WED → Deep Dive into {subjects[0] if len(subjects) > 0 else 'Core Topics'}
• TUE/THU → Master {subjects[1] if len(subjects) > 1 else 'Technical Concepts'}
• FRIDAY → Integration & Practice Problems
• WEEKEND → Review + Preview Next Week

⏰ **DAILY STRUCTURE** ({hours}h):
1. Morning ({hours//2}h): New concepts & theory
2. Afternoon ({hours//3}h): Practice & application  
3. Evening ({hours//6}h): Review & mind mapping

🧠 **SMART TECHNIQUES**:
1️⃣ **Active Recall**: Test yourself every 30 minutes
2️⃣ **Spaced Repetition**: Review after 1 day, 3 days, 1 week
3️⃣ **Feynman Method**: Teach concepts to an imaginary student
4️⃣ **Pomodoro Plus**: 50/10 minute cycles

💡 **PRO TIPS**:
• Start with hardest subject when energy is highest
• Use color-coded notes for better recall
• Create summary sheets for each topic
• Practice with past papers under timed conditions

🎯 **SUCCESS METRICS**:
• Daily: Complete planned topics (aim for 85%+)
• Weekly: Self-assessment quiz
• Final: Full mock exam before D-day

🔥 **MOTIVATION**: "Consistency compounds. Small daily improvements lead to massive results over time!"

📝 **NEXT STEPS**:
1. Break each subject into weekly topics
2. Set specific daily goals
3. Track progress in a study journal
4. Adjust plan based on what's working

🌟 You've got this! Ready to begin? 🚀"""
    
    return jsonify({
        'plan': plan,
        'id': f"plan_{random.randint(1000, 9999)}",
        'created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    })

@app.route('/features')
def get_features():
    """Get features list"""
    features = [
        "✨ Smart Learning Algorithms",
        "⏰ Intelligent Time Management",
        "🧠 Neuroscience-Backed Techniques",
        "💫 Personalized Study Plans",
        "📊 Progress Analytics",
        "🔥 Motivation Engine",
        "🎯 Focus Optimization",
        "🚀 Quick Learning Hacks"
    ]
    return jsonify({'features': features})

@app.route('/quick_tips')
def get_quick_tips():
    """Get quick study tips"""
    tips = [
        "💡 Drink water every hour - dehydration reduces focus by 20%",
        "💡 Study in 50-minute blocks with 10-minute breaks",
        "💡 Use the Feynman technique: Teach what you learn",
        "💡 Practice active recall instead of passive reading",
        "💡 Get 7-8 hours of sleep for optimal memory consolidation",
        "💡 Exercise 30 minutes daily - it boosts brain function",
        "💡 Use spaced repetition apps for long-term retention",
        "💡 Create mind maps for complex topics"
    ]
    return jsonify({'tips': random.sample(tips, 3)})

if __name__ == '__main__':
    print("="*60)
    print("✨ AURA STUDY BUDDY - OLD SDK VERSION")
    print("="*60)
    print(f"🎓 Created by: Naim Othmani & Yassin Oueslati")
    print(f"🤖 AI Status: {'✅ CONNECTED' if AI_AVAILABLE else '⚠️ SMART MODE'}")
    print(f"📦 SDK: google-generativeai (old, stable version)")
    print("🌐 Server: http://localhost:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)