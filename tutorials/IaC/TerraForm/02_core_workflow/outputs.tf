output "workflow_message" {
  description = "Small local-safe output for the workflow lab."
  value       = "Hello ${var.learner_name}, this lab teaches Terraform workflow basics."
}

output "study_topic" {
  description = "Shows data carried by the terraform_data resource."
  value       = terraform_data.study_message.output.topic
}
