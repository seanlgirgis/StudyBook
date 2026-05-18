# CONCEPTUAL ONLY. IAM is high risk.
# Do not run without security review and approval.
# Do not copy/paste broad permissions.

resource "aws_iam_role" "conceptual_pipeline_role" {
  name = "example-learning-pipeline-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "ec2.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

# BAD EXAMPLE (do not use): Action="*", Resource="*"
# Prefer least-privilege policies with explicit actions/resources.
