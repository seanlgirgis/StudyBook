# LearnTerraform

LearnTerraform is a StudyBubble learning-topic container for learning Terraform through StudyBubble maps.

## Opening Paths (Architecture Rule)
- Primary study opening: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\index.html`
- Visual maps: `D:\Workarea\StudyBook\study_maps\IaC\TerraForm\outputs\*.html`
- Runnable labs and hands-on material: `D:\Workarea\StudyBook\tutorials\IaC\TerraForm\...`

This project is a learning-topic container, not StudyBubble engine development.

Normal workflow:
- Teach first.
- Propose bubbles.
- Implement files only when explicitly asked.

Learning layers (MOAG):
- Bubble Map: visual concept map for relationships and study paths.
- Bubble Study Card: concise teaching card in the side panel.
- Hands-On Tutorial/Lab: deeper runnable material under `tutorials/`.

Linking rules:
- Use node `externalLinks` for bubble-specific concept resources.
- Use top-level `mapResources` for whole-map resources (tutorial page, lab, setup, parent/sibling/next maps, glossary/checklists).

Container root rule:
- The active StudyBubble container root is the folder containing `bubbles.ini`.

Central commands from this container:
- `bubbles build`
- `bubbles sync-layout`

Do not hand-edit generated HTML under `outputs/`.
Do not store runnable lab artifacts in generated outputs or StudyBubble engine folders.
