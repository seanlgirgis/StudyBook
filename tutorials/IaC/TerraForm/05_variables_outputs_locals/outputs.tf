output "name_prefix" {
  description = "Shows how variables and locals combine into a reusable name."
  value       = local.name_prefix
}

output "common_tags" {
  description = "Shows a local map built from input variables."
  value       = local.common_tags
}

output "workflow_message" {
  description = "Shows a reusable local expression."
  value       = local.workflow_message
}

output "demo_resource_output" {
  description = "Shows data flowing through a local-safe terraform_data resource."
  value       = terraform_data.variables_demo.output
}

output "sensitive_token_example" {
  description = "Demonstrates a sensitive output without using a real secret."
  value       = var.example_sensitive_token
  sensitive   = true
}
