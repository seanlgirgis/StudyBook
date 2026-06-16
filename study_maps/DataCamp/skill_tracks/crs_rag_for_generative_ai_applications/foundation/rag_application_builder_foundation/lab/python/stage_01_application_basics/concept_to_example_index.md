# Stage 1 Concept-to-Example Index

This reference maps recurring Stage 1 ideas to the smallest application example, the reusable `rag_foundation` mechanic, the validating tests, and a more complete example when one exists. Verified baseline: `322 passing tests`.

## How to Use This Index

Examples:
- Search for “retry”
- Search for “budget”
- Search for “conversation history”
- Search for “audit”

## Most Important Starting Points

- [`68_validate_application_settings.py`](68_validate_application_settings.py): validates non-secret startup settings and confirms the API key is present without storing it.
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py): shows the reusable guarded request workflow that composes retries, budget control, diagnostics, structured results, and audit append.
- [`70_guarded_console_application.py`](70_guarded_console_application.py): shows the tiny end-to-end console application built from validated settings plus the guarded workflow.

## Learning Path Through the Examples

Requests
→ Messages
→ Structured output
→ History
→ Cost
→ Retry
→ Budget
→ Diagnostics
→ Structured result
→ Persistence
→ Audit
→ Settings
→ Guarded workflow
→ Console application

## Quick Lookup

| Need | Start Here | Reusable Mechanic | Complete Example |
| --- | --- | --- | --- |
| First request | [`01_first_request.py`](01_first_request.py) | `rag_foundation.providers.openai_text.OpenAITextProvider` | [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py) |
| Structured parsing | [`35_parse_structured_model_output.py`](35_parse_structured_model_output.py) | `rag_foundation.structured.parse_json_object()` | [`40_extract_validated_fields.py`](40_extract_validated_fields.py) |
| Conversation history | [`26_followup_requires_context.py`](26_followup_requires_context.py) | `ConversationRequest`, `ChatMessage` | [`34_shared_two_turn_conversation.py`](34_shared_two_turn_conversation.py) |
| History trimming | [`44_trim_conversation_history.py`](44_trim_conversation_history.py) | `rag_foundation.history.keep_recent_messages()` | [`47_validate_and_repair_summary.py`](47_validate_and_repair_summary.py) |
| Request cost | [`43_request_cost_calculation.py`](43_request_cost_calculation.py) | `TokenRates`, `estimate_request_cost()` | [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py) |
| Retry | [`49_retry_transient_failure.py`](49_retry_transient_failure.py) | `RetryPolicy`, `run_with_retry()` | [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py) |
| Budget guard | [`54_budget_guard_before_request.py`](54_budget_guard_before_request.py) | `CostBudgetTracker` | [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py) |
| Safe diagnostics | [`51_safe_generation_diagnostics.py`](51_safe_generation_diagnostics.py) | `build_success_diagnostic()`, `build_failure_diagnostic()` | [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py) |
| Structured result | [`61_structured_operation_result_workflow.py`](61_structured_operation_result_workflow.py) | `OperationResult` | [`70_guarded_console_application.py`](70_guarded_console_application.py) |
| Atomic JSON | [`63_atomic_operation_result_file.py`](63_atomic_operation_result_file.py) | `write_json_atomic()` | — |
| Audit summary | [`65_summarize_operation_audit.py`](65_summarize_operation_audit.py) | `summarize_operation_audit()` | — |
| Audit lookup | [`66_find_audit_record_by_correlation_id.py`](66_find_audit_record_by_correlation_id.py) | `find_operation_audit_record()` | — |
| Recent audit records | [`67_list_recent_audit_records.py`](67_list_recent_audit_records.py) | `list_recent_operation_audit_records()` | — |
| Startup settings | [`68_validate_application_settings.py`](68_validate_application_settings.py) | `ApplicationSettings` | [`70_guarded_console_application.py`](70_guarded_console_application.py) |
| Guarded workflow | [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py) | `GuardedTextWorkflow` | [`70_guarded_console_application.py`](70_guarded_console_application.py) |

## Concepts by Category

### Provider and Requests

