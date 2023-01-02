import io
import json
import tensorflow as tf
from keras.preprocessing.text import tokenizer_from_json
from data_pipeline import Pipeline
from conf import MODEL_DIR


# 10.	Implementieren des eigentlichen Spam-Filters (Classifier)
class Classifier:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        # 3.1 Model lesen

        # 3.2 Tokenizer lesen
        json_tokenizer = json.load(self.model_dir)

        tokenizer = tokenizer_from_json(json_tokenizer)

    def predict(self, mail_dir):
        pass
        # 3.2 Data Pipeline auf die Emails in der mail_dir anwenden (mittels der Klasse Pipeline)

        # 3.3 Prediction anhand des geladenen Models
