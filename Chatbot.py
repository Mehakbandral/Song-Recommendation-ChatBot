import numpy as np
from keras.models import load_model
import random
import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle

class Chatbot:
    def __init__(self):
        # Download NLTK resources required for text processing
        nltk.download('punkt')
        nltk.download('wordnet')

        # Load intents from JSON file
        intents_file = open('./filesrequired/intents.json').read()
        self.intents = json.loads(intents_file)

        # Initialize lemmatizer, words, classes, and documents lists
        self.lemmatizer = WordNetLemmatizer()
        self.words = []
        self.classes = []
        self.documents = []

        # Extract words, classes, and documents from intents
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                word = nltk.word_tokenize(pattern)
                self.words.extend(word)
                self.documents.append((word, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        # Preprocess words: lemmatize and convert to lowercase
        self.words = [self.lemmatizer.lemmatize(w.lower()) for w in self.words]
        self.words = sorted(list(set(self.words)))
        self.classes = sorted(list(set(self.classes)))

        # Prepare training data
        training = []
        output_empty = [0] * len(self.classes)

        # Create training data with bag of words representation
        for doc in self.documents:
            bag = []
            word_patterns = doc[0]
            word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in self.words:
                bag.append(1) if word in word_patterns else bag.append(0)
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            training.append([bag, output_row])

        # Convert training data to NumPy array with object dtype
        self.training = np.array(training, dtype=object)

        # Load model, words, and classes from files
        self.model = load_model('./filesrequired/chatbot_model.h5')
        self.words = pickle.load(open('./filesrequired/words.pkl', 'rb'))
        self.classes = pickle.load(open('./filesrequired/classes.pkl', 'rb'))

    # Functions to preprocess and predict
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence, show_details=True):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [1 if word in sentence_words else 0 for word in self.words]
        return np.array(bag)

    def predict_class(self, sentence):
        # Get bag of words representation
        p = self.bag_of_words(sentence, show_details=False)
        # Predict class probabilities
        res = self.model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        # Filter predictions above the threshold
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        # Sort predictions by probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(self, ints):
        tag = ints[0]['intent']
        list_of_intents = self.intents['intents']
        # Retrieve a random response for the predicted intent
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result

    # Main response function
    def respond(self, msg1):
        # Predict the intent for the user message
        ints = self.predict_class(msg1)
        if not ints:
            # Handle the case where no intent is predicted
            return "I'm sorry, I'm not sure how to respond to that."
        # Get a response based on the predicted intent
        res = self.getResponse(ints)
        return res

"""# Create an instance of the Chatbot class
chatbot = Chatbot()

# Start conversation loop
print("Chatbot : Hey there, Wassup ?")
for _ in range(5):
    user_input = input("User : ")
    response = chatbot.respond(user_input)
    print("Chatbot : " + response)
"""
