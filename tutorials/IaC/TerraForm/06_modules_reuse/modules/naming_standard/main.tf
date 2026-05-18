locals {
  name_prefix = "${var.environment}-${var.application_name}"

  common_tags = {
    environment = var.environment
    application = var.application_name
    owner       = var.owner
    managed_by  = "terraform"
    pattern     = "module-demo"
  }
}
