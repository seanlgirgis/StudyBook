# Questions And Answers Cache

Use this file for repeat questions that Sean is likely to ask again.

Lookup rule:

```text
Search this file early for direct question matches or close paraphrases.
If a matching cached answer exists, return it first with the source path.
```

---

# How do I set the environment for the RAG foundation in PowerShell?

Answer:

```powershell
. "D:\py_venv\rag_application_builder_foundation\set_env.ps1"
```

Notes:

```text
Use Windows PowerShell.
The leading dot and space are required.
This dot-sources the script so the venv, environment variables, and custom prompt stay active in the current session.
```

Source of stored setup:

```text
runbooks/rag_foundation.md
```

Tags:
#questions-cache #rag #environment #powershell #venv #openai

---

# How do I get to my code or examples code for the RAG foundation?

Answer:

```powershell
RagCode
```

Notes:

```text
This uses the RagCode PowerShell function from the environment bootstrap.
It sets the location to:
D:\Workarea\StudyBook\study_maps\DataCamp\skill_tracks\crs_rag_for_generative_ai_applications\foundation\rag_application_builder_foundation\lab\python
```

Source of stored setup:

```text
D:\py_venv\rag_application_builder_foundation\set_env.ps1
```

Tags:
#questions-cache #rag #code #examples #powershell #shortcut

---

# Where is the shared code for the RAG foundation?

Answer:

```text
D:\py_libs\rag_foundation
```

Notes:

```text
This is the central reusable Python library for the RAG foundation.
```

Source of stored setup:

```text
runbooks/rag_foundation.md
```

Tags:
#questions-cache #rag #shared-code #library #path

---

# How do I go to the shared library code for the RAG foundation?

Answer:

```powershell
cd D:\py_libs\rag_foundation
```

Notes:

```text
This goes to the central reusable Python library.
```

Source of stored setup:

```text
runbooks/rag_foundation.md
```

Tags:
#questions-cache #rag #shared-code #library #cd

---

# What do I need to do before using RagCode?

Answer:

```powershell
. "D:\py_venv\rag_application_builder_foundation\set_env.ps1"
```

Notes:

```text
Set the venv first before using RagCode.
RagCode comes from the environment bootstrap, so it is available after the environment is loaded.
```

Source of stored setup:

```text
runbooks/rag_foundation.md
```

Tags:
#questions-cache #rag #RagCode #venv #environment #powershell

---

# What Coursera certificate am I working on?

Answer:

```text
Current Coursera certificate/specialization in progress:
RAG for Generative AI Applications
https://www.coursera.org/specializations/rag-for-generative-ai-applications
```

Notes:

```text
User note:
It is a coursea 4 course track of 4 courses.
When asked about the Coursera certificate being worked on, return this stored item.
```

Source of stored setup:

```text
runbooks/questions_cache.md
```

Tags:
#questions-cache #coursera #certificate #specialization #rag

---

# What Coursera certificate should I look into next?

Answer:

```text
Next certificate to look into:
IBM Generative AI Engineering Professional Certificate
https://www.coursera.org/professional-certificates/ibm-generative-ai-engineering
```

Notes:

```text
Stored from user request as the next Coursera certificate to look into after:
RAG for Generative AI Applications
```

Source of stored setup:

```text
runbooks/questions_cache.md
```

Tags:
#questions-cache #coursera #certificate #ibm #generative-ai
