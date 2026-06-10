# Chapter 4 Lab — Prompt Engineering for Chatbot Development

This folder preserves Chapter 4 as a replayable sequence of chatbot prompt-engineering exercises.

## Run order

1. `01_dual_prompt_chatbot.py`
   - Separates the persistent system prompt from the current user request.
   - Demonstrates the basic chatbot message pattern.

2. `02_stateful_chatbot_context.py`
   - Adds compact conversation state to the current request.
   - Shows how prior facts make an answer more relevant.

3. `03_answer_and_updated_state.py`
   - Returns both a user-facing answer and an updated compact state.
   - Demonstrates rolling conversation memory.

4. `04_structured_chat_state.py`
   - Stores state in separate fields:
     - confirmed facts
     - recommended actions
     - completed actions
     - open questions
   - Prevents recommendations from being mixed with confirmed history.

5. `05_validate_chat_state.py`
   - Parses model-generated JSON.
   - Validates top-level keys, state keys, list types, and answer type.
   - Demonstrates the application boundary before state is stored.

6. `06_domain_boundaries.py`
   - Defines the chatbot's supported domain.
   - Uses an exact fallback response for out-of-domain questions.

7. `07_role_playing_comparison.py`
   - Sends the same question to several professional roles.
   - Shows how role changes focus, vocabulary, and priorities.

8. `08_system_prompt_context.py`
   - Places a small trusted company knowledge base in the system prompt.
   - Restricts the chatbot to supplied company facts.

9. `09_sample_conversation_context.py`
   - Uses prior user/assistant examples to teach facts and response style.
   - Demonstrates few-shot conversational context.

10. `10_context_method_comparison.py`
    - Compares system-prompt context with sample-conversation context.
    - Shows the trade-off between compact factual grounding and demonstrated conversational behavior.

## Chapter decision map

```text
Need persistent chatbot behavior
→ system prompt

Need the current question
→ user prompt

Need prior facts carried forward
→ compact conversation state

Need safer memory
→ structured state

Need a narrow supported domain
→ domain boundary + exact fallback

Need a professional perspective
→ role-playing prompt

Need a small stable knowledge base
→ system-prompt context

Need facts plus response style
→ sample-conversation context

Need production use
→ parse and validate before storing state
```

## Core architecture

```text
system contract
+ recent messages
+ structured state
+ current request
→ answer
+ proposed state update
→ Python validation
→ store, reject, retry, or review
```

## Memory model

Keep these categories separate:

```text
confirmed_facts
→ what is known

recommended_actions
→ what the chatbot suggested

completed_actions
→ what the user actually did

open_questions
→ unresolved information needed later
```

## Important cautions

```text
Providing context
≠ guaranteeing every context item is used

Context grounding
≠ exact source fidelity

Valid JSON
≠ semantically correct state

Prompt boundaries
≠ complete application security

Free-form rolling summaries
→ can drift and turn assumptions into facts
```

## How to run

From the course `lab` folder:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python .\chapter_04\01_dual_prompt_chatbot.py
```

Run the remaining files in numerical order.

## Completion standard

Chapter 4 is complete when you can:

- separate system behavior from the current user request;
- define chatbot role, tone, scope, and fallback behavior;
- compare role-based outputs;
- ground answers with small trusted context;
- carry compact state across turns;
- structure facts, recommendations, actions, and questions separately;
- parse and validate a proposed state update before storing it.
