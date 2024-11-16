import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class ChatBot:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        self.chat = self.model.start_chat(history=[])

    def send_message(self, message: str) -> Optional[str]:
        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            print(f"Error in send_message: {str(e)}")
            return None

# 建立 Flask 應用
app = Flask(__name__,template_folder=os.path.abspath('templates'))

# 建立全域的 chatbot 實例
chatbot = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        global chatbot
        if chatbot is None:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                return jsonify({"error": "API key not found"}), 400
            chatbot = ChatBot(api_key)
        
        message = request.json.get('message')
        is_edit = request.json.get('isEdit', False)
        original_message = request.json.get('originalMessage')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        if is_edit:
            # 如果是編輯消息，可以添加特殊處理邏輯
            context = f"原始訊息是: '{original_message}'\n使用者編輯為: '{message}'\n請根據編輯後的訊息重新回應。"
            response = chatbot.send_message(context)
        else:
            response = chatbot.send_message(message)
            
        return jsonify({"response": response})
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)