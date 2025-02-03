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
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report, accuracy_score

# NLTK-setup
nltk.download('punkt_tab')
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
    .str.replace('[^\w\s]', '', regex=True)     # Remove punctuation
    .str.replace('\d+', '', regex=True)         # Remove digits
    .str.replace('<.*?>', '', regex=True)       # Remove HTML tags
)

# Remove stopwords
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
    stemSentence = ""
    for word in sentence.split():
        stemSentence += stemmer.stem(word) + " "
    return stemSentence.strip()

data_raw['Heading'] = data_raw['Heading'].apply(stemming)

# Split the data
train, test = train_test_split(data_raw, random_state=42, test_size=0.30, shuffle=True)

train_text = train['Heading']
test_text = test['Heading']

# Vectorize using TF-IDF
vectorizer = TfidfVectorizer(strip_accents='unicode', 
                             analyzer='word', 
                             ngram_range=(1, 3), 
                             norm='l2')
vectorizer.fit(train_text)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels=['Id', 'Heading'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels=['Id', 'Heading'], axis=1)

# Define the parameter grid
param_grid = {
    'estimator__C': [0.1, 1, 10, 100, 1000, 10000],                 # Regularization strength
    'estimator__kernel': ['linear', 'rbf'],      # Kernel types
    'estimator__gamma': ['scale', 'auto'],       # Kernel coefficient for 'rbf'
}

# Create the OneVsRestClassifier with SVC
svc = OneVsRestClassifier(SVC(probability=True, random_state=42))

# Create the GridSearchCV instance
grid_search = GridSearchCV(
    estimator=svc,
    param_grid=param_grid,
    scoring='accuracy',  # Metric for optimization
    cv=3,                # Cross-validation folds
    verbose=2,           # Verbosity level
    n_jobs=-1            # Use all available CPU cores
)

# Perform Grid Search
grid_search.fit(x_train, y_train)

# Print the best parameters and best score
print(f"Bästa parametrar: {grid_search.best_params_}")
print(f"Bästa CV-score: {grid_search.best_score_:.2f}")

# Use the best model
best_model = grid_search.best_estimator_

# Predict on the test data
y_pred = best_model.predict(x_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy på testdata: {accuracy:.2f}")

report = classification_report(y_test, y_pred, target_names=categories)
print("Classification Report:")
print(report)
