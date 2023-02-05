## Packages for speech recognition and sentiment analysis
import speech_recognition as sr
from happytransformer import HappyTextToText, TTSettings, HappyTextClassification
## Packages for reading out the result
import gtts
from playsound import playsound

# Initialise the recognizer
r = sr.Recognizer()

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source, 1)
    print("Recording")
    # Read the audio data from the default microphone for 15s
    audio_data = r.record(source, duration=15)

    try:
        print("Recognising...")
        # Convert speech to text
        text = r.recognize_google(audio_data)
        print('Printing text')
        print(text)
    except sr.UnknownValueError:
        print("Could not hear that, please repeat what you said")

# Create transformer for grammar correction 
grammar_transformer = HappyTextToText("T5",  "prithivida/grammar_error_correcter_v1")
# Customise algorithm used for grammar correction => 100 tokens considered before correction is made
settings = TTSettings(do_sample=True, top_k=100, temperature=0.5, min_length = 1, max_length=100) 
# Process text 
processed_obj = grammar_transformer.generate_text(text, args=settings)
corrected_text = processed_obj.text
# Print processed text 
print("Printing processed text")
print(corrected_text)

# Carry out sentiment analysis on processed text 
sent_analysis_model = HappyTextClassification(model_type = 'DISTILBERT', model_name = "distilbert-base-uncased-finetuned-sst-2-english", num_labels = 2)
sent_detected = sent_analysis_model.classify_text(corrected_text)
sent_label = sent_detected.label
sent_score = str(100 * round(sent_detected.score, 2))
text_string = "Based on the analysis by sign e fai, there is a  " + sent_score + "% " + "likelihood that the tone of this message is " + sent_label
print(text_string)

# Read out the result of the sentiment analysis 
text_to_speech_fn = gtts.gTTS(text_string)
text_to_speech_fn.save("text_analysis.mp3")
playsound("text_analysis.mp3")
