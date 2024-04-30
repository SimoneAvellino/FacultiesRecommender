import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from gensim.models import KeyedVectors
import os
import nltk.data
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

sentiment_analyzer = SentimentIntensityAnalyzer()
glove_model = KeyedVectors.load_word2vec_format(os.path.abspath('../data/glove.6B.50d.w2vformat.txt'))


class Sentiment:
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    NEUTRAL = 'neutral'
    BOTH = 'both'


class TextAnalyzer(object):

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super(TextAnalyzer, self).__new__(self)
        return self.instance

    @staticmethod
    def sentiment(text: str) -> str:
        polarity = sentiment_analyzer.polarity_scores(text)
        if polarity['pos'] > 0 and polarity['neg'] == 0:
            return Sentiment.POSITIVE
        elif polarity['neg'] > 0 and polarity['pos'] == 0:
            return Sentiment.NEGATIVE
        elif polarity['pos'] > 0 and polarity['neg'] > 0:
            return Sentiment.BOTH
        elif polarity['neu'] == 1:
            return Sentiment.NEUTRAL

    @staticmethod
    def similar_words(word: str, num=3) -> list[str]:
        # consider only the word and not the similarity score
        words = [x[0] for x in glove_model.most_similar(word)[:num]]
        return words

    @staticmethod
    def sub_sentences(text: str) -> list[str]:
        # Create a regex pattern that matches any of the separators
        separators = [r'\.', r'\!', r'\?', r'\;', r'\,', r'\:', r'but', r'and']
        pattern = '|'.join(separators)

        # Split the sentence into sub_sentences using the pattern
        sub_sentences = re.split(pattern, text)

        # Add the separator back to the next subsentence
        sub_sentences = [separator + subsentence for subsentence, separator in
                        zip(sub_sentences[1:], re.findall(pattern, text)) if len(subsentence.strip()) > 0]

        # The first subsentence does not have a separator, so we add an empty string
        sub_sentences.insert(0, text[:text.index(sub_sentences[0])])

        # Create a Sentence object for each subsentence
        sub_sentences = [subsentence.strip() for subsentence in sub_sentences if subsentence.strip()]

        return sub_sentences

    @staticmethod
    def relevant_words(text: str) -> list[str]:
        tokens = nltk.word_tokenize(text)
        tagged_tokens = nltk.pos_tag(tokens)
        relevant_words = []
        for token in tagged_tokens:
            if token[1].startswith('NN'):
                relevant_words.append(token[0])
            elif token[1].startswith('VB') or token[1].startswith('JJ'):
                # obtain the noun form of the verb
                lemma = WordNetLemmatizer().lemmatize(token[0], wordnet.VERB)
                if lemma != token[0]:
                    relevant_words.append(lemma)
        return relevant_words

    @staticmethod
    def has_negation(text):
        """
        Check if the sentence contains a negation word.
        """
        negations = ['not', 'no', 'never', 'none', 'but', 'n\'t']
        tokens = nltk.word_tokenize(text)
        for token in tokens:
            for negation in negations:
                if token.__contains__(negation):
                    return True
        return False
