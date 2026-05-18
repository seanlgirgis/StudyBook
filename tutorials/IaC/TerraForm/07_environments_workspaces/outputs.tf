output "name_prefix" {
  description = "Shows how the environment changes the naming pattern."
  value       = local.name_prefix
}

output "environment_summary" {
  description = "Shows the selected environment-specific values."
  value       = local.environment_summary
}

output "environment_demo_output" {
  description = "Shows local-safe data flowing through the environment demo."
  value       = terraform_data.environment_demo.output
}
