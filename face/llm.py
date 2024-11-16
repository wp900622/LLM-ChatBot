import os
import google.generativeai as genai
from typing import Optional
from dotenv import load_dotenv, dotenv_values 
load_dotenv()
class ChatBot:
    def __init__(self, api_key: str):
        # 設定 API key
        genai.configure(api_key=api_key)
        
        # 初始化 Gemini-Pro 模型
        self.model = genai.GenerativeModel(model_name="gemini-pro")
        
        # 啟動聊天 session
        self.chat = self.model.start_chat()
        
    def send_message(self, message: str) -> Optional[str]:
        try:
            # 發送訊息並獲取回應
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
    
    def get_chat_history(self):
        # 獲取聊天歷史
        return self.chat.history

def main():
    # 從環境變數獲取 API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Please set GOOGLE_API_KEY environment variable")
    
    # 初始化聊天機器人
    chatbot = ChatBot(api_key)
    
    print("聊天機器人已啟動！輸入 'quit' 結束對話")
    
    while True:
        # 獲取用戶輸入
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            break
            
        # 獲取機器人回應
        response = chatbot.send_message(user_input)
        if response:
            print(f"Bot: {response}")
        
        # 可選：印出聊天歷史
        # print("\nChat History:")
        # for i, message in enumerate(chatbot.get_chat_history()):
        #     print(f"{i}: {message}")

if __name__ == "__main__":
    main()
