# Implementation Plan - ML Engine Refactor

## Goal
Update the `ml_engine` service to use realistic features derived from the dataset (Repayment Rate, DPD) instead of the placeholder "Income" feature, as per the refined ML strategy.

## Proposed Changes

### `ml_engine/main.py`

#### [MODIFY] [main.py](file:///c:/Users/Farras Azhary/Antigravity/Amartha x GDG/ml_engine/main.py)
-   Change input payload validation to expect:
    -   `total_paid` (float)
    -   `total_bill` (float)
    -   `current_dpd` (int)
-   Implement `calculate_tier` logic:
    -   Calculate `repayment_rate = total_paid / total_bill`
    -   **Gold**: DPD == 0 AND Rate >= 0.98
    -   **Silver**: DPD <= 7 AND Rate >= 0.90
    -   **Bronze**: Others
-   Update response format to include the calculated `repayment_rate`.

## Verification Plan

### Automated Tests
-   Create a simple test script `test_ml_engine.py` (or use `curl`) to send sample payloads to the running service and verify the Tier output.
    -   Case 1: Gold User (DPD=0, Rate=1.0) -> Expect "Gold"
    -   Case 2: Silver User (DPD=5, Rate=0.95) -> Expect "Silver"
    -   Case 3: Bronze User (DPD=10, Rate=0.8) -> Expect "Bronze"

### Manual Verification
-   Run `docker-compose up ml-engine`
-   Use `curl` or Postman to hit `http://localhost:5000/predict_tier`.
