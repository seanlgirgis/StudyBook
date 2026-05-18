terraform {
  required_version = ">= 1.4.0"
}

resource "terraform_data" "study_message" {
  input = {
    topic   = "Terraform Core Workflow"
    purpose = "Learn init, fmt, validate, and plan safely"
  }
}
