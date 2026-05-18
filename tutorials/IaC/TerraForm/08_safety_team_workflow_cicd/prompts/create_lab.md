Create or recreate this exact local-safe lab under:
D:\Workarea\StudyBook\tutorials\IaC\TerraForm\08_safety_team_workflow_cicd

Guardrails:
- do not invent cloud credentials
- do not use AWS
- do not run terraform apply
- do not create cloud resources
- do not configure a real remote backend
- do not create a live CI/CD pipeline
- create the exact files
- use local-safe terraform_data only
- run version/fmt/validate/plan only if Terraform is installed
- report results
