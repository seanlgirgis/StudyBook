# Terraform Interview Q&A Consolidation

## Purpose
This document turns the completed LearnTerraform course chain into spoken, interview-safe answers Sean can rehearse.

## Sean-Safe Positioning Rules
Sean can safely say:
- I understand the Terraform workflow.
- I understand infrastructure-as-code concepts.
- I understand providers, resources, plan/apply, state, drift, variables, outputs, modules, environments, and team safety.
- I understand how Terraform connects to AWS, observability, data engineering, and capacity planning conversations.
- My strongest production background is data engineering, telemetry, monitoring, capacity forecasting, operational reporting, and production support thinking.
- I am building Terraform fluency to collaborate better with cloud/platform teams.

Sean should not say:
- I owned enterprise Terraform platforms in production.
- I was the primary Terraform platform engineer.
- I managed all AWS infrastructure using Terraform.
- I built production Terraform CI/CD governance from scratch.
- I deeply owned Kubernetes/Terraform/OpenTelemetry production platforms unless specifically true elsewhere.

Recovery line:

"To be precise, I would not position myself as the primary Terraform platform owner. My strength is understanding the workflow and how it connects to data, monitoring, capacity, and cloud operations."

## Master 30-Second Terraform Story
Terraform is infrastructure as code: teams define desired infrastructure in versioned files, review the plan, and apply controlled changes with protected state. The safety core is plan review, state discipline, and controlled apply paths. My strongest background is data engineering, telemetry, monitoring, and capacity forecasting, so Terraform helps me connect infrastructure definition to operational behavior. I use that fluency to collaborate better with platform and cloud teams.

## Master 2-Minute Terraform Story
I frame Terraform as a repeatable infrastructure workflow, not just commands. Teams define desired infrastructure in code, run init/fmt/validate, review plans, and apply changes through controlled approval paths. State is critical because it links code to real resources, so remote state and locking matter in team environments. Drift, environment separation, and wrong-target risk are real, so workflows need PR review, blast-radius checks, least privilege, and CI/CD guardrails.

For my background, the key bridge is operational: Terraform defines the infrastructure pattern, observability shows runtime behavior, and capacity planning evaluates headroom and trend risk. I do not present myself as the primary Terraform platform owner, but I can discuss the workflow clearly, evaluate change risk, and collaborate effectively with platform, cloud, and DevOps teams.

## Q&A Sections
### 1) What is Terraform?
- Short answer: IaC tool for defining and managing infrastructure as code.
- Stronger answer: Terraform compares desired config to current state and proposes changes via plan before controlled apply.
- Safe sentence to memorize: Terraform turns infrastructure changes into reviewable code workflows.
- Common trap / avoid saying: “It is just a script runner.”
- Map reference: 01 Terraform 1000-Foot View

### 2) What problem does Terraform solve?
- Short answer: Reduces manual, inconsistent cloud changes.
- Stronger answer: Gives repeatability, auditability, and safer change review across environments.
- Safe sentence to memorize: Terraform solves repeatability and change-control problems.
- Common trap / avoid saying: “Terraform removes all risk.”
- Map reference: 00 IaC Why Terraform Exists

### 3) What is Infrastructure as Code?
- Short answer: Managing infrastructure definitions through code.
- Stronger answer: IaC brings version control, review, and reproducible change discipline to infrastructure.
- Safe sentence to memorize: IaC is infrastructure with software engineering discipline.
- Common trap / avoid saying: “IaC means no human review.”
- Map reference: 00 IaC Why Terraform Exists

### 4) What is the Terraform workflow?
- Short answer: Write config, init/fmt/validate, plan/review, controlled apply.
- Stronger answer: Mature workflows add approvals, state protection, and environment checks.
- Safe sentence to memorize: Terraform workflow is config plus safety checkpoints.
- Common trap / avoid saying: “I just run apply.”
- Map reference: 02 Terraform Core Workflow

