import os
import json
import uuid
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# Load environment variables from .env file
env_path = find_dotenv()
if env_path:
    load_dotenv(env_path)
    print(f"Loaded .env file from: {env_path}")
else:
    print("Warning: No .env file found")

# Get DeepSeek API key from environment
api_key = os.getenv('DEEPSEEK_API_KEY')
if not api_key or api_key == 'your_openrouter_api_key_here':
    raise ValueError("Please set your DEEPSEEK_API_KEY in the .env file")

print(f"Using DeepSeek API key: {api_key[:5]}...{api_key[-5:]}")

# Initialize OpenAI client for OpenRouter (DeepSeek)
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

app = Flask(__name__)
CORS(app)

# In-memory storage (replace with DB in production)
sessions = {}
messages = {}
SESSION_TTL_HOURS = 24

# Example Product catalog
PRODUCT_CATALOG = {
    "products": [
        {"id": 1, "name": "Sandalwood Incense", "price": "₹199", "description": "Pure sandalwood fragrance, pack of 50 sticks", "category": "Incense Sticks", "fragrance": "Woody"},
        {"id": 2, "name": "Rose Incense", "price": "₹179", "description": "Floral rose fragrance, pack of 50 sticks", "category": "Incense Sticks", "fragrance": "Floral"},
        {"id": 3, "name": "Jasmine Incense", "price": "₹189", "description": "Sweet jasmine fragrance, pack of 50 sticks", "category": "Incense Sticks", "fragrance": "Floral"},
        {"id": 4, "name": "Lavender Incense", "price": "₹209", "description": "Calming lavender fragrance, pack of 50 sticks", "category": "Incense Sticks", "fragrance": "Herbal"},
        {"id": 5, "name": "Nag Champa", "price": "₹229", "description": "Classic nag champa fragrance, pack of 50 sticks", "category": "Incense Sticks", "fragrance": "Floral"}
    ]
}

def get_llm_response(conversation_history):
    """Send messages to DeepSeek (via OpenRouter) and return AI response"""
    try:
        print("\n[DEBUG] Attempting to call DeepSeek API via OpenRouter...")

        # Ensure conversation history is in correct format
        messages_payload = [
            {"role": msg['role'], "content": msg['content']}
            for msg in conversation_history
        ]

        print(f"[DEBUG] Sending messages: {json.dumps(messages_payload, indent=2)}")

        # ✅ Correct SDK usage
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=messages_payload,
            temperature=0.7,
            max_tokens=300
        )

        print("[DEBUG] Successfully received response from DeepSeek")
        return response.choices[0].message.content.strip()

    except Exception as e:
        import traceback
        error_details = f"""
[ERROR] DeepSeek API call failed:
Type: {type(e).__name__}
Message: {str(e)}
Traceback:
{traceback.format_exc()}
"""
        print(error_details)
        return "⚠️ I'm sorry, I'm having trouble connecting to the AI service. Please try again shortly."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    session_id = data.get('session_id')
    user_message = data['message'].strip()
    current_time = datetime.now()

    # Session management
    is_new_session = False
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        is_new_session = True
        sessions[session_id] = {
            'created_at': current_time,
            'last_activity': current_time
        }
        messages[session_id] = []
    else:
        sessions[session_id]['last_activity'] = current_time

    # Add user message to history
    user_message_obj = {
        'role': 'user',
        'content': user_message,
        'timestamp': current_time.isoformat()
    }
    messages[session_id].append(user_message_obj)

    try:
        # Get LLM response
        conversation_history = [
            {'role': msg.get('role'), 'content': msg.get('content', '')}
            for msg in messages[session_id]
        ]

        bot_response = get_llm_response(conversation_history)

        # Store bot response
        bot_message_obj = {
            'role': 'assistant',
            'content': bot_response,
            'timestamp': datetime.now().isoformat()
        }
        messages[session_id].append(bot_message_obj)

        # Clean up old sessions
        cleanup_old_sessions()

        return jsonify({
            'session_id': session_id,
            'is_new_session': is_new_session,
            'response': bot_response,
            'messages': messages[session_id]
        })

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'session_id': session_id,
            'is_new_session': is_new_session,
            'response': "⚠️ I'm having trouble processing your request. Please try again later.",
            'error': str(e)
        }), 500

@app.route('/api/session/<session_id>', methods=['DELETE'])
def end_session(session_id):
    """End a chat session"""
    if session_id in sessions:
        sessions.pop(session_id, None)
        messages.pop(session_id, None)
        return jsonify({'status': 'success'})
    return jsonify({'status': 'session not found'}), 404

def cleanup_old_sessions():
    """Remove sessions that haven't been active for more than SESSION_TTL_HOURS"""
    current_time = datetime.now()
    expired_sessions = []

    for session_id, session_data in sessions.items():
        if current_time - session_data['last_activity'] > timedelta(hours=SESSION_TTL_HOURS):
            expired_sessions.append(session_id)

    for session_id in expired_sessions:
        sessions.pop(session_id, None)
        messages.pop(session_id, None)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
