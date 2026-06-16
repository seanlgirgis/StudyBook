# RAG Foundation Local Memory

## Purpose

This memory documents the complete local setup for the **RAG Application Builder Foundation** and its shared reusable Python library.

It is intended to be saved into Sean's local-memory project so Codex or another assistant can answer questions such as:

```text
Where is the RAG foundation?
How do I activate the environment?
Where are the API keys stored?
Which Python version is used?
Where is the shared library?
How is the library installed?
How do I test the environment?
How do I run the first lab?
How should reusable code be promoted?
How is watsonx.ai incorporated?
What should be backed up or committed to Git?
```

This file is the operational source of truth for the current setup.

---

# 1. System overview

The setup has three distinct layers:

```text
1. StudyBook foundation
   = learning materials, tiny labs, course alignment, and documentation

2. Central Python virtual environment
   = isolated Python runtime and installed dependencies

3. Central reusable Python library
   = permanent, production-quality shared source code
```

The separation is intentional.

```text
StudyBook
→ learning and experimentation

D:\py_venv
→ disposable runtime environment

D:\py_libs
→ permanent reusable code
```

---

# 2. Main StudyBook foundation path

The local RAG preparation project is:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\
crs_rag_for_generative_ai_applications\
foundation\
rag_application_builder_foundation
```

Primary landing page:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\
crs_rag_for_generative_ai_applications\
foundation\
rag_application_builder_foundation\
index.html
```

This project is not an official fifth Coursera course.

It is the local preparation layer for the IBM Coursera specialization:

```text
RAG for Generative AI Applications
```

Provider:

```text
IBM
```

Official specialization course count:

```text
4
```

The foundation exists to:

```text
reuse completed DataCamp learning
→ build transparent AI application skills
→ strengthen prompting
→ build RAG components in tiny Lego-style labs
→ incorporate OpenAI and IBM watsonx.ai
→ prepare for the four IBM Coursera courses
```

---

# 3. Foundation folder structure

Important paths:

```text
rag_application_builder_foundation\
  index.html
  README.md
  ROADMAP.md
  STUDYBUBBLE_SESSION_STATE.md

  docs\
    BILL_OF_MATERIALS.md
    DATACAMP_REUSE_MAP.md
    COURSE_ALIGNMENT_MATRIX.md
    MONITORING_PLAN.md

  source_material\
    datacamp\
    coursera\
      COURSE_RECONNAISSANCE.md
    ibm_watsonx\
    archive\

  study_pages\
    field_guide.md
    rag_application_quick_lookup.md

  lab\
    00_how_to_run.md
    lab_run_book.md
    requirements.txt
    .env.example
    .gitignore

    python\
      stage_01_application_basics\
      stage_02_prompt_engineering\
      stage_03_document_processing\
      stage_04_embeddings_and_vectors\
      stage_05_retrieval\
      stage_06_grounded_generation\
      stage_07_complete_rag\
      stage_08_evaluation_and_observability\
      stage_09_watsonx_comparison\

    data\
    documents\
    vector_stores\
    expected_outputs\
    notes\
    logs\
    tests\
```

---

# 4. Current active lab

Current active stage:

```text
Stage 1 — Application Basics
```

Current working directory:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\
crs_rag_for_generative_ai_applications\
foundation\
rag_application_builder_foundation\
lab\python\stage_01_application_basics
```

Current first script:

```text
01_first_request.py
```

Full path:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\
crs_rag_for_generative_ai_applications\
foundation\
rag_application_builder_foundation\
lab\python\stage_01_application_basics\
01_first_request.py
```

The script has already run successfully.

Validated behavior:

```text
input printed
→ model selected
→ OpenAI request sent
→ model output returned
→ request ID captured
```

Known successful model:

```text
gpt-5.4-mini
```

---

# 5. Python version decision

The machine has multiple Python installations.

Detected:

