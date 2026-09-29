# AssureX Claim Engine – Python ML Model

## Overview

This module contains the Python Machine Learning component of the AssureX Claim Engine project.

The main task is multi-class warranty claim classification using an XGBoost model.

## Model

* Model: XGBoost
* Model Version: 1.0
* Task: Multi-class warranty claim classification
* Classes:

  * Invalid
  * Manual Review
  * Valid

## Dataset

The dataset contains 1,500 warranty claims.

The data was divided using a stratified split:

* Training: 1,050 samples
* Validation: 225 samples
* Testing: 225 samples

The three classes are balanced across the dataset.

## Features

The model uses the following features:

* product_category
* product_age_months
* warranty_period_months
* receipt_available
* serial_number_valid
* damage_type
* repair_history
* purchase_price
* claim_amount
* days_since_purchase
* remaining_warranty_months

`remaining_warranty_months` is a derived feature calculated from the warranty period and product age.

## Model Evaluation

The final XGBoost model achieved:

* Validation Accuracy: 94.22%
* Test Accuracy: 92.00%
* 5-Fold Cross-Validation Mean Accuracy: 92.00%

Test set:

* Total claims: 225
* Correct predictions: 207
* Incorrect predictions: 18

## Prediction Output

The prediction module returns:

* claim_id
* python_prediction
* python_probabilities
* python_confidence
* model_name
* model_version

The class probabilities are provided for:

* Invalid
* Manual Review
* Valid

## Project Structure

```text
Python_Model/
├── Data/
├── Model/
├── Report/
├── Src/
├── Tests/
└── README.md
```

## Integration

The Python model is designed to provide prediction results to the AssureX Claim Engine integration pipeline, where its output can be compared with the other project components and used in the final claim decision process.
