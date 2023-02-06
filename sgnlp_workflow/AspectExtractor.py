from rake_nltk import Rake


class AspectExtractor:

    def __init__(self):
        pass

    def run(self, text):
        rake_nltk_var = Rake()
        rake_nltk_var.extract_keywords_from_text(text)
        keyword_extracted = rake_nltk_var.get_ranked_phrases()
        return keyword_extracted
