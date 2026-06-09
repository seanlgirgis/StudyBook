# Working with the OpenAI API

Canonical DataCamp course package for the **Developing AI Applications** skill track.

- **Track position:** Course 1
- **Canonical slug:** `working_with_the_openai_api`
- **Status:** Completed
- **Platform:** DataCamp

## Course Purpose

This course introduces the Python patterns required to call OpenAI models, control their responses, and build simple conversational applications.

The completed course covers:

- creating an `OpenAI` client
- protecting API keys with environment variables
- sending Chat Completions requests
- selecting a model
- using `system`, `user`, and `assistant` roles
- extracting `response.choices[0].message.content`
- writing specific prompts
- inserting source text with f-strings
- controlling randomness with `temperature`
- limiting output with `max_completion_tokens`
- inspecting input, output, and total token usage
- zero-shot and few-shot prompting
- system-message guardrails
- assistant-message examples
- preserving multi-turn conversation history
- detecting truncated replies with `finish_reason`
- dumping conversation snapshots to JSON and text

## Canonical Folder

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\working_with_the_openai_api
```

## Course Structure

```text
working_with_the_openai_api/
├── docs/
├── lab/
│   ├── python/
│   ├── 00_how_to_run.md
│   └── lab_run_book.md
├── source_material/
├── study_pages/
│   ├── chapter_01_introduction_to_the_openai_api_field_guide.html
│   ├── chapter_02_prompting_openai_models_field_guide.html
│   ├── chapter_03_building_conversations_with_the_openai_api_field_guide.html
│   ├── field_guide.html
│   ├── field_guide.md
│   └── sql_quick_lookup.html
├── index.html
├── README.md
└── STUDYBUBBLE_SESSION_STATE.md
```

## Recommended Study Order

1. Open `index.html`.
2. Review `study_pages/field_guide.html`.
3. Revisit the three chapter guides.
4. Search code patterns in `study_pages/sql_quick_lookup.html`.
5. Run the Python labs in `lab/python`.
6. Review the lab run book.
7. Use the certification-prep digest and code-pattern summary once added.

## Core Request Pattern

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Explain APIs simply."
        }
    ]
)

reply = response.choices[0].message.content
print(reply)
```

## Multi-Turn Pattern

```python
messages.append({
    "role": "user",
    "content": user_text
})

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)

reply = response.choices[0].message.content or ""

messages.append({
    "role": "assistant",
    "content": reply
})
```

The API does not automatically remember prior calls. The application stores and resends the ordered `messages` list.

## Security

Never store a real API key in Python source files.

For a temporary PowerShell session:

```powershell
$env:OPENAI_API_KEY="your-key"
```

The Python client can then use:

```python
client = OpenAI()
```

## Course Closeout

The DataCamp course is complete. All three chapter guides, the accumulated Field Guide, the Markdown guide, and the searchable Quick Lookup are furnished.

Remaining closeout work:

- complete lab documentation
- verify course-root navigation
- link the course from the Developing AI Applications track page
- create certification-prep digest and consolidated code-pattern artifacts