```text
Python 3.14.3
C:\Users\shareuser\AppData\Local\Python\pythoncore-3.14-64\python.exe
```

and:

```text
Python 3.13.11
C:\Users\shareuser\AppData\Roaming\uv\python\
cpython-3.13.11-windows-x86_64-none\
python.exe
```

The RAG foundation intentionally uses:

```text
Python 3.13.11
```

Reason:

```text
Python 3.14 is very new.
Some AI, vector, and scientific packages may lag behind it.
Python 3.13 is the safer compatibility choice for this project.
```

---

# 6. Central virtual environment

The RAG foundation virtual environment is centralized outside the repository.

Path:

```text
D:\py_venv\rag_application_builder_foundation
```

This is preferred over keeping `.venv` inside the StudyBook repository.

The environment was created with:

```powershell
& "C:\Users\shareuser\AppData\Roaming\uv\python\cpython-3.13.11-windows-x86_64-none\python.exe" `
  -m venv "D:\py_venv\rag_application_builder_foundation"
```

Activation script:

```text
D:\py_venv\rag_application_builder_foundation\Scripts\Activate.ps1
```

Direct activation command:

```powershell
& "D:\py_venv\rag_application_builder_foundation\Scripts\Activate.ps1"
```

Expected active interpreter:

```text
D:\py_venv\rag_application_builder_foundation\Scripts\python.exe
```

Expected Python version:

```text
Python 3.13.11
```

---

# 7. Central environment bootstrap script

The main environment bootstrap file is:

```text
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

This file is intentionally outside the repository.

It performs these jobs:

```text
activate the central virtual environment
set OPENAI_API_KEY
set OPENAI_MODEL
prepare watsonx.ai environment variables
set LOCAL_AI_BUDGET_USD
display active Python and configuration
shorten the PowerShell prompt
```

Load it from any PowerShell folder with:

```powershell
. "D:\py_venv\rag_application_builder_foundation\set_env.ps1"
```

The leading dot and space are required.

This is called **dot-sourcing**.

Dot-sourcing ensures that:

```text
the venv remains active
the environment variables remain available
the custom prompt remains active
```

inside the current PowerShell session.

---

# 8. Environment variables

Current OpenAI variables:

```text
OPENAI_API_KEY
OPENAI_MODEL
```

Current model:

```text
gpt-5.4-mini
```

The API key is stored in:

```text
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

This keeps it outside Git repositories.

Important security note:

```text
outside Git
does not mean encrypted
```

The file remains plain-text local secret storage.

Future IBM watsonx.ai variables prepared in the script:

```text
WATSONX_API_KEY
WATSONX_PROJECT_ID
WATSONX_URL
WATSONX_MODEL_ID
```

Local learning budget variable:

```text
LOCAL_AI_BUDGET_USD
```

Important distinction:

```text
LOCAL_AI_BUDGET_USD
= local learning budget configuration

It is not the same as:
actual OpenAI or IBM account credit remaining
```

---

# 9. PowerShell execution policy fix

The bootstrap script initially failed because PowerShell considered it unsigned.

The permanent user-level development setting is:

```powershell
Set-ExecutionPolicy `
  -Scope CurrentUser `
  -ExecutionPolicy RemoteSigned
```

Current execution policy situation after correction:

```text
MachinePolicy: Undefined
UserPolicy: Undefined
Process: Undefined
CurrentUser: RemoteSigned
LocalMachine: RemoteSigned
```

Downloaded-file markers can be removed with:

```powershell
Unblock-File `
  "D:\py_venv\rag_application_builder_foundation\set_env.ps1"
```

Normal startup should now work without repeating the unblock step:

```powershell
. "D:\py_venv\rag_application_builder_foundation\set_env.ps1"
```

Only unblock again if the file is replaced by a newly downloaded copy that carries a new internet-origin marker.

---

# 10. Short PowerShell prompt

The environment bootstrap defines a short prompt.

Instead of showing the full path:

