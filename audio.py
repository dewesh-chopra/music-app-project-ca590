import speech_recognition as sr

def voice(lang):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio_data = r.record(source, duration=5)
        if lang=='1':
            content = r.recognize_google(audio_data, language='en-us')
        elif lang=='2':
            content = r.recognize_google(audio_data, language='hi-in')
        audiolist = [content, audio_data]
        return audiolist
