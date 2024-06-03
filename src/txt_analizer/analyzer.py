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
glove_model = KeyedVectors.load_word2vec_format(os.path.abspath('./data/glove.6B.50d.w2vformat.txt'))


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
        """
        Find the sentiment of the text.
        :param text:
        :return: sentiment of the text (positive, negative, neutral, both)
        """
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
        """
        Find the most similar words to the given word.
        :param word:
        :param num:
        :return: list of num similar words
        """
        try :
            # consider only the word and not the similarity score
            words = [x[0] for x in glove_model.most_similar(word)[:num]]
            return words
        except KeyError:
            # if the word is not in the vocabulary
            return []

    @staticmethod
    def separator_words(text: str) -> list[str]:
        """
        Find the separators in the text.
        :param text:
        :return: list of separators
        """
        separators_words_in_text = re.findall("\.|\!|\?|\;|\,|\:|but|and", text)
        return separators_words_in_text

    @staticmethod
    def sub_sentences(text: str) -> list[str]:
        """
        Extract the sub-sentences from the text.
        :param text:
        :return: list of sub-sentences
        """

        # find the separators in the text
        separators_words_in_text = TextAnalyzer.separator_words(text)

        sub_sentences = []

        for sep in separators_words_in_text:
            # find the index of the separator
            sep_index = text.index(sep)
            # add the sub-sentence to the list
            left = text[:sep_index]
            sub_sentences.append(left)
            # remove the sub-sentence from the text
            right = text[sep_index:]
            text = right

        # add the last sub-sentence
        sub_sentences.append(text)

        return sub_sentences

    @staticmethod
    def relevant_words(text: str) -> list[str]:
        """
        Extract the relevant words from the text.
        :param text:
        :return: list of relevant words
        """
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
    def has_negation(text: str) -> bool:
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