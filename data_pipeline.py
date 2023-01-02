import tensorflow as tf
from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import one_hot
import email_import
import os


class Pipeline:
    def __init__(self, path_email, tokenizer=None, label=None):  # path_email = "data/email/email/"
        self.path_email = path_email
        self.tokenizer = tokenizer
        self.label = label

    def generate_tokenizer(self):
        # 1.1 Tokenizer erzeugen und trainieren
        if not self.tokenizer:
            pass

    def execute(self):
        # 1.2 Emails in Text-Emails konvertieren
        absolute_path = os.path.dirname(__file__)
        full_path = os.path.join(absolute_path, self.path_email)
        importer = email_import.Email_importer(full_path)
        text_emails = importer.get_text()
        # 1.3 Text in eine Token-Sequenz konvertieren
        tokens = [[] for None in range(len(text_emails))]
        # token generation
        for i, elem in enumerate(text_emails):
            words = text_to_word_sequence(elem)
            length = len(words)
            tokens[i] = one_hot(elem, round(length * 2))

        # 1.4 Padding der Token-Sequenz
        padded_list = tf.keras.preprocessing.sequence.pad_sequences(tokens, padding="post")

        # 1.5 Labeling der E-Mails
        if self.label:
            labels = [str(self.label) for None in range(len(padded_list))]
        else:
            labels = None
        # Ausgabe: Zwei Listen: Liste E-Mails als Token-Sequenz und Liste entsprechender Labels, Falls label=None:
        # zweite Liste ist None
        return padded_list, labels