#### First provider request
**What it solves:** Shows the smallest real provider call.

**Start with:**
- [`01_first_request.py`](01_first_request.py)

**Reusable mechanics:**
- `rag_foundation.providers.openai_text.OpenAITextProvider`

**Library source:**
- `src/rag_foundation/providers/openai_text.py`

**Tests:**
- `tests/test_openai_text_provider.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** TextGenerationRequest, TextGenerationResult, Provider abstraction

#### Model selection and temperature
**What it solves:** Chooses capability and output variability deliberately.

**Start with:**
- [`06_model_override.py`](06_model_override.py)
- [`42_sampling_temperature_comparison.py`](42_sampling_temperature_comparison.py)

**Reusable mechanics:**
- `rag_foundation.models.requests.TextGenerationRequest`

**Library source:**
- `src/rag_foundation/models/requests.py`

**Tests:**
- `tests/test_temperature.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** TextGenerationRequest, Request cost calculation

#### Provider abstraction
**What it solves:** Hides provider-specific details behind a stable interface.

**Start with:**
- [`17_use_shared_text_provider.py`](17_use_shared_text_provider.py)

**Reusable mechanics:**
- `rag_foundation.providers.base.TextGenerationProvider`
- `rag_foundation.providers.openai_text.OpenAITextProvider`

**Library source:**
- `src/rag_foundation/providers/base.py`
- `src/rag_foundation/providers/openai_text.py`

**Tests:**
- `tests/test_openai_text_provider.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** First provider request, GuardedTextWorkflow

#### TextGenerationRequest
**What it solves:** Validates request shape before a provider call is attempted.

**Start with:**
- [`08_request_validation.py`](08_request_validation.py)

**Reusable mechanics:**
- `rag_foundation.models.requests.TextGenerationRequest`

**Library source:**
- `src/rag_foundation/models/requests.py`

**Tests:**
- `tests/test_text_generation_models.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** First provider request, Structured prompting, TextGenerationResult

#### TextGenerationResult
**What it solves:** Gives the application one normalized result object with text plus metadata.

**Start with:**
- [`05_result_metadata.py`](05_result_metadata.py)

**Reusable mechanics:**
- `rag_foundation.models.results.TextGenerationResult`

**Library source:**
- `src/rag_foundation/models/results.py`

