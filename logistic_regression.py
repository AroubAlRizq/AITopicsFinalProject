# -*- coding: utf-8 -*-
"""Logistic_Regression.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1BjPZMwZYl1kIttQJHEMJGkK5bs0KWOKo
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix, RocCurveDisplay

#Loading Data
data = pd.read_csv("/content/Dry_Bean_Dataset.csv")

data.info()

# Handle missing values if any (check for NaNs)
print('Number of Null values:', data.isnull().sum().sum())

from scipy.stats import zscore

# Identify and remove outliers using Z-score
numerical_columns = data.select_dtypes(include=['float64', 'int64']).columns
z_scores = zscore(data[numerical_columns])
outliers = (np.abs(z_scores) > 3).any(axis=1)
data = data[~outliers].reset_index(drop=True)
print("Final shape after outlier removal:", data.shape)

# Separate features and target
X = data.drop(columns=['Class'])
y = data['Class']

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler

# Split the data into training and testing sets (80/20 split)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data to ensure optimal KNN performance
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

from sklearn.linear_model import LogisticRegression

# Define the Logistic Regression model
log_reg = LogisticRegression(max_iter=1000, random_state=42)

# Set up the hyperparameter grid for Logistic Regression
param_grid = {
    'C': [0.01, 0.1, 1, 10, 100],  # Regularization strength
    'solver': ['liblinear', 'lbfgs'],  # Optimization algorithms
}

# Use GridSearchCV for hyperparameter tuning with cross-validation
grid_search = GridSearchCV(log_reg, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# Print the best hyperparameters
print("Best hyperparameters found:", grid_search.best_params_)

# Train the Logistic Regression model with optimal parameters
best_log_reg = grid_search.best_estimator_
best_log_reg.fit(X_train, y_train)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
# Evaluate the model
y_pred = best_log_reg.predict(X_test)

# Calculate evaluation metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')

# Print metrics
print("Evaluation Metrics for Logistic Regression:")
print("Model Accuracy:", accuracy)
print("Model Precision:", precision)
print("Model Recall:", recall)
print("Model F1-Score:", f1)

# Print a detailed classification report
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()