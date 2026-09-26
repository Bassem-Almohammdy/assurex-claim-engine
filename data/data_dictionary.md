# AssureX Claim Engine — Data Dictionary

The dataset is synthetic and contains 1,500 warranty claims.

| Field | Type | Description |
|---|---|---|
| `claim_id` | int | Unique claim identifier |
| `product_category` | string | Product category |
| `product_age_months` | int | Product age in months |
| `warranty_period_months` | int | Warranty period in months |
| `receipt_available` | 0/1 | Proof of purchase availability |
| `serial_number_valid` | 0/1 | Serial number validity |
| `damage_type` | string | Damage/failure type |
| `repair_history` | int | Number of previous repairs |
| `purchase_price` | float | Purchase price |
| `claim_amount` | float | Requested claim amount |
| `days_since_purchase` | int | Days since purchase |
| `claim_status` | string | Target class |

Official classes:

```text
Valid
Invalid
Manual Review
```

Split:

```text
70% Training = 1050
15% Validation = 225
15% Testing = 225
```

The same `claim_id` must never occur in more than one split.
