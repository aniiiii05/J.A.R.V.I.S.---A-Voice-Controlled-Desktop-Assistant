import speech_recognition as sr

r = sr.Recognizer()
print("Listing microphones for verification...")
for i, name in enumerate(sr.Microphone.list_microphone_names() or []):
    print(i, name)

with sr.Microphone() as source:
    print("Calibrating mic...")
    r.adjust_for_ambient_noise(source, duration=1.0)
    print("Speak for up to 5 seconds...")
    try:
        audio = r.listen(source, timeout=8, phrase_time_limit=5)
        print("Got audio, recognizing...")
        text = r.recognize_google(audio)
        print("You said:", text)
    except sr.WaitTimeoutError:
        print("Timeout: no speech detected.")
    except sr.UnknownValueError:
        print("Heard audio but could not understand (UnknownValueError).")
    except sr.RequestError as e:
        print("API/request error:", e)
