import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, classification_report

# NLTK settings
nltk.download('punkt')
nltk.download('stopwords')
nltk.data.path.append('C:\\Users\\Tobias E\\AppData\\Roaming\\nltk_data')

# Suppress warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Load the data
data_path = "C:\\workspace\\book1.csv"
data_raw = pd.read_csv(data_path, encoding='latin1')

# Shuffle the data
data_raw = data_raw.sample(frac=1)

# Identify category columns
categories = list(data_raw.columns.values)
categories = categories[2:]  # Adjust if your CSV structure changes

# Basic cleaning on the "Heading" column
data_raw['Heading'] = (
    data_raw['Heading']
    .str.lower()
    .str.replace('[^\w\s]', '', regex=True)     # remove punctuation
    .str.replace('\d+', '', regex=True)         # remove digits
    .str.replace('<.*?>', '', regex=True)       # remove HTML tags
)

# Stop-word removal
stop_words = set(stopwords.words('swedish'))

def removeStopWords(sentence):
    return " ".join(
        [word for word in nltk.word_tokenize(sentence) 
         if word not in stop_words]
    )

data_raw['Heading'] = data_raw['Heading'].apply(removeStopWords)

# Stemming
stemmer = SnowballStemmer("swedish")

def stemming(sentence):
    return " ".join([stemmer.stem(word) for word in sentence.split()])

data_raw['Heading'] = data_raw['Heading'].apply(stemming)

# Split the data
train, test = train_test_split(data_raw, random_state=42, test_size=0.30, shuffle=True)
train_text = train['Heading']
test_text = test['Heading']

# Vectorize using TF-IDF
vectorizer = TfidfVectorizer(strip_accents='unicode', 
                             analyzer='word', 
                             ngram_range=(1,3), 
                             norm='l2')
vectorizer.fit(train_text)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels=['Id', 'Heading'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels=['Id', 'Heading'], axis=1)

# Define Logistic Regression with OneVsRestClassifier
logistic_model = LogisticRegression(random_state=42)
one_vs_rest_classifier = OneVsRestClassifier(logistic_model)

# Set up GridSearchCV
param_grid = {
    'estimator__C': [0.1, 1, 10, 100, 1000, 10000],
    'estimator__penalty': ['l2'],
    'estimator__solver': ['lbfgs', 'liblinear'],
    'estimator__max_iter': [500, 1000, 5000]
}

grid_search = GridSearchCV(
    estimator=one_vs_rest_classifier,
    param_grid=param_grid,
    scoring='accuracy',
    cv=5,
    verbose=1,
    n_jobs=-1
)

# Perform Grid Search
grid_search.fit(x_train, y_train)

# Get the best model and parameters
print("Best Parameters:", grid_search.best_params_)
print("Best Cross-Validation Score:", grid_search.best_score_)

# Evaluate the best model on the test set
best_model = grid_search.best_estimator_
y_pred = best_model.predict(x_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy with Best Model: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=categories))
