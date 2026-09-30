from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from chatbot_config import CHATBOT_NAME, SYSTEM_INSTRUCTION

app = Flask(__name__)

# Configure Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback to local config or environment variable
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
    except ImportError:
        pass

if api_key:
    genai.configure(api_key=api_key)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION
)

@app.route("/")
def index():
    return render_template("index.html", chatbot_name=CHATBOT_NAME)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"response": "Please enter a message."}), 400
    
    try:
        response = model.generate_content(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error interacting with Gemini API: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
