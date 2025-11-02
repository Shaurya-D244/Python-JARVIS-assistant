import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests 
import time
import openai

recognizer = sr.Recognizer()
newsapi = "47686f9ba06c41768d9e5904176ae998"
# API_KEY = "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"
openai.base_url = "https://openrouter.ai/api/v1"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def ask_ai(prompt):
        try:
            response = openai.chat.completions.create(
                model="gpt-4o-mini",  # You can change this model later
                messages=[
                    {"role": "system", "content": "You are JARVIS, an intelligent and helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            answer = response.choices[0].message.content
            return answer
        except Exception as e:
            return f"Error connecting to AI: {e}"
        
def processCommand(c):
    c = c.lower()
    if "open google" in c:
        webbrowser.open("https://www.google.com")
    elif "open youtube" in c:
        webbrowser.open("https://www.youtube.com")
    elif "open python" in c:
        webbrowser.open("https://www.python.org")
    elif "open code" in c:
        webbrowser.open("https://www.codewithharry.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        if song in musicLibrary.music:
            speak(f"Playing {song}")
            link = musicLibrary.music[song]
            webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")

        if r.status_code == 200:
            data = r.json()  # Convert response to dictionary
            articles = data.get("articles", [])  # Extract articles list
            
        if not articles:
            speak("Sorry, I couldn't find any news right now.")

        else:
            speak("Here are the top headlines:")
            for article in articles[:10]:  # Optional: limit to top 10 headlines
                speak(article["title"])
                time.sleep(0.5)
    
    else:
        speak("Let me think...")
        ai_response = ask_ai(c)
        print(ai_response)
        speak(ai_response)




if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    r = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source, timeout=2, phrase_time_limit=3)  # short timeout
                word = r.recognize_google(audio)
                print(f"You said: {word}")

                if word.lower() == "jarvis":
                    speak("Ya")
                    print("Jarvis Active...")
                    # Listen for command (longer phrase)
                    with sr.Microphone() as source:
                        audio = r.listen(source, timeout=None, phrase_time_limit=5)
                        command = r.recognize_google(audio)
                        print(f"Command: {command}")
                        processCommand(command)

        except sr.WaitTimeoutError:
            # Ignore timeout errors and continue listening
            continue
        except sr.UnknownValueError:
            # Could not understand audio
            continue
        except Exception as e:
            print("Error:", e)
            continue
