from src.txt_analizer import TextAnalyzer, Sentiment

class UserQuery:

    def __init__(self, user_interests: list[float], interests_text: str):
        self.user_interests = user_interests
        self.interests_text = interests_text
        self.positive_interests_array = []
        self.negative_interests_array = []
        self.interest_computed = False

    def positive_interests(self):
        if not self.interest_computed:
            self._compute_interests()
        return self.positive_interests_array

    def negative_interests(self):
        if not self.interest_computed:
            self._compute_interests()
        return self.negative_interests_array

    def _compute_interests(self):
        self.interest_computed = True
        text = self.interests_text

        previeous_sentiment = Sentiment.NEUTRAL

        # for each sub sentence in the text
        for sub in TextAnalyzer.sub_sentences(text):
            sentiment = TextAnalyzer.sentiment(sub)
            # find similar words
            words = []
            for word in TextAnalyzer.relevant_words(sub):
                words.append(word)
                for similar in TextAnalyzer.similar_words(word):
                    words.append(similar)

            if sentiment == Sentiment.POSITIVE:
                self.positive_interests_array.extend(words)
                previeous_sentiment = Sentiment.POSITIVE
            elif sentiment == Sentiment.NEGATIVE:
                self.negative_interests_array.extend(words)
                previeous_sentiment = Sentiment.NEGATIVE
            else:
                has_negation = TextAnalyzer.has_negation(sub)
                if previeous_sentiment == Sentiment.POSITIVE and not has_negation:
                    self.positive_interests_array.extend(words)
                    previeous_sentiment = Sentiment.POSITIVE
                elif previeous_sentiment == Sentiment.NEGATIVE and not has_negation:
                    self.negative_interests_array.extend(words)
                    previeous_sentiment = Sentiment.NEGATIVE
                elif previeous_sentiment == Sentiment.POSITIVE and has_negation:
                    self.negative_interests_array.extend(words)
                    previeous_sentiment = Sentiment.NEGATIVE
                elif previeous_sentiment == Sentiment.NEGATIVE and has_negation:
                    self.positive_interests_array.extend(words)
                    previeous_sentiment = Sentiment.POSITIVE