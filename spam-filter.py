import json
import keras
from keras.preprocessing.text import tokenizer_from_json
from pipeline import Pipeline
from config import MODEL_DIR, PRODUCTION


# 10.	Implementieren des eigentlichen Spam-Filters (Classifier)
class Classifier:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        # 3.1 Model lesen
        self.model = keras.models.load_model(self.model_dir)
        # self.model = keras.Sequential([self.model, tf.keras.layers.Softmax()])
        # 3.2 Tokenizer lesen
        with open(self.model_dir + '/tokenizer.json', "r") as f:
            json_tokenizer = json.load(f)

        self.tokenizer = tokenizer_from_json(json_tokenizer)

    def predict(self, mail_dir):
        # 3.2 Data Pipeline auf die Emails in der mail_dir anwenden (mittels der Klasse Pipeline)
        pipeline = Pipeline([mail_dir, ], tokenizer=self.tokenizer)
        email_liste, empty, empty, empty, empty = (pipeline.execute())
        # 3.3 Prediction anhand des geladenen Models
        confidence = self.model.predict(email_liste).flatten()
        predictions = (confidence > 0.5).astype("int32")
        return predictions.tolist(), confidence.tolist()


if __name__ == "__main__":
    classifier = Classifier(MODEL_DIR)
    print(classifier.predict(PRODUCTION))
