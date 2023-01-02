import json
import tensorflow as tf
from keras import layers
from keras.models import Sequential
from datetime import datetime
from pipeline import Pipeline
from config import EMBEDDING_DIM, MAXLEN, SPAM, NON_SPAM, MODEL_DIR

class Trainer:
    def __init__(self, spam, non_spam, model_dir):
        self.spam = spam
        self.non_spam = non_spam
        self.model_dir = model_dir

    def execute(self):
        # 2.1 Data Pipeline auf die Emails im Spam und Nicht-Spam-Ordner anwenden (mittels der Klasse Pipeline)
        pipeline = Pipeline([self.spam, self.non_spam], label=[1, 0], split=0.2)
        email_liste_train, email_liste_test, label_liste_train, label_liste_test, tokenizer = pipeline.execute()

        # 2.2 Aufbau eines Neuronalen Netzes mittels Keras
        model = Sequential()
        model.add(layers.Embedding(len(tokenizer.word_index) + 1, EMBEDDING_DIM, input_length=MAXLEN))
        model.add(layers.Conv1D(128, 5, activation='relu'))
        model.add(layers.GlobalMaxPool1D())
        model.add(layers.Dense(20, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        # 2.3 Einführen eines Tensorboard-Callbacks zur Visualisierung in Tensorflow
        log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

        # 2.4 Trainieren und validieren des Models
        model.fit(email_liste_train, label_liste_train, batch_size=16, epochs=40, validation_data=(email_liste_test, label_liste_test), callbacks=[tensorboard_callback])
        # 2.5 Speichern des Modells
        model.save(self.model_dir)
        # 2.6 Speichern des Tokenizers
        with open(self.model_dir + '/tokenizer.json', "w") as f:
            json.dump(tokenizer.to_json(), f, ensure_ascii=False)


if __name__ == "__main__":
    trainer = Trainer(SPAM, NON_SPAM, MODEL_DIR)
    trainer.execute()
