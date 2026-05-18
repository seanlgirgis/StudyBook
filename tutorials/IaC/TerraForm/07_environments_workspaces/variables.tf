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

variable "size" {
  description = "Example environment-specific sizing value."
  type        = string
  default     = "small"
}

variable "retention_days" {
  description = "Example environment-specific retention setting."
  type        = number
  default     = 7
}

variable "approval_required" {
  description = "Whether this environment should require human approval."
  type        = bool
  default     = false
}
