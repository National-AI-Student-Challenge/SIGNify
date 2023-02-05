### LIVE SPEECH --> SPEECH TO TEXT FUNTIONALITY ##

## Website: https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
import speech_recognition as sr

# initialise the recognizer
r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, 1)
    print("Recording")
    # read the audio data from the default microphone for 15s
    audio_data = r.record(source, duration=15)

    try:
        print("Recognizing...")
        # Convert speech to text
        text = r.recognize_google(audio_data)
        print('Printing text')
        print(text)
    except sr.UnknownValueError:
        print("Could not hear that, please repeat what you said")

