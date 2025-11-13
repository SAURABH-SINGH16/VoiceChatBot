import pyttsx3
import speech_recognition as sr
import webbrowser
import datetime
import pyjokes
import time

# ✅ Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)  # Use female voice if available
engine.setProperty('rate', 150)

def speechtx(text):
    """Convert text to speech and print it."""
    print("Autobot:", text)
    try:
        engine.stop()  # Stop any ongoing speech
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Speech Error: {e}")

def get_response(user_input):
    """Chatbot logic for speech version."""
    user_input = user_input.lower()
    reply = ""

    if "your name" in user_input:
        reply = "My name is Autobot, your voice assistant."

    elif "my name is" in user_input:
        name = user_input.split("my name is")[-1].strip().capitalize()
        reply = f"Hello {name}, nice to meet you!"

    elif "how old are you" in user_input:
        reply = "I’m still young, learning and evolving every day."

    elif "time" in user_input:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        reply = f"The current time is {time_now}."

    elif "joke" in user_input:
        reply = pyjokes.get_joke()

    elif "open youtube" in user_input:
        reply = "Opening YouTube..."
        webbrowser.open("https://www.youtube.com")

    elif "open google" in user_input:
        reply = "Opening Google..."
        webbrowser.open("https://www.google.com")

    elif "open instagram" in user_input:
        reply = "Opening Instagram..."
        webbrowser.open("https://www.instagram.com")

    elif "open amazon" in user_input:
        reply = "Opening Amazon..."
        webbrowser.open("https://www.amazon.in")

    elif "exit" in user_input or "stop" in user_input or "bye" in user_input:
        reply = "Goodbye! Have a great day!"
        speechtx(reply)
        time.sleep(1)
        exit()

    else:
        reply = "Sorry, I didn’t understand that. Could you repeat?"

    speechtx(reply)
    return reply


# ✅ Main Loop
if __name__ == "__main__":
    speechtx("Hello! My name is Autobot. How can I assist you today?")
    recognizer = sr.Recognizer()

    while True:
        with sr.Microphone() as source:
            print("\n🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.8)
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=6)
                data = recognizer.recognize_google(audio)
                print("You said:", data)
                get_response(data)
            except sr.WaitTimeoutError:
                print("⏳ No speech detected. Try again...")
            except sr.UnknownValueError:
                print("❌ Sorry, I could not understand the audio.")
            except sr.RequestError as e:
                print(f"⚠️ Could not request results; {e}")
