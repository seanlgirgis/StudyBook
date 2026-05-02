# Synthetic Demo Document

## Scheduling Policy

## Required Intake Details Before Booking
- Customer first name (initials allowed in demo)
- Service city and zip code
- Service category (HVAC/plumbing/water heater/appliance)
- Symptom summary
- Preferred time window
- Occupancy status (owner, tenant, manager)

## Optional But Helpful
- System age
- Equipment brand/model
- Photos or short symptom video note

## Booking Outcomes
- `booked_standard`
- `booked_urgent`
- `needs_dispatch_review`
- `outside_service_area`
- `unsupported_request`

## Outside-Area and Unsupported Rules
- Outside area: do not book, offer waitlist callback.
- Unsupported request: fallback politely and offer referral callback.

## Sunday Scheduling Rule
- Standard appointments are not booked on Sunday.
- Emergency HVAC cases can be routed to limited dispatch review.
