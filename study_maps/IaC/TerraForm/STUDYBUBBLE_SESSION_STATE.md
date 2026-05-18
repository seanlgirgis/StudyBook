# StudyBubble Session State

- Project: LearnTerraform
- Container path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm
- Current phase: Map -1 visual created before Map 0
- Map -1 created:
  - topic id: iac_why_terraform_exists
  - topic JSON path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/topics/iac_why_terraform_exists.studybubble.json
  - image asset path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/assets/iac_landscape_overview.svg
  - generated HTML path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/outputs/iac_why_terraform_exists.html
  - relationship: this is the pre-intro landscape map before terraform_1000_foot_view
- Link fix applied: childTopics now reference terraform_1000_foot_view.studybubble.json so single-file navigation resolves to terraform_1000_foot_view.html
- Next step: Sean opens the map, adjusts layout, exports layout, syncs layout, rebuilds, then advisor teaches through the landscape
- Known rule: one cluster at a time, 5-10 bubbles preferred, hard max 21
- No engine issue found in this run

- Map 0 update: added back-navigation bubble (back_to_iac_landscape) linking to iac_why_terraform_exists.studybubble.json for return jump to IaC landscape.


- Map 2 created:
  - topic id: terraform_core_workflow
  - topic JSON path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/topics/terraform_core_workflow.studybubble.json
  - image asset path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/assets/terraform_core_workflow.svg
  - generated HTML path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/outputs/terraform_core_workflow.html
  - relationship: this map follows terraform_1000_foot_view and teaches the practical CLI workflow
- Next step: Sean opens the map, adjusts layout, exports layout, syncs layout, rebuilds, then advisor teaches through the workflow
- No engine issue found in this run


- Navigation update: Plan bubble in terraform_1000_foot_view now opens terraform_core_workflow via child topic terraform_core_workflow.studybubble.json.


- Map 6 created:
  - topic id: terraform_state_drift_backends
  - topic JSON path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/topics/terraform_state_drift_backends.studybubble.json
  - image asset path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/assets/terraform_state_drift_backends.svg
  - generated HTML path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/outputs/terraform_state_drift_backends.html
  - relationship: this map follows terraform_core_workflow and teaches the state risk model
- Next step: Sean opens the map, adjusts layout, exports layout, syncs layout, rebuilds, then advisor teaches through the state map
- No engine issue found in this run


- Map 4 created:
  - topic id: terraform_providers_resources
  - topic JSON path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/topics/terraform_providers_resources.studybubble.json
  - image asset path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/assets/terraform_providers_resources.svg
  - generated HTML path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/outputs/terraform_providers_resources.html
  - relationship: this map follows the 1000-foot map and explains the provider / resource model
- Next step: Sean opens the map, adjusts layout, exports layout, syncs layout, rebuilds, then advisor teaches through the provider/resource map
- No engine issue found in this run


- Deep study page update: created tutorials/IaC/TerraForm/study_pages/03_core_workflow/index.html and linked selected Terraform Core Workflow bubbles (Write Configuration, Initialize, Plan, Review Plan, Apply, Outputs) via Open Deep Study Page links.


- Navigation update: Plan bubble in terraform_1000_foot_view now links to Core Workflow deep study page (../../../../tutorials/IaC/TerraForm/study_pages/03_core_workflow/index.html) while preserving child-topic jump to terraform_core_workflow.studybubble.json.


- mapResources retrofit completed for 5 maps (iac_why_terraform_exists, terraform_1000_foot_view, terraform_core_workflow, terraform_state_drift_backends, terraform_providers_resources).
- Build result: all 5 maps built successfully.
- mapResources status: embedded in generated HTML; viewer rendering/interaction should be validated in browser acceptance pass.
- Next planned step: create Core Workflow tutorial/lab package after mapResources are validated.


- Core Workflow tutorial/lab package created:
  - tutorial path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/02_core_workflow/index.html
  - lab README path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/02_core_workflow/README.md
  - topic mapResources updated from planned to active tutorial/lab links
  - Terraform commands run: none (Terraform CLI not executed in this run)
  - next step: browser check tutorial links from mapResources


- State/Drift/Backends tutorial/lab package created:
  - tutorial path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/03_state_drift_backends/index.html
  - lab README path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/03_state_drift_backends/README.md
  - topic mapResources updated from planned to active
  - Terraform commands run: none (Terraform CLI not executed in this run)
  - next step: browser check tutorial links from mapResources


- Providers/Resources tutorial/lab package created:
  - tutorial path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/04_providers_resources/index.html
  - lab README path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/04_providers_resources/README.md
  - topic mapResources updated from planned/missing to active
  - Terraform commands run: none (Terraform CLI not executed in this run)
  - next step: browser check tutorial links from mapResources


- Intro tutorial pages created:
  - IaC tutorial path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/00_iac_why_terraform_exists/index.html
  - Terraform 1000-foot tutorial path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/01_terraform_1000_foot_view/index.html
  - mapResources updated from planned/missing to active tutorial links
  - Terraform commands run: none
  - next step: browser check tutorial links from Map Resources


- LearnTerraform course home page created:
  - course README path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/README.md
  - course index HTML path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/index.html
  - all five maps now link to course home through mapResources
  - Terraform commands run: none
  - next step: browser acceptance check for course home


- Foundation Checkpoint V1 created
- foundation is ready for next new map after user approval
- next map candidate: terraform_variables_outputs_locals


