# AssureX Claim Engine
# Python Machine Learning Model Results

## 1. Dataset

Total records: 1500

Classes:
- Invalid: 500
- Manual Review: 500
- Valid: 500

Dataset split:
- Training: 1050
- Validation: 225
- Testing: 225

Split method:
Stratified split with random_state = 42.

---

## 2. Algorithms Tested

Three classification algorithms were evaluated:

1. Logistic Regression
2. Random Forest
3. XGBoost

---

## 3. Results

| Model | Validation Accuracy | Test Accuracy |
|---|---:|---:|
| Logistic Regression | 85.33% | 87.11% |
| Random Forest | 92.44% | 92.44% |
| XGBoost | 94.22% | 92.00% |

The final Python model is XGBoost.

---

## 4. XGBoost Configuration

- n_estimators: 200
- max_depth: 6
- learning_rate: 0.1
- subsample: 0.9
- colsample_bytree: 0.9
- random_state: 42

---

## 5. Cross Validation

Method:
Stratified 5-Fold Cross Validation

Mean Accuracy:
92.00%

Standard Deviation:
0.97 percentage points

---

## 6. Test Results

Total test claims: 225

Correct predictions: 207

Incorrect predictions: 18

Test accuracy: 92.00%

Average top-class confidence: 95.69%

---

## 7. XGBoost Classification Report

### Invalid

Precision: 0.86
Recall: 0.96
F1-score: 0.91

### Manual Review

Precision: 0.95
Recall: 0.80
F1-score: 0.87

### Valid

Precision: 0.96
Recall: 1.00
F1-score: 0.98

---

## 8. Confusion Matrix

| Actual / Predicted | Invalid | Manual Review | Valid |
|---|---:|---:|---:|
| Invalid | 72 | 3 | 0 |
| Manual Review | 12 | 60 | 3 |
| Valid | 0 | 0 | 75 |

The main classification difficulty is distinguishing
Manual Review from Invalid.

---

## 9. Feature Importance

Top features:

1. Screen Damage
2. Remaining Warranty Months
3. Receipt Availability
4. Serial Number Validity
5. Electrical Failure
6. Battery Failure
7. Manufacturing Defect
8. Software Failure
9. Repair History
10. Unknown Damage

---

## 10. Saved Model Files

- xgboost_pipeline.pkl
- label_encoder.pkl
- python_test_predictions.csv
- python_incorrect_predictions.csv

---

## 11. Prediction Contract

The Python model returns:

- claim_id
- python_prediction
- python_probabilities
- python_confidence
- model_name
- model_version

Classes:

- Invalid
- Manual Review
- Valid