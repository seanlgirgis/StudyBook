output "name_prefix" {
  description = "Standardized name prefix produced by the child module."
  value       = local.name_prefix
}

output "common_tags" {
  description = "Standardized tag map produced by the child module."
  value       = local.common_tags
}
