import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Load batch predictions
df = pd.read_csv("models/python_test_predictions.csv")

# Actual and predicted labels
y_true = df["actual_class"]
y_pred = df["python_prediction"]

# Accuracy
accuracy = accuracy_score(y_true, y_pred)

# Correct / Incorrect
correct = (y_true == y_pred).sum()
incorrect = (y_true != y_pred).sum()

# Classification report
report = classification_report(
    y_true,
    y_pred
)

# Confusion matrix
cm = confusion_matrix(
    y_true,
    y_pred,
    labels=["Invalid", "Manual Review", "Valid"]
)

# Average confidence
average_confidence = df["top_confidence"].mean()

# Average confidence by predicted class
confidence_by_class = df.groupby(
    "python_prediction"
)["top_confidence"].mean()

print("=" * 60)
print("ASSUREX BATCH EVALUATION")
print("=" * 60)

print("\nTotal Claims:")
print(len(df))

print("\nCorrect Predictions:")
print(correct)

print("\nIncorrect Predictions:")
print(incorrect)

print("\nAccuracy:")
print(f"{accuracy:.4f}")

print("\nAverage Top Confidence:")
print(f"{average_confidence:.4f}")

print("\nAverage Confidence By Predicted Class:")
print(confidence_by_class)

print("\nClassification Report:")
print(report)

print("\nConfusion Matrix:")
print("                 Predicted")
print("                 Invalid  Manual  Valid")
print(
    f"Actual Invalid    {cm[0][0]:3}      {cm[0][1]:3}     {cm[0][2]:3}"
)
print(
    f"Actual Manual     {cm[1][0]:3}      {cm[1][1]:3}     {cm[1][2]:3}"
)
print(
    f"Actual Valid      {cm[2][0]:3}      {cm[2][1]:3}     {cm[2][2]:3}"
)

# Save incorrect predictions
incorrect_df = df[
    df["actual_class"] != df["python_prediction"]
]

incorrect_df.to_csv(
    "models/python_incorrect_predictions.csv",
    index=False
)

print("\nIncorrect predictions saved to:")
print("models/python_incorrect_predictions.csv")

print("=" * 60)