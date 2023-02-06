from happytransformer import HappyTextToText, TTSettings, HappyTextClassification

class SA:
    def __init__(self):
        self.model = HappyTextClassification(model_type = 'DISTILBERT', model_name = "distilbert-base-uncased-finetuned-sst-2-english", num_labels = 2)



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