**Tests:**
- `tests/test_text_generation_models.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** TextGenerationRequest, Request cost calculation, Safe generation diagnostics

### Messages and Roles

#### Message order
**What it solves:** Preserves conversational meaning by keeping messages in sequence.

**Start with:**
- [`24_ordered_message_history.py`](24_ordered_message_history.py)

**Reusable mechanics:**
- `rag_foundation.models.chat.ChatMessage`

**Library source:**
- `src/rag_foundation/models/chat.py`

**Tests:**
- `tests/test_chat_message.py`

**Complete example:**
- [`25_two_turn_conversation.py`](25_two_turn_conversation.py)

**Related:** Message roles, Multi-turn conversation, Conversation history

#### Message roles
**What it solves:** Separates system, user, and assistant responsibilities.

**Start with:**
- [`22_message_roles.py`](22_message_roles.py)

**Reusable mechanics:**
- `rag_foundation.models.chat.ChatMessage`

**Library source:**
- `src/rag_foundation/models/chat.py`

**Tests:**
- `tests/test_chat_message.py`

**Complete example:**
- [`25_two_turn_conversation.py`](25_two_turn_conversation.py)

**Related:** Message order, Dual prompts, Multi-turn conversation

#### Multi-turn conversation
**What it solves:** Reuses earlier context so follow-up questions make sense.

**Start with:**
- [`25_two_turn_conversation.py`](25_two_turn_conversation.py)

**Reusable mechanics:**
- `ConversationRequest`
- `ChatMessage`

**Library source:**
- `src/rag_foundation/models/requests.py`
- `src/rag_foundation/models/chat.py`

**Tests:**
- `tests/test_conversation_request.py`

**Complete example:**
- [`34_shared_two_turn_conversation.py`](34_shared_two_turn_conversation.py)

**Related:** Message order, Conversation history, History trimming

### Prompting

#### Dual prompts
**What it solves:** Keeps application behavior separate from the user’s current question.

**Start with:**
- [`48_dual_prompt_chatbot.py`](48_dual_prompt_chatbot.py)

**Reusable mechanics:**
- `rag_foundation.models.requests.TextGenerationRequest`

**Library source:**
- `src/rag_foundation/models/requests.py`

**Tests:**
- `tests/test_text_generation_models.py`

**Complete example:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Related:** Message roles, Structured prompting, End-to-end console application

#### Few-shot prompting
**What it solves:** Shows how example-driven prompts steer output differently from zero-shot prompts.

**Start with:**
- [`33_zero_shot_vs_few_shot.py`](33_zero_shot_vs_few_shot.py)

**Reusable mechanics:**
- `rag_foundation.models.requests.TextGenerationRequest`

**Library source:**
- `src/rag_foundation/models/requests.py`

**Tests:**
- `tests/test_text_generation_models.py`

**Related:** Structured prompting, TextGenerationRequest

#### Structured prompting
**What it solves:** Asks for machine-usable fields instead of free-form prose.

**Start with:**
- [`20_structured_ticket_triage.py`](20_structured_ticket_triage.py)

**Reusable mechanics:**
- `rag_foundation.models.requests.TextGenerationRequest`
- `rag_foundation.structured.parse_json_object()`

**Library source:**
- `src/rag_foundation/models/requests.py`
- `src/rag_foundation/structured.py`

**Tests:**
- `tests/test_structured.py`

**Complete example:**
- [`40_extract_validated_fields.py`](40_extract_validated_fields.py)

**Related:** Safe parsing, Validated ticket model, Dual prompts

### Structured Output

#### Safe parsing
**What it solves:** Rejects invalid or non-object structured output before the app uses it.

**Start with:**
- [`35_parse_structured_model_output.py`](35_parse_structured_model_output.py)

**Reusable mechanics:**
- `rag_foundation.structured.StructuredOutputError`
- `rag_foundation.structured.parse_json_object()`

**Library source:**
- `src/rag_foundation/structured.py`

**Tests:**
- `tests/test_structured.py`

**Complete example:**
- [`40_extract_validated_fields.py`](40_extract_validated_fields.py)

**Related:** Structured prompting, Validated ticket model, JSON-safe serialization and Decimal precision

#### Structured model response
**What it solves:** Requests a predictable field-based response shape.

**Start with:**
- [`20_structured_ticket_triage.py`](20_structured_ticket_triage.py)

**Reusable mechanics:**
- `rag_foundation.structured.parse_json_object()`

**Library source:**
- `src/rag_foundation/structured.py`

**Tests:**
- `tests/test_structured.py`

**Complete example:**
- [`40_extract_validated_fields.py`](40_extract_validated_fields.py)

**Related:** Structured prompting, Safe parsing, Validated ticket model

#### Validated ticket model
**What it solves:** Converts structured output into validated application-owned data.

**Start with:**
- [`21_validated_ticket_model.py`](21_validated_ticket_model.py)

**Reusable mechanics:**
- `rag_foundation.structured.parse_json_object()`

**Library source:**
- `src/rag_foundation/structured.py`

**Tests:**
- `tests/test_structured.py`

**Complete example:**
- [`40_extract_validated_fields.py`](40_extract_validated_fields.py)

**Related:** Structured model response, Safe parsing, Validation

### Conversation History

#### Conversation history
**What it solves:** Keeps prior turns available for later questions.

**Start with:**
- [`26_followup_requires_context.py`](26_followup_requires_context.py)

**Reusable mechanics:**
- `ConversationRequest`
- `ChatMessage`

**Library source:**
- `src/rag_foundation/models/requests.py`
- `src/rag_foundation/models/chat.py`

**Tests:**
- `tests/test_conversation_request.py`

**Complete example:**
- [`34_shared_two_turn_conversation.py`](34_shared_two_turn_conversation.py)

**Related:** Message order, Multi-turn conversation, History trimming

#### History trimming
**What it solves:** Shrinks resent history while preserving the most important messages.

**Start with:**
- [`44_trim_conversation_history.py`](44_trim_conversation_history.py)

**Reusable mechanics:**
- `rag_foundation.history.keep_recent_messages()`

**Library source:**
- `src/rag_foundation/history.py`

**Tests:**
- `tests/test_history.py`

**Complete example:**
- [`47_validate_and_repair_summary.py`](47_validate_and_repair_summary.py)

**Related:** Conversation history, Older-history summarization, Summary validation and repair

#### Older-history summarization
**What it solves:** Replaces earlier turns with one summary to save context space.

**Start with:**
- [`45_summarize_older_history.py`](45_summarize_older_history.py)

**Reusable mechanics:**
- `rag_foundation.history.build_summarized_history()`

**Library source:**
- `src/rag_foundation/history.py`

**Tests:**
- `tests/test_history_summary.py`

**Complete example:**
- [`47_validate_and_repair_summary.py`](47_validate_and_repair_summary.py)

**Related:** History trimming, Summary information loss, Summary validation and repair

#### Summary information loss
**What it solves:** Shows which facts can disappear when history is summarized too aggressively.

**Start with:**
- [`46_summary_information_loss.py`](46_summary_information_loss.py)

**Reusable mechanics:**
- `rag_foundation.summary_validation.validate_summary_facts()`

**Library source:**
- `src/rag_foundation/summary_validation.py`

**Tests:**
- `tests/test_summary_validation.py`

**Complete example:**
- [`47_validate_and_repair_summary.py`](47_validate_and_repair_summary.py)

**Related:** Older-history summarization, Summary validation and repair

#### Summary validation and repair
**What it solves:** Checks required facts after summarization and repairs the summary when facts are missing.

**Start with:**
- [`47_validate_and_repair_summary.py`](47_validate_and_repair_summary.py)

**Reusable mechanics:**
- `rag_foundation.summary_validation.SummaryValidationResult`
- `rag_foundation.summary_validation.validate_summary_facts()`

**Library source:**
- `src/rag_foundation/summary_validation.py`

**Tests:**
- `tests/test_summary_validation.py`

**Related:** Summary information loss, Older-history summarization, Safe parsing

### Tokens and Cost

#### Local cumulative budget
**What it solves:** Tracks local spending across multiple requests.

**Start with:**
- [`53_local_budget_tracking.py`](53_local_budget_tracking.py)

**Reusable mechanics:**
- `rag_foundation.budget.CostBudgetTracker`

**Library source:**
- `src/rag_foundation/budget/tracker.py`

**Tests:**
- `tests/test_budget_tracker.py`

**Complete example:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Related:** Request cost calculation, Budget tracking and warning threshold, Cumulative workflow budget

#### Request cost calculation
**What it solves:** Turns token usage into estimated monetary cost.

**Start with:**
- [`43_request_cost_calculation.py`](43_request_cost_calculation.py)

**Reusable mechanics:**
- `rag_foundation.costs.TokenRates`
- `rag_foundation.costs.estimate_request_cost()`

**Library source:**
- `src/rag_foundation/costs.py`

**Tests:**
- `tests/test_costs.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** TokenRates, Local cumulative budget, Projected-cost reservation

