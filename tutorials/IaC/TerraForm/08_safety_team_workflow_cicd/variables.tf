variable "environment" {
  description = "Environment being reviewed, such as dev, test, stage, or prod."
  type        = string
  default     = "dev"
}

variable "change_type" {
  description = "Type of Terraform change being reviewed."
  type        = string
  default     = "learning-change"
}

variable "requested_by" {
  description = "Person or team requesting the change."
  type        = string
  default     = "Sean"
}

variable "approval_required" {
  description = "Whether this change should require human approval."
  type        = bool
  default     = true
}

variable "blast_radius" {
  description = "Plain-English impact category for the proposed change."
  type        = string
  default     = "low"
}
