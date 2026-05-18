# StudyBubble v1 Closure Handoff

## 1. Current status
StudyBubble is now a usable StudyBook visual study-map engine.

It is not a finished commercial product, but it is ready to use for real study topics.

Recommended next use:
Use `MOAG_STUDYBUBBLE_AI_GUIDE.md` with another GenAI session to study one topic incrementally, starting with Terraform, Power BI, Tableau, AWS, Kubernetes, OpenTelemetry, or another topic.

## 2. Project identity
StudyBubble is:
- static
- single-file output
- data-driven
- no React
- no npm
- no backend
- no database
- no local server required
- meant for StudyBook learning and interview rehearsal

Core flow:
topic notes / topic plan
  -> StudyBubble topic JSON
  -> validate
  -> build
  -> standalone HTML
  -> study / drag / export layout
  -> sync layout / rebuild

## 3. Repository paths
Use relative paths from StudyBook root where possible.

StudyBook root:
.

StudyBubble engine:
Study_bubbles/

Study topic workspace:
study_maps/

Engine demo topic JSON:
Study_bubbles/topics/

Engine demo generated HTML:
Study_bubbles/outputs/single_file/

Engine demo layouts:
Study_bubbles/layouts/

Real study container:
study_maps/<ProjectName>/bubbles.ini
study_maps/<ProjectName>/topics/
study_maps/<ProjectName>/layouts/
study_maps/<ProjectName>/outputs/
study_maps/<ProjectName>/assets/

MOAG:
Study_bubbles/docs/MOAG_STUDYBUBBLE_AI_GUIDE.md

Important local example:
D:\Workarea\StudyBook

## 4. Environment and commands
From StudyBook root:

.\env_setter.ps1
cd Study_bubbles
python -m pytest -q

Build topic:

python -m src.study_bubbles.build_topic --topic topics\<topic_id>.studybubble.json --out outputs\single_file\<topic_id>.html --mode single-file

Build with layout:

python -m src.study_bubbles.build_topic --topic topics\<topic_id>.studybubble.json --layout layouts\<topic_id>.layout.json --out outputs\single_file\<topic_id>.html --mode single-file

One-command layout sync and rebuild:

python tools\sync_layouts_and_rebuild.py

## 5. Major milestones completed
- v0.7 BOA interaction parity:
  minimap, zoom HUD, pan, fit/reset, drag mode, context menu, focus/filter behavior, study path highlighting, keyboard hints.

- v0.9 Study Card + Media + Links:
  side-panel study cards, common traps, interview answers, related questions, note summaries, images, captions, external links, copy buttons.

- v1.0 Usable Release Package:
  release folder, index page, release docs/checklist, direct-open package.

- post-v1 practical improvements:
  resizable side panel
  group bubble colors
  manual layout export/import
  one-command layout sync/rebuild
  independent map pane vs side-panel scroll
  builder image asset copy/resizing
  StudyBook integration docs/templates
  MOAG StudyBubble AI guide

## 6. Important tags
- studybubble-boa-interaction-parity-v1
- studybubble-study-card-media-links-v1
- studybubble-v1.0-usable-release
- studybubble-group-colors-v1
- studybubble-independent-map-pane-v1
- studybubble-builder-image-sizing-v1 (expected/planned tag may need verification)
- studybubble-studybook-integration-v1 (expected/planned tag may need verification)
- studybubble-moag-ai-guide-v1

## 7. Current stable feature set
- standalone single-file HTML output
- direct-open browser usage
- validator and pytest suite
- parent/child/grandchild navigation
- side panel study card
- search and group filters
- study paths
- minimap
- zoom/pan/fit/reset
- drag mode
- context menu
- group coloring
- resizable side panel
- independent map pane and internal side scroll
- image support and builder resizing
- external links
- layout export/import
- one-command sync and rebuild
- StudyBook topic workbench structure
- MOAG guide for any GenAI

## 8. Known accepted warning
The browser may show:

file:// unique-origin warning

This is accepted for direct-open local HTML and is not blocking.

Blocking errors are:
- TypeError
- ReferenceError
- SyntaxError
- blank map
- bubbles not rendering
- broken navigation
- required image asset not found
- layout export/import failure
- side panel/map layout regression

## 9. Source-of-truth rules
Generated HTML files are not hand-maintained source.

Do not hand edit:
outputs/single_file/*.html

Edit:
viewer/
src/study_bubbles/
study_bubbles/
topics/
layouts/
docs/
templates/

Then rebuild.

## 10. Study workflow going forward
For a new topic:
1. Open a new GenAI session.
2. Upload/paste:
   docs/MOAG_STUDYBUBBLE_AI_GUIDE.md
3. Tell it:
   "I want to study <topic> using StudyBubble."
4. Work one cluster at a time.
5. Store study material and topic JSON in:
   study_maps/<ProjectName>/topics/
6. Build from the project container folder using:
   ../../scripts/bubbles.ps1 build
7. Output HTML remains inside:
   study_maps/<ProjectName>/outputs/

## 11. Topic growth model
bubble -> cluster -> island -> city -> continent

Meaning:
- one concept becomes a bubble
- one study session becomes a cluster
- clusters form subtopic islands
- subtopics form topic cities
- topic maps can become bubbles in larger continent maps

## 12. When to come back to this StudyBubble project
Only come back for engine-level work when:
- builder fails
- viewer breaks
- generated map has serious runtime errors
- layout workflow fails
- image handling fails
- navigation breaks
- a feature gap blocks actual studying

Do not keep adding features just because they sound nice.

## 13. Next recommended real use
Start with Terraform Basics as a stress-test topic.

Suggested first cluster:
Terraform Core Workflow:
- Terraform
- Configuration
- Provider
- Resource
- Plan
- Apply
- State

Do not build the full Terraform map in one shot.

## 14. Closing summary
StudyBubble is ready to leave engine-building mode and enter real study mode.
Future development should be driven by real study pain, not speculative features.
