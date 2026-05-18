# Prompt: Create Core Workflow Lab (Local-Safe)

Create a Terraform lab under:

D:\Workarea\StudyBook\tutorials\IaC\TerraForm\02_core_workflow

Requirements:
- Do not invent cloud credentials.
- Do not use AWS resources in the default path.
- Do not run terraform apply.
- Create exactly these files:
  - README.md
  - index.html
  - main.tf
  - variables.tf
  - outputs.tf
  - expected_output\terraform_version.txt
  - expected_output\terraform_fmt.txt
  - expected_output\terraform_validate.txt
  - expected_output\terraform_plan_notes.txt
  - troubleshooting.md
  - prompts\create_lab.md
  - prompts\recreate_tutorial.md
- Use a local-safe `terraform_data` example and require Terraform >= 1.4.0.
- If Terraform CLI is installed, run only:
  - terraform version
  - terraform fmt
  - terraform validate
  - terraform plan
- Report command results clearly.
