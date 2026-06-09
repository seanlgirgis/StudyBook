# Chapter 1 Lab — Introduction to Prompt Engineering Best Practices

This folder preserves the Chapter 1 learning sequence as small, replayable exercises.

## Run order

1. `01_message_roles.py`
   - Uses system and user roles.
   - Shows how the system message controls assistant behavior.

2. `02_simple_get_response.py`
   - Sends one prompt through the reusable `OpenAIService`.
   - Keeps API plumbing separate from the study code.

3. `03_system_role_and_constraints.py`
   - Combines a system role with explicit response constraints.
   - Demonstrates control over tone and length.

4. `04_weak_vs_precise_prompt.py`
   - Compares a broad prompt with a specific prompt.
   - Shows how audience, scope, required concepts, and length improve predictability.

5. `05_delimited_prompt_f_string.py`
   - Inserts source text using an f-string.
   - Separates instructions from input using triple backticks.

6. `06_structured_output.py`
   - Requests a predictable labeled response.
   - Demonstrates output formats that are easier to read and process.

7. `07_conditional_prompt.py`
   - Adds prompt-based branching.
   - Produces different output depending on whether a deadline is present.

8. `08_support_ticket_analysis.py`
   - Combines delimiters, conditions, and structured output.
   - Applies the chapter skills to a realistic support-ticket example.

## How to run

From the `lab` folder:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python .\chapter_01\01_message_roles.py