### 5) What is terraform init?
- Short answer: Prepares the working directory.
- Stronger answer: Downloads/providers/modules metadata and initializes execution context.
- Safe sentence to memorize: init prepares consistent execution context.
- Common trap / avoid saying: “init validates production safety.”
- Map reference: 02 Terraform Core Workflow

### 6) What is terraform fmt?
- Short answer: Formats Terraform files.
- Stronger answer: Reduces style noise and improves readability in code review.
- Safe sentence to memorize: fmt is hygiene, not risk approval.
- Common trap / avoid saying: “fmt means change is safe.”
- Map reference: 02 Terraform Core Workflow

### 7) What is terraform validate?
- Short answer: Checks config syntax and structure.
- Stronger answer: Catches basic config errors but does not validate business impact.
- Safe sentence to memorize: validate checks config health, not blast radius.
- Common trap / avoid saying: “validate replaces plan review.”
- Map reference: 02 Terraform Core Workflow

### 8) What is terraform plan?
- Short answer: Preview of proposed infra changes.
- Stronger answer: Shows create/change/destroy actions before execution and supports review.
- Safe sentence to memorize: plan is the safety preview.
- Common trap / avoid saying: “plan is optional noise.”
- Map reference: 02 Terraform Core Workflow

### 9) Why is plan review important?
- Short answer: Confirms intended impact before apply.
- Stronger answer: Catches unexpected replacement, destruction, or wrong-environment context.
- Safe sentence to memorize: plan review is the key pre-apply checkpoint.
- Common trap / avoid saying: “small diff means low risk.”
- Map reference: 08 Safety, Team Workflow, and CI/CD

### 10) What is terraform apply?
- Short answer: Executes approved infrastructure changes.
- Stronger answer: Apply changes real systems and should follow controlled workflow gates.
- Safe sentence to memorize: apply is execution and must be controlled.
- Common trap / avoid saying: “Anyone can apply to production.”
- Map reference: 02 Terraform Core Workflow

### 11) Why should apply be controlled?
- Short answer: To prevent unsafe or unauthorized infra changes.
- Stronger answer: Controlled apply reduces wrong-target and high-impact production mistakes.
- Safe sentence to memorize: controlled apply is core operational safety.
- Common trap / avoid saying: “Direct laptop apply to prod is normal.”
- Map reference: 08 Safety, Team Workflow, and CI/CD

### 12) What is Terraform state?
- Short answer: Terraform’s record of managed resources.
- Stronger answer: State links config intent to real objects and powers accurate planning.
- Safe sentence to memorize: state is Terraform’s memory.
- Common trap / avoid saying: “state is optional.”
- Map reference: 03 State, Drift, and Backends

### 13) Why is state important?
- Short answer: Enables accurate reconciliation.
- Stronger answer: Without trusted state, Terraform cannot safely calculate changes.
- Safe sentence to memorize: reliable state is required for reliable plans.
- Common trap / avoid saying: “code alone is enough.”
- Map reference: 03 State, Drift, and Backends

### 14) Why is state risky?
- Short answer: It can contain sensitive and high-impact data.
- Stronger answer: Badly protected state can create security and change-integrity problems.
- Safe sentence to memorize: state needs strong protection and access control.
- Common trap / avoid saying: “sensitive=true removes all risk.”
- Map reference: 03 State, Drift, and Backends

### 15) What is drift?
- Short answer: Real infra differs from Terraform expectation.
- Stronger answer: Drift usually comes from out-of-band changes and appears in plan behavior.
- Safe sentence to memorize: drift is configuration-vs-reality mismatch.
- Common trap / avoid saying: “drift cannot happen.”
- Map reference: 03 State, Drift, and Backends

### 16) What is a backend?
- Short answer: Where/how Terraform state is stored.
- Stronger answer: Backend strategy controls collaboration and state safety.
- Safe sentence to memorize: backend is state storage strategy.
- Common trap / avoid saying: “backend equals provider.”
- Map reference: 03 State, Drift, and Backends

