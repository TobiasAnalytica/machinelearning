import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import classification_report

# Load the dataset
file_path = 'C:\\workspace\\book1.csv'
data = pd.read_csv(file_path, encoding='latin1')

# Define features (X) and labels (y)
X = data['Heading']
y = data.drop(columns=['Id', 'Heading'])

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Convert text data into TF-IDF features
vectorizer = TfidfVectorizer(max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Wrap a Logistic Regression model in a OneVsRestClassifier for multi-label classification
model = OneVsRestClassifier(LogisticRegression(max_iter=1000, random_state=42))
model.fit(X_train_tfidf, y_train)

# Make predictions
y_pred = model.predict(X_test_tfidf)

# Evaluate the model
report = classification_report(y_test, y_pred, target_names=y.columns, zero_division=0)
print(report)
