import io
import json
import tensorflow as tf
from keras.models import Sequential
from datetime import datetime
from data_pipeline import Pipeline
from conf import SPAM, NON_SPAM, MODEL_DIR


class Trainer:
    def __init__(self, spam, non_spam, model_dir):
        self.spam = spam
        self.non_spam = non_spam
        self.model_dir = model_dir

    def execute(self):
        # 2.1 Data Pipeline auf die Emails im Spam und Nicht-Spam-Ordner anwenden (mittels der Klasse Pipeline)
        pipeline_spam = Pipeline("data/email/email/Spam", label="Spam")
        pipeline_ham = Pipeline("data/email/email/non_spam", label="Non_Spam")
        spam_emails = pipeline_spam.execute()
        ham_emails = pipeline_ham.execute()
        # 2.2 Aufbau eines neuronalen Netzes mittels Keras
        model = Sequential()

        # 2.3 Einführen eines Tensorboard-Callbacks zur Visualisierung in Tensorflow
        log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

        # 2.4 Trainieren und validieren des Models

        # 2.5 Speichern des Modells

        # 2.6 Speichern des Tokenizers
        json.dump(tokenizer.to_json(), self.model_dir + '/tokenizer.json', ensure_ascii=False)