### 17) What is remote state?
- Short answer: Shared centralized state location.
- Stronger answer: Teams use remote state so everyone references one trusted state source.
- Safe sentence to memorize: remote state supports team consistency.
- Common trap / avoid saying: “local state is enough for all team work.”
- Map reference: 03 State, Drift, and Backends

### 18) What is state locking?
- Short answer: Prevents concurrent state writes.
- Stronger answer: Locking avoids conflicting applies and state corruption.
- Safe sentence to memorize: locking protects state integrity.
- Common trap / avoid saying: “ignore locks to move faster.”
- Map reference: 03 State, Drift, and Backends

### 19) What is a provider?
- Short answer: Terraform integration to a platform/API.
- Stronger answer: Providers translate Terraform resource intent into platform operations.
- Safe sentence to memorize: providers connect Terraform to external systems.
- Common trap / avoid saying: “Terraform knows every platform natively.”
- Map reference: 04 Providers and Resources

### 20) What is a resource?
- Short answer: Managed infrastructure object.
- Stronger answer: Resources define what Terraform creates/updates/tracks.
- Safe sentence to memorize: resources are the things Terraform manages.
- Common trap / avoid saying: “resources only mean VMs.”
- Map reference: 04 Providers and Resources

### 21) Difference between provider and resource?
- Short answer: Provider connects; resource defines object intent.
- Stronger answer: Provider is the API bridge, resource is the managed declaration.
- Safe sentence to memorize: integration layer vs managed object.
- Common trap / avoid saying: “they are the same concept.”
- Map reference: 04 Providers and Resources

### 22) What are variables?
- Short answer: Input values for Terraform.
- Stronger answer: Variables separate reusable logic from environment-specific values.
- Safe sentence to memorize: variables make one pattern reusable.
- Common trap / avoid saying: “hardcode everything.”
- Map reference: 05 Variables, Outputs, and Locals

### 23) What are locals?
- Short answer: Internal computed values.
- Stronger answer: Locals reduce repetition and standardize internal expressions.
- Safe sentence to memorize: locals organize reusable internal logic.
- Common trap / avoid saying: “locals are external inputs.”
- Map reference: 05 Variables, Outputs, and Locals

### 24) What are outputs?
- Short answer: Exposed values from Terraform config/state.
- Stronger answer: Outputs help humans/tools consume important result values.
- Safe sentence to memorize: outputs publish useful results.
- Common trap / avoid saying: “expose secrets casually.”
- Map reference: 05 Variables, Outputs, and Locals

### 25) What are tfvars files?
- Short answer: Files supplying variable values.
- Stronger answer: They support per-environment inputs without rewriting shared config.
- Safe sentence to memorize: tfvars separate values from reusable code.
- Common trap / avoid saying: “commit secrets in tfvars.”
- Map reference: 05 Variables, Outputs, and Locals
### 26) What are modules?
- Short answer: Reusable Terraform configuration packages.
- Stronger answer: Modules package repeated patterns and help enforce standards.
- Safe sentence to memorize: modules reduce copy/paste and improve consistency.
- Common trap / avoid saying: “modules automatically equal quality.”
- Map reference: 06 Modules and Reuse

### 27) What is a root module?
- Short answer: The configuration where Terraform runs.
- Stronger answer: Root module is execution entry point that may call child modules.
- Safe sentence to memorize: root module is the active run context.
- Common trap / avoid saying: “root means enterprise shared module.”
- Map reference: 06 Modules and Reuse

### 28) What is a child module?
- Short answer: A module called by another module.
- Stronger answer: Child modules take inputs and return outputs to callers.
- Safe sentence to memorize: child modules are reusable called components.
- Common trap / avoid saying: “hide everything in complex child modules.”
- Map reference: 06 Modules and Reuse

### 29) Why do teams use modules?
- Short answer: Reuse and standardization.
- Stronger answer: Teams encode common patterns once and apply consistently.
- Safe sentence to memorize: modules scale repeatable infrastructure patterns.
- Common trap / avoid saying: “modularize everything too early.”
- Map reference: 06 Modules and Reuse

