terraform {
  required_version = ">= 1.4.0"
}

locals {
  name_prefix = "${var.environment}-${var.application_name}"

  common_tags = {
    environment = var.environment
    application = var.application_name
    owner       = var.owner
    managed_by  = "terraform"
  }

  environment_summary = {
    environment     = var.environment
    size            = var.size
    retention_days  = var.retention_days
    approval_needed = var.approval_required
  }
}

resource "terraform_data" "environment_demo" {
  input = {
    name_prefix = local.name_prefix
    tags        = local.common_tags
    summary     = local.environment_summary
    lesson      = "Same Terraform pattern, different environment inputs."
  }
}
