terraform {
  required_version = ">= 1.4.0"
}

locals {
  change_summary = {
    change_type       = var.change_type
    environment       = var.environment
    requested_by      = var.requested_by
    approval_required = var.approval_required
    blast_radius      = var.blast_radius
  }

  safety_message = "Review ${var.change_type} change for ${var.environment} before any apply."
}

resource "terraform_data" "safety_review_demo" {
  input = {
    change_summary = local.change_summary
    safety_message = local.safety_message
    lesson         = "Terraform safety is about review, plan visibility, controlled apply, and protected state."
  }
}