#### TokenRates
**What it solves:** Keeps pricing rates in explicit application data.

**Start with:**
- [`43_request_cost_calculation.py`](43_request_cost_calculation.py)

**Reusable mechanics:**
- `rag_foundation.costs.TokenRates`

**Library source:**
- `src/rag_foundation/costs.py`

**Tests:**
- `tests/test_costs.py`

**Complete example:**
- [`68_validate_application_settings.py`](68_validate_application_settings.py)

**Related:** Request cost calculation, ApplicationSettings

### Reliability and Retry

#### Bounded retries
**What it solves:** Retries temporary failures without retrying forever.

**Start with:**
- [`49_retry_transient_failure.py`](49_retry_transient_failure.py)

**Reusable mechanics:**
- `rag_foundation.retry.RetryPolicy`
- `rag_foundation.retry.run_with_retry()`

**Library source:**
- `src/rag_foundation/retry.py`

**Tests:**
- `tests/test_retry.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Retry exhaustion, Safe fallback, Correlation ID and attempt count

#### Retry exhaustion
**What it solves:** Stops after the last allowed retry instead of looping forever.

**Start with:**
- [`50_retry_exhaustion_safe_fallback.py`](50_retry_exhaustion_safe_fallback.py)

**Reusable mechanics:**
- `rag_foundation.retry.RetryPolicy`
- `rag_foundation.retry.run_with_retry()`

**Library source:**
- `src/rag_foundation/retry.py`

**Tests:**
- `tests/test_retry.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Bounded retries, Safe fallback, Safe generation diagnostics

