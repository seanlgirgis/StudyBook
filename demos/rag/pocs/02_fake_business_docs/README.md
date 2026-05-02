# 02_fake_business_docs

## Purpose
Create synthetic business knowledge documents for a fake HVAC-first home-services company so later retrieval and assistant behavior can be tested with realistic policy data.

## Synthetic Data Warning
All content in this folder is synthetic demo content. It is not a real company profile, does not contain private customer data, and should not be used as legal or operational advice.

## File List
- `data/home_services_demo/company_profile.md`
- `data/home_services_demo/service_area.md`
- `data/home_services_demo/business_hours.md`
- `data/home_services_demo/hvac_repair_policy.md`
- `data/home_services_demo/ac_replacement_estimates.md`
- `data/home_services_demo/plumbing_services.md`
- `data/home_services_demo/water_heater_policy.md`
- `data/home_services_demo/appliance_repair_policy.md`
- `data/home_services_demo/maintenance_plan.md`
- `data/home_services_demo/coupon_policy.md`
- `data/home_services_demo/scheduling_policy.md`
- `data/home_services_demo/financing_policy.md`
- `data/home_services_demo/warranty_policy.md`
- `data/home_services_demo/escalation_rules.md`
- `data/home_services_demo/intake_script.md`
- `data/home_services_demo/faq.md`
- `notes/retrieval_questions.md`
- `notes/what_good_answers_should_include.md`
- `notes/document_design_notes.md`

## How These Docs Will Be Used Later
- Retrieval corpus for answer-with-citations testing.
- Policy grounding for intake classification and urgency detection.
- Rule source for fallback and escalation behavior.
- Reference set for lead quality scoring and outcome logging design.

## What This Milestone Does Not Implement
- No backend services
- No RAG pipeline
- No FastAPI endpoints
- No model/API calls
- No deployment workflow

## Next Milestone
Use these documents in a basic retrieval POC that returns cited snippets and safe fallback behavior.
