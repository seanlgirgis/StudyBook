# Snowflake Schema - Story Map

## 1. Story (family tree)
Instead of one flat family list, you link parents to grandparents. The tree is tidy, but you need more steps to reach the top.

## 2. Core Concepts (street version)
- Snowflake schema = dimensions are normalized into sub-dimensions.
- Star schema = dimensions stay denormalized and flat.

## 3. What Changes
Product dimension might split into Product -> Category -> Department. Each hop is another join.

## 4. Why It Exists
Normalization reduces duplication and keeps dimension updates consistent.

## 5. Tradeoff
More joins make queries slightly more complex than star schema.

## 6. Final Mental Model
Snowflake is a star with extra branches on the spokes.

## 7. Run Order
1. c003_snowflake_schema_demo.py
