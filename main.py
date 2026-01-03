from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

def get_chatbot_logic(question):
    """Aapke original gpt.py ka logic"""
    english_instruction = "Please respond in English. "
    enhanced_question = english_instruction + question
    
    payload = {
        'messages': [
            {'role': 'assistant', 'content': 'Hello! How can I help you today?'},
            {'role': 'user', 'content': enhanced_question}
        ]
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36...',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    url = 'https://chatbot-ji1z.onrender.com/chatbot-ji1z'

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            api_response = response.json()
            return api_response['choices'][0]['message']['content']
        return f"API Error: {response.status_code}"
    except Exception as e:
        return str(e)

@app.route('/')
def home():
    return jsonify({"status": "API is Live", "endpoint": "/chat"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    # hackGPT 'message' ya 'question' dono handle karega
    user_query = data.get('message') or data.get('question')
    
    if not user_query:
        return jsonify({"error": "No message provided"}), 400
    
    response_text = get_chatbot_logic(user_query)
    
    # hackGPT ke format ke hisab se response bhej raha hoon
    return jsonify({
        "answer": response_text,
        "response": response_text,
        "status": "success"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