```text
(rag_application_builder_foundation) PS D:\Workarea\StudyBook\...
```

the prompt appears as:

```text
(rag_application_builder_foundation) stage_01_application_basics>
```

The real directory is unchanged.

To display the full path at any time:

```powershell
pwd
```

or:

```powershell
$PWD
```

The short prompt belongs in:

```text
set_env.ps1
```

rather than the general PowerShell profile.

This gives environment-specific behavior:

```text
normal shell
→ normal prompt

RAG shell
→ short RAG prompt
```

---

# 11. How to activate and verify the full environment

From a new PowerShell window:

```powershell
. "D:\py_venv\rag_application_builder_foundation\set_env.ps1"
```

Then verify:

```powershell
python --version
```

Expected:

```text
Python 3.13.11
```

Verify interpreter:

```powershell
python -c "import sys; print(sys.executable)"
```

Expected:

```text
D:\py_venv\rag_application_builder_foundation\Scripts\python.exe
```

Verify environment root:

```powershell
$env:VIRTUAL_ENV
```

Expected:

```text
D:\py_venv\rag_application_builder_foundation
```

Verify model:

```powershell
$env:OPENAI_MODEL
```

Expected:

```text
gpt-5.4-mini
```

---

# 12. Central reusable Python library

Permanent shared library path:

```text
D:\py_libs\rag_foundation
```

This is separate from the virtual environment.

The design rule is:

```text
D:\py_venv
= disposable runtime

D:\py_libs
= permanent reusable source
```

Never store permanent library source inside the virtual environment.

A virtual environment may be deleted and recreated.

The shared library should survive independently.

---

# 13. Shared library structure

Current intended structure:

```text
D:\py_libs\rag_foundation\
  pyproject.toml
  README.md

  src\
    rag_foundation\
      __init__.py
      config.py
      exceptions.py

      models\
        __init__.py
        text_generation.py

      providers\
        __init__.py
        base.py
        openai_text.py

      validation\
      retrieval\
      monitoring\

  tests\
    test_config.py
    test_text_generation_models.py
    test_openai_text_provider.py

  docs\
    OPENAI_TEXT_PROVIDER.md
```

The library uses the standard `src` layout.

Import name:

```python
import rag_foundation
```

Distribution/package name:

```text
rag-foundation
```

---

# 14. Shared library package metadata

Package configuration file:

```text
D:\py_libs\rag_foundation\pyproject.toml
```

Current package metadata:

```toml
[build-system]
requires = ["setuptools>=77", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "rag-foundation"
version = "0.1.0"
description = "Reusable helpers developed through the RAG Application Builder Foundation."
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "openai",
    "python-dotenv"
]

[tool.setuptools.packages.find]
where = ["src"]
```

Important Windows encoding issue:

```text
pyproject.toml must be UTF-8 without BOM
```

The initial install failed because Windows PowerShell wrote a BOM.

Correct no-BOM writing pattern:

```powershell
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

[System.IO.File]::WriteAllText(
    "D:\py_libs\rag_foundation\pyproject.toml",
    $content,
    $utf8NoBom
)
```

---

# 15. Editable installation

The central library is installed into the RAG virtual environment in editable mode.

Command:

```powershell
python -m pip install -e "D:\py_libs\rag_foundation"
```

Editable install means:

```text
Python imports the central library normally
but source changes under D:\py_libs are visible immediately
without reinstalling after every edit
```

Verify import:

```powershell
python -c "import rag_foundation; print(rag_foundation.__file__)"
```

Expected:

```text
D:\py_libs\rag_foundation\src\rag_foundation\__init__.py
```

The editable install has already been validated successfully.

---

# 16. Current reusable configuration helper

Current file:

```text
D:\py_libs\rag_foundation\src\rag_foundation\config.py
```

Current tested import:

```python
from rag_foundation.config import require_env
```

Validated test:

