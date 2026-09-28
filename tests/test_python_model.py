import sys
import os

sys.path.append(
    os.path.abspath(".")
)

from src.ml.predict import predict_claim


def create_test_claim():

    return {
        "product_category": "Laptop",
        "product_age_months": 6,
        "warranty_period_months": 24,
        "receipt_available": 1,
        "serial_number_valid": 1,
        "damage_type": "Manufacturing Defect",
        "repair_history": 0,
        "purchase_price": 1000,
        "claim_amount": 500,
        "days_since_purchase": 180
    }


def test_prediction_exists():

    claim = create_test_claim()

    result = predict_claim(
        claim,
        "TEST-001"
    )

    assert result is not None


def test_prediction_class():

    claim = create_test_claim()

    result = predict_claim(
        claim,
        "TEST-002"
    )

    valid_classes = [
        "Invalid",
        "Manual Review",
        "Valid"
    ]

    assert result["python_prediction"] in valid_classes


def test_probabilities_exist():

    claim = create_test_claim()

    result = predict_claim(
        claim,
        "TEST-003"
    )

    probabilities = result[
        "python_probabilities"
    ]

    assert "Invalid" in probabilities
    assert "Manual Review" in probabilities
    assert "Valid" in probabilities


def test_probabilities_range():

    claim = create_test_claim()

    result = predict_claim(
        claim,
        "TEST-004"
    )

    probabilities = result[
        "python_probabilities"
    ]

    for probability in probabilities.values():

        assert 0 <= probability <= 1


def test_probability_sum():

    claim = create_test_claim()

    result = predict_claim(
        claim,
        "TEST-005"
    )

    probabilities = result[
        "python_probabilities"
    ]

    total = sum(
        probabilities.values()
    )

    assert abs(total - 1.0) < 0.0001


def test_confidence():

    claim = create_test_claim()

    result = predict_claim(
        claim,
        "TEST-006"
    )

    confidence = result[
        "python_confidence"
    ]

    assert 0 <= confidence <= 1


def test_claim_id():

    claim = create_test_claim()

    result = predict_claim(
        claim,
        "TEST-007"
    )

    assert result["claim_id"] == "TEST-007"


def test_model_version():

    claim = create_test_claim()

    result = predict_claim(
        claim,
        "TEST-008"
    )

    assert result["model_name"] == "XGBoost"
    assert result["model_version"] == "1.0"