# Rollback Notes

- Terraform rollback is not always a simple `git revert`.
- Infrastructure changes can have side effects.
- Rollback may require code revert plus another controlled Terraform run.
- Some incidents require partial or manual recovery steps.
- Data-related changes are especially sensitive.
- Test rollback approach in lower environments when possible.
