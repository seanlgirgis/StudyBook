terraform {
  required_version = ">= 1.4.0"
}

module "standard_name" {
  source = "./modules/naming_standard"

  environment      = var.environment
  application_name = var.application_name
  owner            = var.owner
}

resource "terraform_data" "module_demo" {
  input = {
    standard_name = module.standard_name.name_prefix
    tags          = module.standard_name.common_tags
    lesson        = "Modules package reusable Terraform patterns."
  }
}
