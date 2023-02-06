from happytransformer import HappyTextClassification

class SA:
    def __init__(self, enabled):
        self.enabled = enabled
        if self.enabled:
            self.model = HappyTextClassification(model_type = 'DISTILBERT', model_name = "distilbert-base-uncased-finetuned-sst-2-english", num_labels = 2)

    def run(self, text):
        if self.enabled:
            sent_detected = self.model.classify_text(text)
            sent_label = sent_detected.label
            sent_score = str(100 * round(sent_detected.score, 2))
            text_string = "There is a  " + sent_score + "% " + "likelihood that the tone of this message is " + sent_label
            print(text_string)
            return sent_label, sent_score
        return "TEST", 0