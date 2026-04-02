# Schema Validation - Story Map

## 1. Story (security checkpoint)
A warehouse scans shipments before they enter storage. If the label format is wrong, the shipment is rejected.

## 2. Core Concepts (street version)
- Schema validation = check required fields and data types.
- Expected schema = the contract for incoming data.
- Failure = missing columns or wrong types.

## 3. What Gets Checked
Required fields, types (numeric vs text), and extra unexpected fields.

## 4. Clean Pass Case
When all rows match the schema, the batch loads into curated tables.

## 5. Failure Case
If rows fail validation, the batch is blocked or quarantined for review.

## 6. Final Mental Model
Validate early. Bad schema means bad downstream data.

## 7. Run Order
1. c001_schema_validation_demo.py
