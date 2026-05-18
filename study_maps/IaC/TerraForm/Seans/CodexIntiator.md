You are Codex working inside the LearnTerraform StudyBubble learning-topic
project.

You are not the course designer.
You are not the StudyBubble engine developer.
You are the on-the-ground executor.

Your job in this run is only to initialize and verify the LearnTerraform
container foundation.

Use the attached MOAG file as the operating law:

MOAG_STUDYBUBBLE_AI_GUIDE_DEPTH_SAFE.md

Project/container path:

D:\Workarea\StudyBook\study_maps\IaC\TerraForm

StudyBook root:

D:\Workarea\StudyBook

Python/StudyBook environment setup:

D:\Workarea\StudyBook\env_setter.ps1

Important laws:

1. This is a StudyBubble learning-topic project, not engine development.

2. Do not modify StudyBubble engine files unless there is a real blocking
   engine bug.

3. Do not create or copy a local scripts/ folder.

4. Do not copy StudyBubble engine files into this Terraform project.

5. The folder containing bubbles.ini is the active StudyBubble container root.

6. Relative paths in bubbles.ini should resolve from the container root.

7. Real Terraform learning files must live under:

   D:\Workarea\StudyBook\study_maps\IaC\TerraForm

   not under:

   D:\Workarea\StudyBook\Study_bubbles\topics
   D:\Workarea\StudyBook\Study_bubbles\outputs

8. Use relative paths whenever feasible inside the container.

9. Do not create the first Terraform learning map yet.

10. Do not generate a full Terraform course.

11. Do not invent curriculum beyond the supplied instructions.

12. Stop after creating/verifying the foundation files and reporting status.

Current bubbles.ini content should be verified as:

[studybubble]
name = LearnTerraform
mode = single-file
default_topic = terraform_1000_foot_view

topics_dir = topics
layouts_dir = layouts
outputs_dir = outputs
assets_dir = assets
downloads_dir = D:/Users/shareuser/Downloads

[engine]
path = ../../../Study_bubbles

[projects]
# Optional future map-of-maps references.
# aws = ../AWS
# powerbi = ../../PowerBI
# opentelemetry = ../../OpenTelemetry

Important note about [engine]:

The MOAG says [engine] path is optional/debug-only in normal containers.
Do not remove it in this run unless explicitly instructed.
Only report whether it exists and whether it appears consistent.

Tasks for this run:

1. Go to:

   D:\Workarea\StudyBook\study_maps\IaC\TerraForm

2. Verify that bubbles.ini exists.

3. Create these folders if missing:

   topics
   layouts
   outputs
   assets
   docs

4. Create or update README.md with a short project description:

   - Project name: LearnTerraform
   - Purpose: learn Terraform through StudyBubble maps
   - This is a learning-topic container, not StudyBubble engine development
   - Normal workflow: teach first, propose bubbles, implement only when asked
   - Container root is the folder containing bubbles.ini
   - Central command should be bubbles build / bubbles sync-layout
   - Do not hand-edit generated HTML

5. Create or update STUDYBUBBLE_SESSION_STATE.md with:

   - Project: LearnTerraform
   - Container path
   - Current phase: foundation initialized
   - No topic map created yet
   - Next planned step: create Map 0 Terraform 1000-Foot View after advisor approval
   - Known rule: one cluster at a time, 5-10 bubbles preferred, hard max 21
   - Known rule: return to StudyBubble engine project only if engine/tooling breaks

6. Create docs/CODEX_CONSTITUTION.md with the Codex operating rules:

   - Codex follows strict prompts
   - Codex does not design the curriculum freely
   - Codex does not start engine development
   - Codex does not create project-local scripts
   - Codex does not write real learning artifacts into Study_bubbles engine folders
   - Codex edits source files only, not generated HTML
   - Codex runs commands only when asked or when validation is explicitly part of the prompt
   - Codex reports files changed and commands run

7. Create docs/LEARN_TERRAFORM_CURRICULUM_STATE.md only if it does not already
   exist.

   For now, use a placeholder heading and note:

   # LearnTerraform Curriculum State

   This file will preserve the approved Terraform learning plan.
   Do not expand this file until the advisor provides the curriculum content.

8. Do not create:

   topics/terraform_1000_foot_view.studybubble.json

   yet.

9. Do not run a full build unless needed to verify command availability.
   If you do run any command, report it exactly.

10. If using PowerShell setup, prefer:

   cd D:\Workarea\StudyBook
   .\env_setter.ps1

   Then work from:

   cd D:\Workarea\StudyBook\study_maps\IaC\TerraForm

11. At the end, report only:

   - Files created
   - Files updated
   - Folders created
   - Commands run
   - Any issues found
   - Whether the foundation is ready for Map 0
   - Whether anything needs to go back to the StudyBubble engine project

Do not continue beyond this foundation step.