#### Safe fallback
**What it solves:** Returns a controlled user-safe response after failure.

**Start with:**
- [`50_retry_exhaustion_safe_fallback.py`](50_retry_exhaustion_safe_fallback.py)

**Reusable mechanics:**
- `rag_foundation.diagnostics.build_failure_diagnostic()`
- `rag_foundation.operation_result.OperationResult`

**Library source:**
- `src/rag_foundation/diagnostics.py`
- `src/rag_foundation/operation_result.py`

**Tests:**
- `tests/test_guarded_text_workflow.py`

**Complete example:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Related:** Retry exhaustion, Safe generation diagnostics, OperationResult

### Budget Control

#### Budget tracking and warning threshold
**What it solves:** Tracks local spend and raises a warning before exhaustion.

**Start with:**
- [`53_local_budget_tracking.py`](53_local_budget_tracking.py)

**Reusable mechanics:**
- `rag_foundation.budget.CostBudgetTracker`

**Library source:**
- `src/rag_foundation/budget/tracker.py`

**Tests:**
- `tests/test_budget_tracker.py`

**Complete example:**
- [`68_validate_application_settings.py`](68_validate_application_settings.py)

**Related:** Local cumulative budget, Pre-request budget guard, ApplicationSettings

#### Context-managed reservation
**What it solves:** Automatically cleans up reservations around provider work.

**Start with:**
- [`58_automatic_reservation_cleanup.py`](58_automatic_reservation_cleanup.py)

**Reusable mechanics:**
- `rag_foundation.budget.BudgetReservationScope`

**Library source:**
- `src/rag_foundation/budget/reservation_scope.py`

**Tests:**
- `tests/test_budget_reservation_scope.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Projected-cost reservation, Reservation cleanup, GuardedTextWorkflow

#### Pre-request budget guard
**What it solves:** Blocks overspending before the provider call happens.

**Start with:**
- [`54_budget_guard_before_request.py`](54_budget_guard_before_request.py)

**Reusable mechanics:**
- `rag_foundation.budget.CostBudgetTracker`
- `rag_foundation.budget.BudgetDecision`

**Library source:**
- `src/rag_foundation/budget/tracker.py`

**Tests:**
- `tests/test_budget_guard.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Projected-cost reservation, Budget tracking and warning threshold, OperationResult

#### Projected-cost reservation
**What it solves:** Holds expected cost for an in-flight request before actual cost is known.

**Start with:**
- [`55_concurrent_budget_reservations.py`](55_concurrent_budget_reservations.py)

**Reusable mechanics:**
- `rag_foundation.budget.BudgetReservationScope`

**Library source:**
- `src/rag_foundation/budget/reservation_scope.py`

