import speech_recognition as sr
import webbrowser
import pyttsx3
import sys
import musiclib
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "576413c49d2746418849d87ad2c2fce3"

def speak(text: str) -> None:
    engine.say(text)
    engine.runAndWait()

def processCommand(c: str) -> None:
    cl = c.lower().strip()
    if "open google" in cl:
        webbrowser.open("https://google.com")
        speak("Opening Google")
    elif "open youtube" in cl:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
    elif "open gmail" in cl:
        webbrowser.open("https://mail.google.com")
        speak("Opening Gmail")
    elif "open linkedin" in cl:
        webbrowser.open("https://linkedin.com")
        speak("Opening LinkedIn")
    elif cl.startswith("play"):
        parts = cl.split()
        if len(parts) >= 2:
            song = " ".join(parts[1:])  # support multi-word titles
            try:
                link = musiclib.music[song]
                webbrowser.open(link)
                speak(f"Playing {song}")
            except KeyError:
                speak(f"I couldn't find {song} in the music library.")
        else:
            speak("Please say the song name after play.")
    elif "news" in cl:
        try:
            r = requests.get(
                f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}",
                timeout=10
            )
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])[:5]
                if not articles:
                    speak("No news articles available.")
                for article in articles:
                    title = article.get('title') or "Untitled article"
                    speak(title)
            else:
                speak("News service returned an error.")
        except requests.RequestException:
            speak("Network problem while fetching news.")
    else:
        speak("Sorry, I didn't understand that command.")

def listen_once(r: sr.Recognizer, source: sr.Microphone, timeout=8, phrase_time_limit=5) -> str:
    # brief calibration before each capture helps a lot
    r.adjust_for_ambient_noise(source, duration=0.3)
    audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
    return r.recognize_google(audio)  # requires internet

if __name__ == "__main__":
    speak("Initializing Jarvis in 3... 2... 1...")
    try:
        # Optional: pick a specific mic if default is wrong
        # print(sr.Microphone.list_microphone_names())
        # mic = sr.Microphone(device_index=YOUR_INDEX)
        mic = sr.Microphone()

        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            speak("Jarvis is ready. Say 'Jarvis' to activate.")

        while True:
            print("Waiting for wake word 'Jarvis'...")
            try:
                with mic as source:
                    print("Listening for wake word...")
                    wake_text = listen_once(recognizer, source, timeout=10, phrase_time_limit=2)
                    print(f"Heard wake candidate: {wake_text!r}")
            except sr.WaitTimeoutError:
                continue  # keep waiting
            except sr.UnknownValueError:
                continue  # heard audio but couldn't parse; keep waiting
            except sr.RequestError as e:
                print(f"Recognition service error (wake): {e}")
                speak("Recognition service error.")
                continue

            norm = wake_text.strip().lower()
            if ("jarvis" in norm) or (norm == "jarvis"):
                speak("Yes?")
                try:
                    with mic as source:
                        print("Jarvis active. Listening for command...")
                        command_text = listen_once(recognizer, source, timeout=10, phrase_time_limit=7)
                        print(f"Command: {command_text!r}")
                        processCommand(command_text)
                except sr.WaitTimeoutError:
                    speak("I didn't hear any command.")
                except sr.UnknownValueError:
                    speak("Sorry, I didn't catch that.")
                except sr.RequestError as e:
                    print(f"Recognition service error (command): {e}")
                    speak("Recognition service error.")

    except KeyboardInterrupt:
        print("\nExiting.")
        speak("Goodbye.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred. Please check the console.")
