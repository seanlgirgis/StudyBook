# Backend Notes

A backend controls where Terraform stores state.

- Local state is default and simple for learning.
- Teams prefer remote state for collaboration and controls.
- Locking prevents concurrent state writes.
- Backend is not provider: backend stores state, provider manages resources.

Explanatory only (do not run without approved real setup):

`hcl
terraform {
  backend "s3" {
    bucket = "example-terraform-state-bucket"
    key    = "learnterraform/state-demo.tfstate"
    region = "us-east-1"
  }
}
`

This is only an explanatory example. Do not run this unless bucket, permissions, encryption, and locking strategy are approved.