```powershell
python -c "from rag_foundation.config import require_env; print(require_env('OPENAI_MODEL'))"
```

Validated output:

```text
gpt-5.4-mini
```

---

# 17. Library quality standard

Anything under:

```text
D:\py_libs\rag_foundation
```

must be treated as production-quality code.

Future library files must include:

```text
clear module docstrings
clear class and function docstrings
type hints
explicit exceptions
documented inputs and outputs
documented side effects
focused tests
stable public interfaces
examples where useful
no unexplained shortcuts
no incomplete learning stubs
```

The library is not a scratchpad.

Learning scripts can be small and visible.

Shared library code must be polished, documented, tested, and reusable.

---

# 18. Promotion rule for reusable code

Reusable code should not be moved into the central library immediately.

Use this process:

```text
1. Build the behavior visibly in a small lab script.
2. Run it successfully.
3. Inspect the inputs and outputs.
4. Explain what each component does.
5. Notice the repeated plumbing.
6. Extract the reusable part.
7. Add full documentation.
8. Add tests.
9. Promote it to D:\py_libs\rag_foundation.
10. Use it from later lesson scripts.
```

A reusable pattern should ideally be promoted only after:

```text
it has been understood
it has been validated
it is useful in more than one place
```

---

# 19. Learning-script versus shared-library boundary

Use this rule:

```text
Reusable technical plumbing
→ central library

Concept being studied
→ lesson script
```

For example, from `01_first_request.py`:

Keep in the lesson script:

```text
the prompt
the concept-specific output
the lesson explanation
the input/output display
```

Move to the shared library:

```text
environment lookup
client creation
provider request
provider exception handling
response normalization
metadata extraction
```

Desired future lesson style:

```python
from rag_foundation import OpenAITextProvider, TextGenerationRequest

provider = OpenAITextProvider()

request = TextGenerationRequest(
    prompt="Explain an AI application in one sentence."
)

result = provider.generate(request)

print(result.text)
print(result.request_id)
```

---

# 20. Generic provider architecture

The shared library is being designed to support multiple model providers.

Provider-neutral concepts:

```text
TextGenerationProvider
TextGenerationRequest
TextGenerationResult
```

Current OpenAI provider:

```text
OpenAITextProvider
```

Future provider:

```text
WatsonxTextProvider
```

The goal is:

```python
result = provider.generate(request)
```

without hiding access to provider-specific features.

---

# 21. Fine-grained access requirement

The library must support both:

```text
clean generic access
and
fine provider-specific access
```

Normalized access:

```python
result.text
result.provider
result.model
result.request_id
```

Fine access to original response:

```python
result.raw_response
```

Fine access to provider SDK client:

```python
provider.client
```

This prevents the abstraction from becoming a prison.

Use the generic interface for normal code.

Use the raw client or raw response only when a provider-specific capability is genuinely needed.

---

# 22. Current production library package

The first production-quality package includes:

```text
src\rag_foundation\exceptions.py
src\rag_foundation\config.py
src\rag_foundation\models\__init__.py
src\rag_foundation\models\text_generation.py
src\rag_foundation\providers\__init__.py
src\rag_foundation\providers\base.py
src\rag_foundation\providers\openai_text.py
src\rag_foundation\__init__.py

tests\test_config.py
tests\test_text_generation_models.py
tests\test_openai_text_provider.py

docs\OPENAI_TEXT_PROVIDER.md
```

The tests use a fake OpenAI client.

They should not consume API tokens.

Run tests from:

```powershell
cd D:\py_libs\rag_foundation
python -m unittest discover -s tests -v
```

---

# 23. OpenAI provider usage

Normal use:

```python
from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)

provider = OpenAITextProvider()

request = TextGenerationRequest(
    prompt="Explain RAG simply."
)

result = provider.generate(request)

print(result.text)
print(result.request_id)
```

Concise use:

