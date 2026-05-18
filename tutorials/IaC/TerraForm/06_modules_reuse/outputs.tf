output "standard_name_from_module" {
  description = "Shows an output returned by the child module."
  value       = module.standard_name.name_prefix
}

output "standard_tags_from_module" {
  description = "Shows standardized tags returned by the child module."
  value       = module.standard_name.common_tags
}

output "module_demo_output" {
  description = "Shows local-safe data flowing through the root module."
  value       = terraform_data.module_demo.output
}
