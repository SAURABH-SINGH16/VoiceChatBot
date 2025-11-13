from flask import Flask, render_template, request, jsonify
import pyttsx3
import datetime
import pyjokes

# ✅ Flask setup
app = Flask(__name__, template_folder='templates', static_folder='static')

# ✅ Text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

def speak(text):
    """Speak text using pyttsx3 (server-side optional)"""
    try:
        engine.stop()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS Error: {e}")

def chatbot_reply(text):
    """Chatbot logic"""
    text = text.lower().strip()
    reply = ""
    link = None  # Optional URL to open in browser

    # --- Basic Q&A ---
    if "your name" in text:
        reply = "My name is Autobot, your personal assistant."

    elif "how old are you" in text:
        reply = "I’m still quite new — learning and improving every day!"

    elif "time" in text:
        reply = f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."

    elif "joke" in text:
        reply = pyjokes.get_joke()

    elif "my name is" in text:
        user_name = text.split("my name is")[-1].strip().capitalize()
        reply = f"Hello {user_name}, nice to meet you!"

    # --- Website commands ---
    elif "open youtube" in text:
        reply = "Opening YouTube..."
        link = "https://www.youtube.com"

    elif "open google" in text:
        reply = "Opening Google..."
        link = "https://www.google.com"

    elif "open instagram" in text:
        reply = "Opening Instagram..."
        link = "https://www.instagram.com"

    elif "open amazon" in text:
        reply = "Opening Amazon..."
        link = "https://www.amazon.in"

    elif "exit" in text or "stop" in text or "bye" in text:
        reply = "Goodbye! Have a great day!"

    else:
        reply = "Sorry, I didn’t understand that. Can you please repeat?"

    # Speak server-side (optional)
    speak(reply)

    return {"reply": reply, "link": link}


# --- Flask Routes ---
@app.route("/")
def home():
    return render_template("chatbot.html")


@app.route("/get", methods=["POST"])
def get_bot_response():
    try:
        data = request.get_json()
        user_input = data.get("message", "")
        if not user_input:
            return jsonify({"reply": "Please type something.", "link": None})
        response_data = chatbot_reply(user_input)
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"reply": f"Error: {e}", "link": None})


# ✅ Main entry point
if __name__ == "__main__":
    app.run(debug=True, port=5000)
