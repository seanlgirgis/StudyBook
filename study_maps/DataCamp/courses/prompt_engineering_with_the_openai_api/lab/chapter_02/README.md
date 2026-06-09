# Chapter 2 Lab — Advanced Prompt Engineering Strategies

This folder preserves Chapter 2 as a small, replayable sequence of prompting experiments.

## Run order

1. `01_zero_shot_prompting.py`
   - Gives the task with no examples.
   - Uses explicit allowed labels to keep the answer controlled.

2. `02_one_shot_prompting.py`
   - Adds one user/assistant example pair.
   - Keeps the system message so the full label set remains explicit.

3. `03_few_shot_prompting.py`
   - Provides one representative example for each sentiment class.
   - Demonstrates that examples should cover the complete classification space.

4. `04_multi_step_prompting.py`
   - Uses dependent stages: identify the problem, infer the trigger, then choose the first action.
   - Sean's memory label: **tiered response pattern**.

5. `05_chain_of_thought_prompting.py`
   - Requests a visible calculation and final answer.
   - Useful for inspection, but often excessive for trivial arithmetic.

6. `06_few_shot_reasoning.py`
   - Demonstrates the desired brief calculation format with one example.
   - Produces a concise answer instead of a long explanation.

7. `07_self_consistency_prompting.py`
   - Compares several candidate calculations and uses a majority result.
   - Shows the basic self-consistency idea.

8. `08_incident_root_cause_consistency.py`
   - Generates competing root-cause hypotheses and supporting clues.
   - Demonstrates that a plausible hypothesis is not a confirmed root cause.

9. `09_temperature_comparison.py`
   - Compares temperature `0.0` with `0.7`.
   - Shows that higher temperature permits variation but does not guarantee meaningfully different reasoning.

## Chapter decision map

```text
No example needed
→ zero-shot

Need one demonstrated format
→ one-shot

Need several classes or patterns
→ few-shot

Task has dependent stages
→ multi-step prompting

Need a brief visible calculation
→ reasoning prompt

Need several candidate approaches
→ self-consistency

Need predictable classification or extraction
→ low temperature

Need diverse ideas or hypotheses
→ moderate temperature, followed by validation
```

## Core distinctions

```text
Shots
→ number of examples supplied

Steps
→ stages inside the task

System message
→ defines persistent rules and the valid answer space

Example pairs
→ demonstrate how to behave inside that space
```

## Trust rule

An LLM-generated hypothesis is not a confirmed fact or root cause.

Use model output to guide investigation, then verify with:

- logs
- metrics
- traces
- deployment diffs
- tests
- source code
- deterministic calculations

## How to run

From the course `lab` folder:

```powershell
$env:PYTHONPATH = (Get-Location).Path
python .\chapter_02\01_zero_shot_prompting.py
```

Run the remaining files in numerical order.
