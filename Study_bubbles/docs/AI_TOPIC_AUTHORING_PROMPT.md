# AI Topic Authoring Prompt (Reusable)

Use this prompt when starting a new StudyBubble topic with ChatGPT/Codex.

---
We are using StudyBubble in:
`D:\Workarea\StudyBook\Study_bubbles`

Task flow:
1. Create a topic plan first.
2. Then create a StudyBubble topic JSON file.

Constraints:
- Keep first version modest (7-15 nodes unless asked otherwise).
- Use groups, nodes, links, and study paths.
- Include definitions for all nodes.
- Include `whyItMatters`, `safeSentence`, `commonTrap`, `interviewAnswer`, `relatedQuestions` where useful.
- Keep interview wording safe and factual.
- Do not invent fake personal experience.
- Keep single-file StudyBubble direction.

Output expectations:
- Show planned groups.
- Show proposed core/support/detail node split.
- Produce `topics/<topic_id>.studybubble.json`.
- If image refs are used, keep local relative paths.

Build/validate commands:
```powershell
..\env_setter.ps1
python -m pytest -q
python -m src.study_bubbles.build_topic --topic topics\<topic_id>.studybubble.json --out outputs\single_file\<topic_id>.html --mode single-file
```

Final report format:
- Files changed
- Validation/build results
- Manual smoke status
---
