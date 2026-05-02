# Retrieval Questions (Synthetic Demo)

Each question maps to expected source docs and recommended assistant action.

| # | Sample Customer Question | Expected Source Document(s) | Action |
|---|---|---|---|
| 1 | My A/C stopped cooling. Can someone come today? | `hvac_repair_policy.md`, `business_hours.md`, `scheduling_policy.md` | Answer |
| 2 | My unit is 17 years old. Should I repair or replace it? | `ac_replacement_estimates.md`, `hvac_repair_policy.md` | Answer |
| 3 | Do you offer financing for a new A/C system? | `financing_policy.md`, `ac_replacement_estimates.md` | Answer |
| 4 | Do you service Plano? | `service_area.md` | Answer |
| 5 | Are you open on Sunday? | `business_hours.md`, `scheduling_policy.md` | Answer |
| 6 | Can you waive the diagnostic fee? | `coupon_policy.md` | Answer |
| 7 | Do you repair water heaters? | `water_heater_policy.md` | Answer |
| 8 | Do you repair refrigerators? | `appliance_repair_policy.md` | Answer |
| 9 | What info do you need before scheduling? | `scheduling_policy.md`, `intake_script.md` | Answer |
| 10 | I smell gas near the heater. What should I do? | `escalation_rules.md`, `water_heater_policy.md` | Escalate |
| 11 | I’m outside your service area, can you still come? | `service_area.md`, `scheduling_policy.md` | Fallback |
| 12 | Can you do a Sunday plumbing appointment? | `business_hours.md`, `scheduling_policy.md` | Fallback |
| 13 | What is included in your maintenance plan? | `maintenance_plan.md` | Answer |
| 14 | Can I combine two coupons with emergency service? | `coupon_policy.md` | Fallback |
| 15 | What warranty comes with a repair? | `warranty_policy.md` | Answer |
| 16 | What if I want a special discount not listed? | `coupon_policy.md`, `escalation_rules.md` | Escalate |
| 17 | Do you handle commercial rooftop HVAC units? | `company_profile.md`, `escalation_rules.md` | Fallback |
| 18 | My apartment manager needs multi-unit scheduling, can you do that? | `service_area.md`, `intake_script.md`, `scheduling_policy.md` | Answer |
| 19 | Can you quote exact replacement price by chat? | `ac_replacement_estimates.md` | Fallback |
| 20 | My AC is out and my parent uses medical equipment. | `hvac_repair_policy.md`, `escalation_rules.md` | Escalate |
| 21 | Do you replace tankless water heaters too? | `water_heater_policy.md` | Answer |
| 22 | Can I finance a small diagnostic-only visit? | `financing_policy.md` | Fallback |
| 23 | What happens if parts are unavailable? | `hvac_repair_policy.md`, `appliance_repair_policy.md` | Answer |
| 24 | What outcome should happen after intake is complete? | `intake_script.md`, `scheduling_policy.md` | Answer |

Action Key:
- `Answer`: respond with policy-grounded answer plus citations.
- `Fallback`: decline unsupported/out-of-policy request and offer next-best option.
- `Escalate`: route to safety/dispatch/pricing queue based on policy.
