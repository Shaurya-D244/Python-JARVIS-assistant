import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import time
import json

# --- Configuration ---
NEWS_API_KEY = "NEWS_API"  # You can search News API on your web browser
OPENROUTER_KEY = "API_KEY" # You can use OpenAI


# --- Functions ---
def speak(text):
    # Initialize TTS engine once
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.3)  # small pause after speaking

def ask_ai(prompt):
    """Send a prompt to OpenRouter AI via requests and return the response."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        r = requests.post(url, headers=headers, data=json.dumps(payload), timeout=20)
        r.raise_for_status()
        data = r.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f"Error connecting to AI: {e}"

def processCommand(c):
    c = c.lower()

    # --- Web commands ---
    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "open python" in c:
        speak("Opening Python.org")
        webbrowser.open("https://www.python.org")
    elif "open code" in c:
        speak("Opening CodeWithHarry")
        webbrowser.open("https://www.codewithharry.com/")

    # --- Music ---
    elif c.startswith("play "):
        song = c.split(" ", 1)[1]
        if song in musicLibrary.music:
            speak(f"Playing {song}")
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak(f"Sorry, I don't have {song} in the library.")

    # --- News ---
    elif "news" in c:
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}")
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            if not articles:
                speak("Sorry, I couldn't find any news right now.")
            else:
                speak("Here are the top headlines:")
                for article in articles[:5]:
                    speak(article["title"])
                    time.sleep(0.5)
        else:
            speak("Sorry, I couldn't fetch the news right now.")

    # --- AI handling ---
    else:
        speak("Let me think...")
        ai_response = ask_ai(c)
        print(f"AI response: {ai_response}")
        speak(ai_response)

# --- Main loop ---
if __name__ == "__main__":
    recognizer = sr.Recognizer()
    speak("Initializing Jarvis...")

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                word = recognizer.recognize_google(audio)
                print(f"You said: {word}")

                if word.lower() == "jarvis":
                    speak("Yes?")
                    print("Jarvis Active...")
                    with sr.Microphone() as source:
                        audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)
                        command = recognizer.recognize_google(audio)
                        print(f"Command: {command}")
                        processCommand(command)

        except sr.WaitTimeoutError:
            continue
        except sr.UnknownValueError:
            continue
        except Exception as e:
            print("Error:", e)

            continue
