from src.txt_analizer import TextAnalyzer, Sentiment
import questionary
import os
from IPython.display import clear_output

questions = {
    "Quale tipologia d'istituto superiore hai frequentato?": {
        "Artistico": -4,
        "Musicale": -3,
        "Classico": -2,
        "Linguistico": -1,
        "Scienze umane": 0,
        "Economico": 1,
        "Tecnologico": 2,
        "Scientifico": 3,
        "Professionale": 4
    },
    "Preferisco studiare materie:": {
        "Scientifiche": 1,
        "Umanistiche": -1
    },
    "Preferisco:": {
        "Pratica": 0,
        "Teoria": 1
    },
    "Studio perché voglio aiutare le persone dal punto di vista: (ciò che preferisci di più)": {
        "artistico (es. Stilista, Designer, ...)": -5,
        "culinario (es. Cuoco, ...)": -4,
        "turistico (es. Guida Turistica, ...)": -3,
        "sociale (es. Assistente Sociale, ...)": -2,
        "educativo (es. Insegnante, ...)": -1,
        "civile (es. Avvocato, Politico, ...)": 0,
        "ambientale (es. Agricoltore, Attivista, ...)": 1,
        "economico (es. Impiegato in banca, Economista, ...)": 2,
        "tecnologico (es. Sviluppatore, Progettista, ...)": 3,
        "sanitario (es. Dottore, Infermiere, Psicologo, ...)": 4,
        "della ricerca (es. Fisico, Matematico, Storico, ...)": 5
    },
    "Mi soddisfa più: (ciò che preferisci di più)": {
        "creare": -3,
        "comunicare": -2,
        "progettare": -1,
        "comprendere": 0,
        "analizzare": 1,
        "ricercare": 2,
        "aiutare": 3
    },
    "Quando studio, mi piace avere più risposte per la stessa domanda:": {
        "No": -1,
        "Sì": 1
    },
    "Fra questi obiettivi mi rispecchio più in: (ciò che preferisci di più)": {
        "espandere le mie conoscenze e competenze": -3,
        "fare carriera": -2,
        "esplorare nuove culture": -1,
        "esprimere la mia creatività ed originalità": 0,
        "contribuire al benessere degli altri": 1,
        "fare una differenza nel mondo": 2,
        "promuovere la giustizia": 3,
        "promuovere l'innovazione ed il cambiamento": 4
    },
    "In quale ambiente di lavoro ti senti più a tuo agio?": {
        "Un ambiente creativo e innovativo": -3,
        "Un ambiente dinamico e stimolante": -2,
        "Un ambiente collaborativo e team-oriented": -1,
        "Un ambiente multiculturale e diversificato": 0,
        "Un ambiente autonomo e indipendente": 1,
        "Un ambiente strutturato e ben organizzato": 2
    }
}


class UserQuery:

    def __init__(self, user_interests: list[float], interests_text: str):
        self.user_interests = user_interests
        self.interests_text = interests_text
        self.positive_interests_array = []
        self.negative_interests_array = []
        self.interest_computed = False

    def ask_quetions(self):
        """
        Ask the user the questions of the questions and the interests text
        :return:
        """
        # reset user interests
        self.interests_text = input("Write your interests: ")
        print("\nAnswer the following questions:")
        self.user_interests = []
        for question, options in questions.items():
            choices = list(options.keys())
            answer = questionary.select(question, choices=choices).ask()
            self.user_interests.append(options[answer])
        print(self.user_interests)

    def ask_quetions_on_jupiter(self):

        print("\nAnswer the following questions:")
        for question in questions.keys():
            print(question)
            options = list(questions[question].keys())
            for i, option in enumerate(options):
                print(i + 1, ")", option)
            answer = input("Type the number for the answer: ")
            self.user_interests.append(questions[question][options[int(answer)-1]])
            # clear_output(wait=True)

        self.interests_text = input("Write your interests: ")
        clear_output(wait=True)

    def show_interests(self):
        print("Interest text:\n", self.interests_text, "\n\n")
        print("Answers to the questions:\n")
        for i, question in enumerate(questions.keys()):
            possible_answers = questions[question]
            # extract the answer where the index is the answer
            j = 0
            for value in possible_answers.values():
                if value == self.user_interests[i]:
                    break
                j += 1
            print(f" {i + 1})", question, ":", list(possible_answers.keys())[j])

    def positive_interests(self):
        if not self.interest_computed:
            self._compute_interests()
        return self.positive_interests_array

    def negative_interests(self):
        if not self.interest_computed:
            self._compute_interests()
        return self.negative_interests_array

    def _compute_interests(self):
        """
        Compute the interests from the text
        :return: void
        """
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