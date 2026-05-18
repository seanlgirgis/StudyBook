# IaC: Why Terraform Exists

## Purpose
Explain the pre-Terraform landscape and why Infrastructure as Code became necessary.

## What This Tutorial Teaches
- before IaC
- manual console work limits
- scripts and tribal knowledge limits
- cloud growth problem
- IaC as the workflow shift
- Terraform and alternatives (CloudFormation, Ansible, Pulumi, OpenTofu)

## Suggested Study Path
Before IaC -> Manual Console -> Scripts/Tribal Knowledge -> Cloud Growth -> IaC -> Terraform -> Alternatives

## Key Ideas
- scale and repeatability drove IaC adoption
- reviewability and version control changed infrastructure operations
- Terraform is one major option, not the only option

## Quick Comparison Table
| Tool | Strength | Typical Fit |
|---|---|---|
| Terraform | Broad multi-platform workflow | Cross-platform IaC teams |
| CloudFormation | Deep AWS-native integration | AWS-focused teams |
| Ansible | Automation/configuration strength | Ops/config + orchestration |
| Pulumi | General programming languages | Teams preferring language-native IaC |
| OpenTofu | Terraform-compatible open governance | Teams emphasizing OSS governance |

## Safe Interview Answer
IaC became necessary because manual and loosely scripted infrastructure struggled to scale, review, and repeat safely. Terraform became popular by offering a consistent desired-state workflow across platforms while alternatives remain valid based on team context.

## Common Traps
- saying console work is always bad
- saying Terraform is the only serious option
- confusing automation tooling with declarative provisioning goals

## Links Back To Maps
- ../../../../study_maps/IaC/TerraForm/outputs/iac_why_terraform_exists.html
- ../../../../study_maps/IaC/TerraForm/outputs/terraform_1000_foot_view.html

## No Lab Required
This orientation tutorial is conceptual. No runnable Terraform lab is required for this map.