- Map created: terraform_variables_outputs_locals
  - topic JSON path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/topics/terraform_variables_outputs_locals.studybubble.json
  - generated HTML path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/outputs/terraform_variables_outputs_locals.html
  - image asset path: D:/Workarea/StudyBook/study_maps/IaC/TerraForm/assets/terraform_variables_outputs_locals.svg
  - tutorial/lab package status: planned next after browser acceptance


- Variables/Outputs/Locals planned tutorial/lab placeholders created to avoid dead mapResource links.
- Planned Resource Link Rule added to CODEX_CONSTITUTION.md.


- Variables/Outputs/Locals tutorial/lab package completed.
- placeholder replaced with real content.
- tutorial path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/05_variables_outputs_locals/index.html
- lab README path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/05_variables_outputs_locals/README.md
- topic mapResources updated from planned/placeholder to active.
- course index updated from planned to ready.
- Terraform commands run: none (Terraform CLI not executed in this run).
- next step: browser check tutorial/lab links from Map Resources.


- Course index badge/status for Variables, Outputs, and Locals corrected from planned/future styling to ready.


- Map created: terraform_modules_reuse.
- tutorial/lab placeholders exist in 06_modules_reuse to avoid dead mapResource links.


- Course index 'What to Study Next' section updated to remove stale Variables future wording and point to Modules and Reuse.


- Modules and Reuse tutorial/lab package completed.
- placeholder replaced with real content.
- tutorial path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/06_modules_reuse/index.html
- lab README path: D:/Workarea/StudyBook/tutorials/IaC/TerraForm/06_modules_reuse/README.md
- topic mapResources updated from placeholder to active.
- course index updated from under construction to ready.
- Terraform commands run: none (Terraform CLI not executed in this run).
- next step: browser check tutorial/lab links from Map Resources.


- Environments and Workspaces map created (	erraform_environments_workspaces) and tutorial/lab placeholders added under 	utorials/IaC/TerraForm/07_environments_workspaces to avoid dead mapResource links.

- Environments and Workspaces tutorial/lab package completed; placeholder replaced with real content. Tutorial: tutorials/IaC/TerraForm/07_environments_workspaces/index.html; Lab README: tutorials/IaC/TerraForm/07_environments_workspaces/README.md; mapResources active; course index updated to ready; Terraform CLI commands not run; next step: browser check tutorial/lab links from Map Resources.

- Safety, Team Workflow, and CI/CD map created (	erraform_safety_team_workflow_cicd) and tutorial/lab placeholders created under 	utorials/IaC/TerraForm/08_safety_team_workflow_cicd to prevent dead mapResource links.

- Safety, Team Workflow, and CI/CD tutorial/lab package completed; placeholder replaced with real content. Tutorial: tutorials/IaC/TerraForm/08_safety_team_workflow_cicd/index.html; Lab README: tutorials/IaC/TerraForm/08_safety_team_workflow_cicd/README.md; mapResources active; course index updated to ready; Terraform CLI commands not run; next step: browser check tutorial/lab links from Map Resources.

- AWS, Observability, and Interview Bridge map created (	erraform_aws_observability_interview_bridge) and tutorial/lab placeholders added under 	utorials/IaC/TerraForm/09_aws_observability_interview_bridge to avoid dead mapResource links.

- AWS, Observability, and Interview Bridge tutorial/interview package completed; placeholder replaced with real content. Tutorial: tutorials/IaC/TerraForm/09_aws_observability_interview_bridge/index.html; README: tutorials/IaC/TerraForm/09_aws_observability_interview_bridge/README.md; conceptual examples: tutorials/IaC/TerraForm/09_aws_observability_interview_bridge/conceptual_examples; interview files: tutorials/IaC/TerraForm/09_aws_observability_interview_bridge/interview; checklists: tutorials/IaC/TerraForm/09_aws_observability_interview_bridge/checklists; mapResources active; course index ready; no Terraform or AWS commands run; next step: browser check tutorial/README links from Map Resources.

- FOUNDATION_CHECKPOINT_V2.md created.
- first major LearnTerraform course chain checkpointed.
- recommended next work is Interview Q&A consolidation or Terraform Language Basics, not uncontrolled expansion.

- TERRAFORM_INTERVIEW_QA_CONSOLIDATION.md created
- purpose is spoken interview rehearsal from the completed 00-09 course chain
- next recommended step is human review and rehearsal, then possible flashcards

- Interview Q&A Consolidation HTML companion created.
- source Markdown remains in docs.
- HTML page is for browser-based study and rehearsal.
- no Terraform or AWS commands run.

- Terraform Interview Flashcards HTML created
- source material comes from Q&A consolidation
- flashcards are for fast spoken rehearsal
- no Terraform or AWS commands run


- Course home and README cleaned after flashcards acceptance.
- Stale/duplicative wording removed.
- Current course inventory now reflects 00-11 ready items.
- Recommended next work is rehearsal before further expansion.


- Architecture decision recorded: study_maps/IaC/TerraForm is the course/study/deployable front door.
- tutorials/IaC/TerraForm is for runnable labs and hands-on material.
- Added primary front door page: study_maps/IaC/TerraForm/index.html and aligned README messaging.


- course-home mapResources were repaired (course-home links now target ../index.html).
- non-lab study pages moved to study_maps (study_pages and course content).
- Q&A and flashcards moved to study_maps/course.
- tutorials is now lab-only in hub/README and removed non-lab folders.
- generated outputs were rebuilt across all topic maps.

