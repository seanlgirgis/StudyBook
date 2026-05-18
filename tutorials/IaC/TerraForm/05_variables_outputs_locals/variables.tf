variable "environment" {
  description = "Environment name such as dev, test, or prod."
  type        = string
  default     = "dev"
}

variable "application_name" {
  description = "Application or learning workload name."
  type        = string
  default     = "learnterraform"
}

variable "owner" {
  description = "Owner or learner name for tagging examples."
  type        = string
  default     = "Sean"
}

variable "enable_extra_message" {
  description = "Boolean example showing feature-style input."
  type        = bool
  default     = true
}

variable "allowed_regions" {
  description = "Example list variable for teaching input types."
  type        = list(string)
  default     = ["us-east-1", "us-east-2"]
}

variable "demo_settings" {
  description = "Example object variable for grouped settings."
  type = object({
    size      = string
    retention = number
  })
  default = {
    size      = "small"
    retention = 7
  }
}

variable "example_sensitive_token" {
  description = "Example sensitive variable. Do not put real secrets here."
  type        = string
  default     = "do-not-use-real-secrets"
  sensitive   = true
}
