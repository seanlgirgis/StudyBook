# Synthetic Demo Document

## Intake Script (Demo)

## Step 1: Identify Need
Ask:
1. "What issue are you experiencing right now?"
2. "Is this HVAC, plumbing, water heater, or appliance related?"

## Step 2: Detect Urgency
Ask:
1. "Is there a safety concern such as gas smell, burning odor, or active water leak?"
2. "Is anyone in the home medically sensitive to temperature extremes?"

If yes to safety concern, escalate immediately.

## Step 3: Confirm Serviceability
Ask:
1. "What city and zip code is the service location?"
2. "Are you the homeowner, tenant, or property manager?"

## Step 4: Collect Equipment Context
Ask category-specific details:
- HVAC: system age, cooling/heating status, unusual noise
- Water heater: leak location, hot-water availability
- Appliance: appliance type, brand/model, symptom

## Step 5: Route Outcome
- If serviceable and safe: offer booking window.
- If outside area: fallback and offer waitlist callback.
- If unsupported: fallback with supported-service summary.
- If policy exception requested: escalate pricing.

## Lead Quality Scoring Inputs (Demo)
- `service_in_area` (yes/no)
- `urgency_level` (low/medium/high)
- `service_type_supported` (yes/no)
- `replacement_intent` (yes/no/unknown)
- `schedule_readiness` (ready/not_ready)

## Outcome Event Template
- `event_type`: `intake_completed`
- `classification`: hvac_repair|hvac_replace|plumbing|water_heater|appliance|unsupported
- `action`: answer|fallback|escalate|book