```python
from rag_foundation import OpenAITextProvider

provider = OpenAITextProvider()

text = provider.generate_text(
    "Explain embeddings in plain English."
)

print(text)
```

Fine-grained use:

```python
from rag_foundation import (
    OpenAITextProvider,
    TextGenerationRequest,
)

provider = OpenAITextProvider()

request = TextGenerationRequest(
    prompt="Explain RAG.",
    provider_options={
        "store": False,
    },
)

result = provider.generate(request)

print(result.text)

raw_response = result.raw_response
client = provider.client
```

---

# 24. How to run the current lab from a new shell

Open Windows PowerShell.

Load the environment:

```powershell
. "D:\py_venv\rag_application_builder_foundation\set_env.ps1"
```

Go to Stage 1:

```powershell
cd "D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation\lab\python\stage_01_application_basics"
```

Run the current script:

```powershell
python .\01_first_request.py
```

Expected broad behavior:

```text
INPUT
LOCAL PYTHON
MODEL OUTPUT
REQUEST ID
```

Convenience command for getting to the RAG foundation Python code/examples folder:

```powershell
RagCode
```

This uses the PowerShell function defined in:

```text
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

It sets the location to:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation\lab\python
```

---

# 25. DataCamp reuse strategy

Existing DataCamp sources to reuse selectively:

```text
Working with the OpenAI API
Prompt Engineering with the OpenAI API
Working with Hugging Face
AI Ethics
Introduction to Data Privacy
```

Canonical DataCamp course folders remain unchanged.

Do not move or rename them.

Reuse pattern:

```text
reference original course
→ adapt small useful pattern
→ preserve source path
→ avoid copying entire course package
```

Current reuse map:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\
crs_rag_for_generative_ai_applications\
foundation\
rag_application_builder_foundation\
docs\
DATACAMP_REUSE_MAP.md
```

---

# 26. IBM watsonx.ai strategy

Sean has created a free watsonx.ai account.

watsonx.ai should be incorporated where it adds learning value.

Do not duplicate every OpenAI exercise for watsonx.ai.

Use watsonx.ai for:

```text
selected provider comparisons
IBM-specific Coursera alignment
one direct model request
one structured response comparison
embedding or retrieval comparison when useful
authentication and project configuration learning
```

OpenAI remains the primary local provider.

Coursera-required IBM or Hugging Face work remains valid official course evidence.

---

# 27. Monitoring and observability plan

The future shared library should progressively track:

```text
request count
provider
model
input tokens
output tokens
total tokens
estimated local cost
configured local budget
estimated local remaining budget
latency
retries
failures
tool calls
embedding requests
retrieval latency
retrieved chunk scores
source coverage
RAG answer quality
```

Important distinction:

```text
provider account credit
is not automatically equal to
locally calculated remaining project budget
```

Local calculation:

```text
configured local budget
-
tracked estimated cost
=
estimated local remaining budget
```

---

# 28. Git and backup strategy

Recommended:

```text
D:\py_libs\rag_foundation
```

should become its own Git repository.

The virtual environment should not be committed.

```text
Commit:
D:\py_libs\rag_foundation

Do not commit:
D:\py_venv\rag_application_builder_foundation
```

The local secret bootstrap should remain outside Git:

```text
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

Backup recommendations:

```text
Back up:
D:\py_libs\rag_foundation
set_env.ps1 through a secure local backup process
important StudyBook foundation docs

Do not normally back up:
the entire virtual environment
```

The venv can be rebuilt from:

```text
Python version
pyproject.toml
package dependencies
editable install command
```

Sean's existing `gitqall.ps1` can be used to synchronize the shared-library repository if configured to include it.

The E-drive backup can protect Git-ignored or local-only files when needed.

---

# 29. Rebuild procedure

If the virtual environment is lost or corrupted:

## Step 1 — recreate it

