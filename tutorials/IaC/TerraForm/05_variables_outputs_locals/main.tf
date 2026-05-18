terraform {
  required_version = ">= 1.4.0"
}

locals {
  name_prefix = "-"

  common_tags = {
    environment = var.environment
    application = var.application_name
    owner       = var.owner
    managed_by  = "terraform"
  }

  workflow_message = "Planning  for "
}

resource "terraform_data" "variables_demo" {
  input = {
    name_prefix = local.name_prefix
    tags        = local.common_tags
    message     = local.workflow_message
  }
}