### 30) What are module risks?
- Short answer: Bad modules spread bad patterns widely.
- Stronger answer: Risks include unclear inputs/outputs, hidden side effects, weak version control.
- Safe sentence to memorize: module reuse amplifies both good and bad design.
- Common trap / avoid saying: “modules are safe black boxes.”
- Map reference: 06 Modules and Reuse

### 31) How do teams separate dev, test, and prod?
- Short answer: Explicit boundaries in inputs, state, and approvals.
- Stronger answer: Use folder strategy, tfvars separation, backend boundaries, and stronger prod controls.
- Safe sentence to memorize: environment separation is safety design.
- Common trap / avoid saying: “different names alone are enough.”
- Map reference: 07 Environments and Workspaces

### 32) What are Terraform workspaces?
- Short answer: Named state instances for same config.
- Stronger answer: Useful for separation but requires strict context awareness.
- Safe sentence to memorize: workspaces separate state, not all risk.
- Common trap / avoid saying: “workspace alone secures production.”
- Map reference: 07 Environments and Workspaces

### 33) Why can workspaces be risky?
- Short answer: Wrong active workspace can target wrong state.
- Stronger answer: Unclear workspace context can lead to unintended plans/applies.
- Safe sentence to memorize: always verify active workspace before change operations.
- Common trap / avoid saying: “workspace selection mistakes are minor.”
- Map reference: 07 Environments and Workspaces

### 34) What is backend-per-environment?
- Short answer: Separate state location/path per environment.
- Stronger answer: Helps prevent state mixing and reduces wrong-target impact.
- Safe sentence to memorize: backend boundaries should match environment boundaries.
- Common trap / avoid saying: “shared dev/prod state is fine.”
- Map reference: 07 Environments and Workspaces

### 35) What is wrong-environment risk?
- Short answer: Running changes in unintended environment/account/state.
- Stronger answer: High-impact risk mitigated by explicit pre-apply context checks.
- Safe sentence to memorize: wrong-target execution is a top Terraform hazard.
- Common trap / avoid saying: “CLI context is probably right.”
- Map reference: 07 Environments and Workspaces

### 36) How do teams use Terraform safely?
- Short answer: PRs, plans, approvals, protected state, least privilege.
- Stronger answer: Safety is workflow discipline with automation and human review gates.
- Safe sentence to memorize: Terraform safety is process plus controls.
- Common trap / avoid saying: “validate passing is enough.”
- Map reference: 08 Safety, Team Workflow, and CI/CD

### 37) How does Terraform fit into CI/CD?
- Short answer: CI/CD standardizes checks and review evidence.
- Stronger answer: Pipelines run fmt/validate/plan, publish artifacts, and gate apply.
- Safe sentence to memorize: CI/CD makes Terraform review repeatable.
- Common trap / avoid saying: “auto-apply everywhere is best practice.”
- Map reference: 08 Safety, Team Workflow, and CI/CD

### 38) What role do pull requests play in Terraform?
- Short answer: Code and impact review gate.
- Stronger answer: PRs improve traceability, peer review, and intent clarity before execution.
- Safe sentence to memorize: PRs turn infra changes into shared team decisions.
- Common trap / avoid saying: “PR review is optional ceremony.”
- Map reference: 08 Safety, Team Workflow, and CI/CD

### 39) What is blast radius?
- Short answer: Potential scope of impact from a change.
- Stronger answer: Assesses resource/business impact before approval.
- Safe sentence to memorize: blast radius review is operational risk discipline.
- Common trap / avoid saying: “line count equals impact.”
- Map reference: 08 Safety, Team Workflow, and CI/CD

### 40) What are policy checks?
- Short answer: Automated rule enforcement before apply.
- Stronger answer: Enforces security/compliance guardrails consistently in workflow.
- Safe sentence to memorize: policy checks are scalable guardrails.
- Common trap / avoid saying: “manual memory is enough for policy compliance.”
- Map reference: 08 Safety, Team Workflow, and CI/CD

