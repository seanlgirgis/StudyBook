# Synthetic Demo Document

## Service Area Policy

## Core Coverage Zone
The standard coverage zone includes the following North Texas cities:
- Fort Worth
- Arlington
- Mansfield
- Burleson
- Keller
- Plano
- Frisco
- McKinney

## Limited Coverage Zone
Requests in nearby communities outside the core list may be accepted only when:
- the job is HVAC emergency service, and
- dispatch load is below 80%.

## Outside-Service-Area Rule
- If outside all coverage zones, the assistant must fallback with: "We are currently out of your area."
- Offer waitlist callback only; do not promise dispatch.
- Log outcome as `outside_service_area`.

## Edge Cases
- Borderline zip codes require dispatcher confirmation.
- Multi-property managers with 3+ addresses can request manual service-area review.
