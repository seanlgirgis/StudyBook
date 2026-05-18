terraform {
  required_version = ">= 1.4.0"
}

variable "environment" {
  description = "Learning environment name."
  type        = string
  default     = "learning"
}

resource "terraform_data" "state_demo" {
  input = {
    environment = var.environment
    lesson      = "state maps Terraform configuration to managed objects"
  }
}

output "state_lesson" {
  description = "Explains the state concept without creating cloud resources."
  value       = terraform_data.state_demo.output.lesson
}

output "environment" {
  description = "Shows the selected learning environment."
  value       = var.environment
}