### 41) What is least privilege in Terraform automation?
- Short answer: Grant minimum required permissions.
- Stronger answer: Limits blast radius and credential misuse risk.
- Safe sentence to memorize: least privilege limits potential damage.
- Common trap / avoid saying: “admin credentials by default are fine.”
- Map reference: 08 Safety, Team Workflow, and CI/CD

### 42) How does Terraform relate to AWS?
- Short answer: Terraform can define/review AWS infra as code.
- Stronger answer: Adds repeatability and safer change workflow for AWS foundations.
- Safe sentence to memorize: Terraform adds discipline to AWS infrastructure changes.
- Common trap / avoid saying: “I owned all AWS Terraform production work.”
- Map reference: 09 AWS, Observability, and Interview Bridge

### 43) What AWS resources might Terraform manage?
- Short answer: Storage, IAM, networking, compute, and monitoring assets.
- Stronger answer: Common examples are S3, IAM roles/policies, VPC/network controls, compute support, CloudWatch primitives.
- Safe sentence to memorize: Terraform often manages foundational AWS components.
- Common trap / avoid saying: “everything in AWS is always Terraform-managed.”
- Map reference: 09 AWS, Observability, and Interview Bridge

### 44) How does Terraform relate to observability?
- Short answer: It can version observability config components.
- Stronger answer: Dashboards/alerts/integrations can be managed with reviewable IaC patterns where supported.
- Safe sentence to memorize: Terraform can improve observability config consistency.
- Common trap / avoid saying: “IaC alone guarantees good observability.”
- Map reference: 09 AWS, Observability, and Interview Bridge

### 45) How can dashboards or alerts be managed as code?
- Short answer: Version and review definitions in source control.
- Stronger answer: Improves ownership, consistency, and rollback clarity while reducing manual drift.
- Safe sentence to memorize: dashboards and alerts as code improve repeatability.
- Common trap / avoid saying: “coded dashboards are automatically useful.”
- Map reference: 09 AWS, Observability, and Interview Bridge

### 46) How does Terraform relate to data engineering?
- Short answer: Data workflows depend on cloud infrastructure Terraform conversations define.
- Stronger answer: Storage, IAM, compute, network, and monitoring dependencies make Terraform fluency valuable for collaboration.
- Safe sentence to memorize: Terraform supports infrastructure around data pipelines.
- Common trap / avoid saying: “Terraform replaces data pipeline engineering.”
- Map reference: 09 AWS, Observability, and Interview Bridge

### 47) How does Terraform relate to capacity planning?
- Short answer: Terraform defines capacity shape; telemetry validates adequacy.
- Stronger answer: Capacity planning uses utilization trends and thresholds to inform infrastructure changes.
- Safe sentence to memorize: provisioning intent must connect to capacity behavior.
- Common trap / avoid saying: “provisioning equals forecasting.”
- Map reference: 09 AWS, Observability, and Interview Bridge

### 48) What is your real Terraform experience?
- Short answer: Structured practical fluency plus operational collaboration strength.
- Stronger answer: Strongest production background is data/monitoring/capacity; Terraform fluency supports safer cloud/platform collaboration.
- Safe sentence to memorize: my Terraform positioning is fluent collaboration, not overclaimed ownership.
- Common trap / avoid saying: “I was primary enterprise Terraform owner.”
- Map reference: 09 AWS, Observability, and Interview Bridge

### 49) How would you collaborate with DevOps/platform teams on Terraform?
- Short answer: Align workflow, risk gates, and observability outcomes.
- Stronger answer: Contribute strong plan-review, operational, and capacity-impact context while respecting platform ownership.
- Safe sentence to memorize: I add operational clarity to Terraform team workflows.
- Common trap / avoid saying: “I would independently own production apply.”
- Map reference: 08 Safety + 09 Bridge