**Tests:**
- `tests/test_budget_reservations.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Context-managed reservation, Concurrent reservation, Request cost calculation

#### Reservation cleanup
**What it solves:** Releases projected budget after failure.

**Start with:**
- [`57_release_reservation_after_failure.py`](57_release_reservation_after_failure.py)

**Reusable mechanics:**
- `rag_foundation.budget.BudgetReservationScope`

**Library source:**
- `src/rag_foundation/budget/reservation_scope.py`

**Tests:**
- `tests/test_budget_reservation_scope.py`

**Complete example:**
- [`58_automatic_reservation_cleanup.py`](58_automatic_reservation_cleanup.py)

**Related:** Projected-cost reservation, Context-managed reservation, Retry exhaustion

### Concurrency and Reservations

#### Concurrent reservation
**What it solves:** Protects a shared budget when multiple requests compete at the same time.

**Start with:**
- [`56_real_concurrent_reservation_race.py`](56_real_concurrent_reservation_race.py)

**Reusable mechanics:**
- `rag_foundation.budget.CostBudgetTracker`
- `rag_foundation.budget.BudgetReservationScope`

**Library source:**
- `src/rag_foundation/budget/tracker.py`
- `src/rag_foundation/budget/reservation_scope.py`

**Tests:**
- `tests/test_budget_reservations.py`

**Complete example:**
- [`55_concurrent_budget_reservations.py`](55_concurrent_budget_reservations.py)

**Related:** Projected-cost reservation, Reservation cleanup, Context-managed reservation

### Diagnostics and Safety

#### Safe generation diagnostics
**What it solves:** Captures safe success and failure metadata without leaking sensitive content.

**Start with:**
- [`51_safe_generation_diagnostics.py`](51_safe_generation_diagnostics.py)

**Reusable mechanics:**
- `rag_foundation.diagnostics.GenerationDiagnostic`
- `rag_foundation.diagnostics.build_success_diagnostic()`
- `rag_foundation.diagnostics.build_failure_diagnostic()`

**Library source:**
- `src/rag_foundation/diagnostics.py`

**Tests:**
- `tests/test_diagnostics.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Sensitive-data exclusion, Correlation ID and attempt count, OperationResult

#### Sensitive-data exclusion
**What it solves:** Keeps prompts, answers, exception messages, secrets, and raw responses out of safe metadata.

**Start with:**
- [`51_safe_generation_diagnostics.py`](51_safe_generation_diagnostics.py)

**Reusable mechanics:**
- `rag_foundation.diagnostics.build_success_diagnostic()`
- `rag_foundation.diagnostics.build_failure_diagnostic()`
- `rag_foundation.operation_audit_builder.build_operation_audit_record()`

**Library source:**
- `src/rag_foundation/diagnostics.py`
- `src/rag_foundation/operation_audit_builder.py`

**Tests:**
- `tests/test_diagnostics.py`
- `tests/test_operation_audit_builder.py`

**Complete example:**
- [`64_operation_audit_jsonl.py`](64_operation_audit_jsonl.py)

**Related:** Safe generation diagnostics, Safe audit record, ApplicationSettings

### Correlation and Tracing

#### Correlation ID and attempt count
**What it solves:** Gives one logical request a stable reference across retries and final outcomes.

**Start with:**
- [`52_correlation_id_across_operation.py`](52_correlation_id_across_operation.py)

**Reusable mechanics:**
- `rag_foundation.correlation.create_correlation_id()`
- `rag_foundation.correlation.validate_correlation_id()`

**Library source:**
- `src/rag_foundation/correlation.py`

**Tests:**
- `tests/test_correlation.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** OperationDiagnosticContext, Safe generation diagnostics, OperationResult

#### OperationDiagnosticContext
**What it solves:** Bundles correlation ID plus attempt count for safe diagnostics.

**Start with:**
- [`61_structured_operation_result_workflow.py`](61_structured_operation_result_workflow.py)

**Reusable mechanics:**
- `rag_foundation.operation_context.OperationDiagnosticContext`

**Library source:**
- `src/rag_foundation/operation_context.py`

**Tests:**
- `tests/test_operation_context.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Correlation ID and attempt count, Safe generation diagnostics, OperationResult

### Serialization

#### Decimal precision
**What it solves:** Keeps money values precise in JSON-safe output by serializing Decimal as strings.

**Start with:**
- [`62_json_safe_operation_result.py`](62_json_safe_operation_result.py)

**Reusable mechanics:**
- `rag_foundation.serialization.to_json_safe()`

**Library source:**
- `src/rag_foundation/serialization.py`

**Tests:**
- `tests/test_serialization.py`

**Complete example:**
- [`65_summarize_operation_audit.py`](65_summarize_operation_audit.py)

**Related:** JSON-safe serialization, Atomic JSON writing, Audit summary

#### JSON-safe serialization
**What it solves:** Produces a `json.dumps()`-ready representation of structured results.

**Start with:**
- [`62_json_safe_operation_result.py`](62_json_safe_operation_result.py)