```powershell
& "C:\Users\shareuser\AppData\Roaming\uv\python\cpython-3.13.11-windows-x86_64-none\python.exe" `
  -m venv "D:\py_venv\rag_application_builder_foundation"
```

## Step 2 — activate it

```powershell
& "D:\py_venv\rag_application_builder_foundation\Scripts\Activate.ps1"
```

## Step 3 — upgrade packaging tools

```powershell
python -m pip install --upgrade pip setuptools wheel
```

## Step 4 — install shared library editable

```powershell
python -m pip install -e "D:\py_libs\rag_foundation"
```

## Step 5 — restore or recreate `set_env.ps1`

Path:

```text
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

## Step 6 — verify

```powershell
python --version
python -c "import rag_foundation; print(rag_foundation.__file__)"
```

---

# 30. Common questions Codex should answer

## Where is the RAG foundation?

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\
crs_rag_for_generative_ai_applications\
foundation\
rag_application_builder_foundation
```

## Where is the virtual environment?

```text
D:\py_venv\rag_application_builder_foundation
```

## How do I activate everything?

```powershell
. "D:\py_venv\rag_application_builder_foundation\set_env.ps1"
```

## Where is the central shared library?

```text
D:\py_libs\rag_foundation
```

## How is the library installed?

```powershell
python -m pip install -e "D:\py_libs\rag_foundation"
```

## How do I verify the import?

```powershell
python -c "import rag_foundation; print(rag_foundation.__file__)"
```

## Where are the OpenAI settings?

```text
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

## Where is the current first lab?

```text
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\
crs_rag_for_generative_ai_applications\
foundation\
rag_application_builder_foundation\
lab\python\stage_01_application_basics\
01_first_request.py
```

## How do I run the first lab?

```powershell
python .\01_first_request.py
```

## How do I run library tests?

```powershell
cd D:\py_libs\rag_foundation
python -m unittest discover -s tests -v
```

## What Python version should be used?

```text
Python 3.13.11
```

## Why not Python 3.14?

```text
Python 3.14 is newer and may have weaker compatibility with some AI,
vector, and scientific packages.
```

---

# 31. Codex operating rules for this setup

Codex should follow these rules:

```text
1. Do not move or rename the canonical StudyBook foundation.
2. Do not move permanent library source into the virtual environment.
3. Do not commit the virtual environment.
4. Do not expose or print API keys.
5. Treat D:\py_libs\rag_foundation as production-quality code.
6. Add full documentation and tests for shared-library changes.
7. Keep lesson scripts small and concept-focused.
8. Promote code only after it is understood and validated.
9. Preserve fine-grained provider access.
10. Use Python 3.13.11 for this environment.
11. Use editable install during development.
12. Keep OpenAI primary and watsonx.ai selective.
13. Sean handles Git unless explicitly requested otherwise.
14. Do not overbuild future modules before the relevant learning stage.
```

---

# 32. Current next step

Current next technical step:

```text
Extract the production-quality provider classes into:
D:\py_libs\rag_foundation
```

Then run:

```powershell
cd D:\py_libs\rag_foundation
python -m unittest discover -s tests -v
```

After tests pass:

```text
rewrite 01_first_request.py
to use the central OpenAITextProvider
while keeping the prompt and output visible
```

---

# 33. Final architecture summary

```text
StudyBook foundation
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\
crs_rag_for_generative_ai_applications\
foundation\
rag_application_builder_foundation

Central virtual environment
D:\py_venv\rag_application_builder_foundation

Environment bootstrap and secrets
D:\py_venv\rag_application_builder_foundation\set_env.ps1

Central reusable Python library
D:\py_libs\rag_foundation

Current Python
Python 3.13.11

Current OpenAI model
gpt-5.4-mini

Current active lab
stage_01_application_basics\01_first_request.py
```

The governing principle is:

```text
Understand visibly.
Promote repeated plumbing.
Document shared code fully.
Test production helpers.
Keep learning scripts concise.
Preserve direct provider access.
```
