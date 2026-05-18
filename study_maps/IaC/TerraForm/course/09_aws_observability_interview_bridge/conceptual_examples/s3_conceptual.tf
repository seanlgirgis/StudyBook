# CONCEPTUAL ONLY.
# Do not run without approved AWS credentials, naming, security,
# cost review, backend/state plan, and cleanup plan.

resource "aws_s3_bucket" "learning_logs" {
  bucket = "example-company-learning-logs-bucket"

  tags = {
    environment = "conceptual"
    owner       = "platform-team"
    purpose     = "learning"
  }
}

# Conceptual: encryption and lifecycle should be reviewed in real use.