**Reusable mechanics:**
- `rag_foundation.serialization.to_json_safe()`
- `OperationResult.to_json_dict()`

**Library source:**
- `src/rag_foundation/serialization.py`
- `src/rag_foundation/operation_result.py`

**Tests:**
- `tests/test_serialization.py`
- `tests/test_operation_result.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Python-native dictionary, Decimal precision, OperationResult

#### OperationResult
**What it solves:** Returns one validated structured outcome for success, fallback, and blocked paths.

**Start with:**
- [`61_structured_operation_result_workflow.py`](61_structured_operation_result_workflow.py)

**Reusable mechanics:**
- `rag_foundation.operation_result.OperationResult`
- `rag_foundation.operation_result.OperationStatus`

**Library source:**
- `src/rag_foundation/operation_result.py`

**Tests:**
- `tests/test_operation_result.py`

**Complete example:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Related:** Correlation ID and attempt count, JSON-safe serialization, GuardedTextWorkflow

#### Python-native dictionary
**What it solves:** Shows the pre-JSON representation before conversion to JSON-safe output.

**Start with:**
- [`62_json_safe_operation_result.py`](62_json_safe_operation_result.py)

**Reusable mechanics:**
- `OperationResult.to_dict()`
- `OperationResult.to_json_dict()`

**Library source:**
- `src/rag_foundation/operation_result.py`

**Tests:**
- `tests/test_operation_result.py`

**Complete example:**
- [`63_atomic_operation_result_file.py`](63_atomic_operation_result_file.py)

**Related:** JSON-safe serialization, Decimal precision, Atomic JSON writing

### File Persistence

#### Atomic JSON writing
**What it solves:** Replaces a destination file atomically after a full temporary write.

**Start with:**
- [`63_atomic_operation_result_file.py`](63_atomic_operation_result_file.py)

**Reusable mechanics:**
- `rag_foundation.json_files.write_json_atomic()`

**Library source:**
- `src/rag_foundation/json_files.py`

**Tests:**
- `tests/test_json_files.py`

**Related:** JSON-safe serialization, Decimal precision, JSON Lines append

#### JSON Lines append
**What it solves:** Appends one compact JSON object per line with flush and sync.

**Start with:**
- [`64_operation_audit_jsonl.py`](64_operation_audit_jsonl.py)

**Reusable mechanics:**
- `rag_foundation.json_lines.append_json_line()`

**Library source:**
- `src/rag_foundation/json_lines.py`

**Tests:**
- `tests/test_json_lines.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Atomic JSON writing, Safe audit record, Recent audit records

### Audit Logging

#### Safe audit record
**What it solves:** Logs compact operational metadata while excluding prompts, answers, secrets, and raw responses.

**Start with:**
- [`64_operation_audit_jsonl.py`](64_operation_audit_jsonl.py)

**Reusable mechanics:**
- `rag_foundation.operation_audit_record.OperationAuditRecord`
- `rag_foundation.operation_audit_builder.build_operation_audit_record()`

**Library source:**
- `src/rag_foundation/operation_audit_record.py`
- `src/rag_foundation/operation_audit_builder.py`