### 50) How do you avoid overclaiming Terraform?
- Short answer: Separate direct ownership from collaborative fluency.
- Stronger answer: Use precise language on scope, strengths, and role boundaries.
- Safe sentence to memorize: precision builds technical credibility.
- Common trap / avoid saying: “I built everything end-to-end” when not true.
- Map reference: 09 AWS, Observability, and Interview Bridge

## Special Section: Questions That Could Trap Sean
1. Have you owned Terraform in production?
- Risk: Overstating ownership.
- Safe answer: I have strong workflow fluency and production-adjacent collaboration, but I would not position myself as primary Terraform platform owner.
- Strong pivot: I bring deep strengths in telemetry, monitoring, capacity, and operational risk framing.

2. Did you build Terraform modules for AWS?
- Risk: Claiming direct build ownership.
- Safe answer: I understand module patterns and risks, and collaborate with platform teams on implementation outcomes.
- Strong pivot: I focus on observability and capacity impact of module-level changes.

3. Did you design remote state and locking?
- Risk: Claiming architecture ownership.
- Safe answer: I understand why remote state and locking are core controls; I do not overstate ownership boundaries.
- Strong pivot: I can identify operational risk when state controls are weak.

4. Have you run Terraform apply in production?
- Risk: Fabricating execution history.
- Safe answer: I understand controlled-apply workflow and approvals; I do not overclaim unmanaged production apply ownership.
- Strong pivot: I contribute strongly to plan review, blast-radius checks, and post-change telemetry verification.

5. Are you a Terraform expert?
- Risk: Inflated self-label.
- Safe answer: I describe myself as practically fluent and safety-aware, with strongest expertise in data/monitoring/capacity domains.
- Strong pivot: I combine Terraform understanding with strong operational decision support.

6. How much Terraform experience do you have?
- Risk: Ambiguous overstatement.
- Safe answer: I have built structured fluency across workflow, state, modules, environments, and team safety patterns.
- Strong pivot: I contribute quickly in collaboration-heavy cloud/platform contexts.

7. Can you troubleshoot Terraform state problems?
- Risk: Claiming deep incident ownership.
- Safe answer: I understand core state risk patterns and safe troubleshooting approaches; I am careful about scope.
- Strong pivot: I am strong at structured incident reasoning and operational communication.

8. Can you build Terraform CI/CD pipelines?
- Risk: Claiming governance ownership.
- Safe answer: I understand secure CI/CD workflow shape and controls; I collaborate with platform teams on production implementations.
- Strong pivot: I add value on review gates, risk criteria, and observability expectations.

9. Have you used Terraform with Kubernetes?
- Risk: Inventing adjacent ownership.
- Safe answer: I answer only to direct experience and otherwise discuss transferable Terraform safety concepts.
- Strong pivot: My strongest edge is workflow discipline and operations insight.

10. Can you manage AWS infrastructure with Terraform?
- Risk: Overpromising ownership.
- Safe answer: I can participate effectively in Terraform-based AWS reviews and collaboration, while being explicit about ownership scope.
- Strong pivot: I am strongest in linking infra changes to telemetry, capacity, and operational risk.
## Special Section: Sean's Best Pivots
- Terraform -> capacity forecasting: IaC defines shape; capacity forecasting tests headroom.
- Terraform -> observability: Infra changes should include signal and alert-quality expectations.
- Terraform -> monitoring: Plan review is pre-change evidence; monitoring confirms post-change behavior.
- Terraform -> data engineering: Pipelines rely on infra layers Terraform conversations shape.
- Terraform -> production support: Safe change control is review + verification, not just execution.
- Terraform -> management reporting: Telemetry plus infra context improves decision quality.
- Terraform -> safe change control: PR + plan + approvals + state protection.
- Terraform -> AWS collaboration: Operational context plus Terraform fluency strengthens cross-team work.

