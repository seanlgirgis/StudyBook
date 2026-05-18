# CONCEPTUAL ONLY. Not meant to run.

resource "aws_cloudwatch_log_group" "app_logs" {
  name              = "/example/learning/app"
  retention_in_days = 14
}

# Conceptual alarm/dashboard wiring should be reviewed for signal quality,
# ownership, and notification routes before real use.
