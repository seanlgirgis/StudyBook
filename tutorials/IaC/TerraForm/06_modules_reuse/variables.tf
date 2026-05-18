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