## Special Section: One-Liners to Memorize
1. Terraform plan is the safety preview before infrastructure changes.
2. State is Terraform's memory, so teams protect it carefully.
3. Drift means the real environment changed outside Terraform.
4. Providers connect Terraform to platform APIs.
5. Resources are the objects Terraform manages.
6. validate checks structure, not operational impact.
7. Apply should be controlled in shared and production environments.
8. Remote state and locking protect team workflows.
9. Variables make one Terraform pattern reusable.
10. tfvars separate environment values from shared config.
11. Locals reduce repetition and improve readability.
12. Outputs expose useful values for humans and automation.
13. Modules package reusable patterns but need discipline.
14. Environment boundaries should match state boundaries.
15. Wrong-environment execution is a top Terraform risk.
16. CI/CD should publish plan evidence and gate apply.
17. Policy checks scale guardrails.
18. Least privilege limits automation blast radius.
19. Terraform can help version observability assets.
20. My Terraform positioning is fluency and collaboration, not overclaimed ownership.

## Special Section: 5-Minute Oral Rehearsal Script
Terraform is infrastructure as code, which means infrastructure changes become versioned, reviewable, and repeatable instead of ad-hoc console edits. The core flow is write configuration, initialize, format and validate, generate a plan, review impact, and then apply changes through controlled workflow.

State is central because it links Terraform config to real managed objects. In teams, remote state and locking are important controls to avoid collisions and confusion. Drift can appear when changes happen outside Terraform, so plan review and environment checks matter.

Providers and resources are the model basics: providers connect Terraform to APIs, and resources describe what should exist. Variables, locals, outputs, and tfvars enable reuse; modules package repeated patterns; environments and workspace strategy reduce wrong-target risk.

For team safety, mature workflows use pull requests, CI/CD checks, plan evidence, policy checks, least privilege, and controlled apply gates. Blast-radius review helps teams evaluate impact before approving changes.

For my background, this connects directly to data engineering and operations. I bring strong experience in telemetry, monitoring, capacity forecasting, and operational reporting. Terraform helps me collaborate with cloud/platform teams by connecting infrastructure intent to runtime behavior and risk. I do not position myself as the primary Terraform platform owner, but I can contribute effectively to safer cloud change processes.

## Special Section: Quick Self-Test
1. What is Terraform in one sentence?
2. Why is IaC better than manual console workflows?
3. Why is plan review essential?
4. What does state do?
5. Why is state sensitive?
6. What causes drift?
7. Why do teams use remote state?
8. Why does locking matter?
9. Provider vs resource difference?
10. Why use variables?
11. Locals vs variables?
12. Why outputs matter?
13. What tfvars solves?
14. Why modules exist?
15. What module risk is common?
16. How to separate dev/test/prod?
17. What are workspaces?
18. Why can workspaces be risky?
19. What is wrong-environment risk?
20. Why controlled apply?
21. What is blast radius?
22. What policy checks enforce?
23. What least privilege means in automation?
24. How Terraform connects to AWS/observability/data/capacity?
25. What is your safe Terraform positioning line?

## Map Reference Index
- 00 IaC Why Terraform Exists: Why IaC emerged and Terraform's role.
- 01 Terraform 1000-Foot View: Core mental model.
- 02 Terraform Core Workflow: Practical command/review flow.
- 03 State, Drift, and Backends: State risk model.
- 04 Providers and Resources: Platform integration model.
- 05 Variables, Outputs, and Locals: Reuse and input/output patterns.
- 06 Modules and Reuse: Packaging repeatable patterns safely.
- 07 Environments and Workspaces: Environment boundaries and wrong-target risk.
- 08 Safety, Team Workflow, and CI/CD: Team safety workflow and guardrails.
- 09 AWS, Observability, and Interview Bridge: Safe bridge to AWS/ops interview language.

## Recommended Next Step
After this document is created, Sean should rehearse answers before creating another map.

Recommended next artifact after review:
`D:\Workarea\StudyBook\study_maps\IaC\TerraForm\docs\TERRAFORM_INTERVIEW_FLASHCARDS.md`

or

a StudyBubble map only if the Q&A document proves useful.
