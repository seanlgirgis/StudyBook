resource "terraform_data" "provider_resource_demo" {
  input = {
    topic   = "providers and resources"
    purpose = "show resource type, resource name, address, and attributes"
  }
}

resource "terraform_data" "dependent_demo" {
  input = {
    upstream_topic = terraform_data.provider_resource_demo.output.topic
    dependency     = "this resource references an attribute from another resource"
  }
}

output "resource_address_example" {
  description = "Example of the Terraform resource address used in this lab."
  value       = "terraform_data.provider_resource_demo"
}

output "dependency_message" {
  description = "Shows a value passed through a Terraform reference."
  value       = terraform_data.dependent_demo.output.dependency
}
