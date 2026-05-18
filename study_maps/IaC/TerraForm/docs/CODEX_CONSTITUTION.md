# Codex Constitution

- Codex follows strict prompts and MOAG operating law.
- Codex does not design the curriculum freely.
- Codex does not start engine development unless StudyBubble is actually broken.
- Codex does not create project-local scripts.
- Codex does not write real learning artifacts into Study_bubbles engine folders.
- Codex edits source files only, not generated HTML.
- Codex runs commands only when asked or when validation is explicitly part of the prompt.
- Codex reports files changed and commands run.
- Codex treats the folder containing bubbles.ini as the active container root.
- Codex uses stable commands from container root: bubbles build, bubbles sync-layout.
- Codex keeps map work incremental (one cluster/session unless explicitly requested otherwise).
- Codex keeps bubble cards teachable but not crowded.

## Learning Layers

- Bubble Map: visual concept relationships.
- Bubble Study Card: concise teaching card in side panel.
- Hands-On Tutorial: deeper runnable material under tutorials/.

## Linking Rules

- Bubble-specific concept links belong in node-level externalLinks.
- Whole-map links belong in top-level mapResources.
- Do not force whole-map tutorials/labs/setup/neighbor map links into random bubbles.
- Keep mapResources visually separate from selected bubble details when supported.

## Resource Placement

- Place deeper tutorial and lab artifacts under tutorials/, not generated outputs/.
- Do not place runnable lab artifacts under StudyBubble engine folders.
- Do not place runnable lab artifacts under map outputs/.

## Engine Escalation

- Escalate to StudyBubble engine project only for real tool breakage such as build, viewer, image handling, navigation, sync-layout, or mapResources rendering/navigation issues.

## Planned Resource Link Rule

- Do not create dead mapResource links.
- If a mapResource points to a planned tutorial, lab, checklist, or guide, the target file must either already exist or a lightweight under-construction placeholder must be created in the same run.
- If no placeholder is created, do not add the href yet.
- Planned links should be clearly labeled as planned or under construction.
- When the real tutorial/lab is later created, replace the placeholder content with the finished content.

