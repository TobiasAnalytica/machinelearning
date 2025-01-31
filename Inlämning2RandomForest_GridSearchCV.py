import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import GridSearchCV

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Specify the path to your NLTK data (if required)
nltk.data.path.append('C:\\Users\\Tobias E\\AppData\\Roaming\\nltk_data')

# Suppress all warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Load the dataset
data_path = "C:\\workspace\\book1.csv"  # Update with the correct file path
data_raw = pd.read_csv(data_path, encoding='latin1')

# Shuffle the data
data_raw = data_raw.sample(frac=1)

# Identify category columns (update as per your dataset structure)
categories = list(data_raw.columns.values)
categories = categories[2:]  # Assuming categories start from the third column

# Clean the "Heading" column
data_raw['Heading'] = (
    data_raw['Heading']
    .str.lower()
    .str.replace('[^\w\s]', '', regex=True)     # Remove punctuation
    .str.replace('\d+', '', regex=True)         # Remove digits
    .str.replace('<.*?>', '', regex=True)       # Remove HTML tags
)

# Define stop words and a function to remove them
stop_words = set(stopwords.words('swedish'))

def removeStopWords(sentence):
    return " ".join(
        [word for word in nltk.word_tokenize(sentence) if word not in stop_words]
    )

data_raw['Heading'] = data_raw['Heading'].apply(removeStopWords)

# Apply stemming using SnowballStemmer
stemmer = SnowballStemmer("swedish")

def stemming(sentence):
    stem_sentence = ""
    for word in sentence.split():
        stem_sentence += stemmer.stem(word) + " "
    return stem_sentence.strip()

data_raw['Heading'] = data_raw['Heading'].apply(stemming)

# Split the data into training and testing sets
train, test = train_test_split(data_raw, random_state=42, test_size=0.30, shuffle=True)
train_text = train['Heading']
test_text = test['Heading']

# Vectorize the text data using TF-IDF
vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1, 3), norm='l2')
vectorizer.fit(train_text)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels=['Id', 'Heading'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels=['Id', 'Heading'], axis=1)

# Define a parameter grid for Random Forest tuning
param_grid = {
    'estimator__n_estimators': [100, 200, 300, 400],  # Number of trees in the forest
    'estimator__max_depth': [None, 10, 20, 30],  # Maximum depth of the trees
    'estimator__min_samples_split': [2, 5, 10, 20],  # Minimum samples to split a node
    'estimator__min_samples_leaf': [1, 2, 4]     # Minimum samples in each leaf node
}

# Initialize GridSearchCV with Random Forest inside OneVsRestClassifier
grid_search = GridSearchCV(
    OneVsRestClassifier(RandomForestClassifier(random_state=42)),
    param_grid=param_grid,
    scoring='accuracy',       # Use accuracy for evaluation
    cv=3,                     # Perform 3-fold cross-validation
    verbose=2,                # Display progress logs
    n_jobs=-1                 # Use all available CPU cores
)

# Train the model using GridSearchCV
grid_search.fit(x_train, y_train)

# Retrieve the best parameters and evaluate the model
print("Best parameters found:", grid_search.best_params_)

# Use the best model for predictions
best_model = grid_search.best_estimator_
rf_predictions = best_model.predict(x_test)

# Print evaluation metrics
print("Optimized Random Forest Model Evaluation")
print(classification_report(y_test, rf_predictions, target_names=categories))
print(f"Accuracy: {accuracy_score(y_test, rf_predictions):.2f}")