**Tests:**
- `tests/test_operation_audit_builder.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Sensitive-data exclusion, JSON Lines append, Audit summary

### Audit Inspection

#### Audit lookup by correlation ID
**What it solves:** Retrieves one exact audit record for one logical request.

**Start with:**
- [`66_find_audit_record_by_correlation_id.py`](66_find_audit_record_by_correlation_id.py)

**Reusable mechanics:**
- `rag_foundation.operation_audit_lookup.find_operation_audit_record()`

**Library source:**
- `src/rag_foundation/operation_audit_lookup.py`

**Tests:**
- `tests/test_operation_audit_lookup.py`

**Related:** Correlation ID and attempt count, Audit summary, Recent audit records

#### Audit summary
**What it solves:** Calculates totals and latest reference data from the audit log.

**Start with:**
- [`65_summarize_operation_audit.py`](65_summarize_operation_audit.py)

**Reusable mechanics:**
- `rag_foundation.operation_audit_summary.OperationAuditSummary`
- `rag_foundation.operation_audit_reader.summarize_operation_audit()`

**Library source:**
- `src/rag_foundation/operation_audit_summary.py`
- `src/rag_foundation/operation_audit_reader.py`

**Tests:**
- `tests/test_operation_audit_reader.py`

**Related:** Safe audit record, Audit lookup by correlation ID, Recent audit records

#### Recent audit records
**What it solves:** Lists the latest audit entries in newest-first order.

**Start with:**
- [`67_list_recent_audit_records.py`](67_list_recent_audit_records.py)

**Reusable mechanics:**
- `rag_foundation.operation_audit_recent.list_recent_operation_audit_records()`

**Library source:**
- `src/rag_foundation/operation_audit_recent.py`

**Tests:**
- `tests/test_operation_audit_recent.py`

**Related:** Audit summary, Audit lookup by correlation ID, JSON Lines append

### Configuration

#### API-key presence without storing the key
**What it solves:** Confirms required secret configuration exists without storing or printing the secret itself.

**Start with:**
- [`68_validate_application_settings.py`](68_validate_application_settings.py)

**Reusable mechanics:**
- `ApplicationSettings.from_environment()`

**Library source:**
- `src/rag_foundation/application_settings.py`

**Tests:**
- `tests/test_application_settings.py`

**Complete example:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Related:** ApplicationSettings, Environment startup validation, Sensitive-data exclusion

#### ApplicationSettings
**What it solves:** Stores validated non-secret startup configuration.

**Start with:**
- [`68_validate_application_settings.py`](68_validate_application_settings.py)

**Reusable mechanics:**
- `rag_foundation.application_settings.ApplicationSettings`

**Library source:**
- `src/rag_foundation/application_settings.py`

**Tests:**
- `tests/test_application_settings.py`

**Complete example:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Related:** Environment startup validation, API-key presence without storing the key, GuardedTextWorkflow

#### Environment startup validation
**What it solves:** Fails early when required startup environment configuration is missing or blank.

**Start with:**
- [`68_validate_application_settings.py`](68_validate_application_settings.py)

**Reusable mechanics:**
- `ApplicationSettings.from_environment()`

**Library source:**
- `src/rag_foundation/application_settings.py`

**Tests:**
- `tests/test_application_settings.py`

**Complete example:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Related:** ApplicationSettings, API-key presence without storing the key, GuardedTextWorkflow

### Reusable Workflow

#### Cumulative workflow budget
**What it solves:** Reuses one local budget tracker across multiple workflow calls.

**Start with:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Reusable mechanics:**
- `GuardedTextWorkflow.budget_tracker`

**Library source:**
- `src/rag_foundation/guarded_text_workflow.py`

**Tests:**
- `tests/test_guarded_text_workflow.py`

**Complete example:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Related:** GuardedTextWorkflow, Local cumulative budget, ApplicationSettings

#### GuardedTextWorkflow
**What it solves:** Composes retries, budget control, diagnostics, structured results, and audit append into one reusable workflow object.

**Start with:**
- [`69_reusable_guarded_workflow.py`](69_reusable_guarded_workflow.py)

**Reusable mechanics:**
- `rag_foundation.guarded_text_workflow.GuardedTextWorkflow`

**Library source:**
- `src/rag_foundation/guarded_text_workflow.py`

**Tests:**
- `tests/test_guarded_text_workflow.py`

**Complete example:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Related:** ApplicationSettings, Cumulative workflow budget, OperationResult

### End-to-End Application

#### End-to-end console application
**What it solves:** Shows the full Stage 1 pattern in one tiny interactive application.

**Start with:**
- [`70_guarded_console_application.py`](70_guarded_console_application.py)

**Reusable mechanics:**
- `ApplicationSettings`
- `GuardedTextWorkflow`

**Library source:**
- `src/rag_foundation/application_settings.py`
- `src/rag_foundation/guarded_text_workflow.py`

**Tests:**
- `tests/test_application_settings.py`
- `tests/test_guarded_text_workflow.py`

**Related:** ApplicationSettings, GuardedTextWorkflow, Safe audit record
