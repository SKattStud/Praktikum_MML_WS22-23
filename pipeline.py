import numpy as np
from sklearn.model_selection import train_test_split
from email_import import Email_importer
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from config import MAXLEN, SPAM, NON_SPAM


class Pipeline:
    def __init__(self, paths_email, tokenizer=None, label=None, split=None):
        self.paths_email = paths_email
        self.tokenizer = tokenizer
        self.label = label
        self.split = split

    def execute(self):
        pass
        # 1.1 Emails in Text-Emails konvertieren
        email_listen = [Email_importer(path).get_text() for path in self.paths_email]
        email_liste = np.array(sum(email_listen, []))
        # 1.2 Emails labeln (nur im Fall T)
        if self.label is not None:
            label_liste = np.array(sum([[self.label[i], ]*len(email_listen[i]) for i in range(len(self.label))], []))
            # 1.3 Splitting in Trainings- und Testdaten (Validierungsdaten) (nur im Fall T)
            email_liste_train, email_liste_test, label_liste_train, label_liste_test = train_test_split(email_liste, label_liste, test_size=self.split, shuffle=True)
        else:
            email_liste_train, email_liste_test, label_liste_train, label_liste_test = email_liste, np.array([]), np.array([]), np.array([])
        # 1.4 Tokenizer mit Trainingsmenge generieren (nur im Fall T)
        if self.tokenizer is None and self.label is not None:
            self.tokenizer = Tokenizer(num_words=5000)
            self.tokenizer.fit_on_texts(email_liste_train)

        # 1.5 Text in eine Token-Sequenz konvertieren
        email_liste_train = self.tokenizer.texts_to_sequences(email_liste_train)
        email_liste_test = self.tokenizer.texts_to_sequences(email_liste_test)
        # 1.6 Padding der Token-Sequenz
        email_liste_train = pad_sequences(email_liste_train, maxlen=MAXLEN)
        email_liste_test = pad_sequences(email_liste_test, maxlen=MAXLEN)
        # Ausgabe: Zwei Listen:
        # Liste E-Mails als Token-Sequenz und Liste entsprechender Labels, Falls label=None: zweite Liste ist None
        return email_liste_train, email_liste_test, label_liste_train, label_liste_test, self.tokenizer


if __name__ == "__main__":
    pipeline = Pipeline([SPAM, NON_SPAM], label=[1, 0])
    result = pipeline.execute()
