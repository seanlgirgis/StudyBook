# Manuals & Guides

Welcome to the **Manuals** directory. This folder acts as the primary knowledge base for the StudyBook repository. It contains high-level, human-readable guides that explain how to use the systems, tools, and environments configured in this project.

## Purpose

While the `operations/` and `adr/` folders contain technical workflows, scripts, and architectural decisions, the `manuals/` folder is designed for **you**. These documents are intended to be accessible, step-by-step articles that help you (or any AI agent) quickly understand and interact with the local environment.

## Current Contents

* **[AWS Access & Configuration Manual](./AWS_ACCESS_GUIDE.md)**: A complete guide on how AWS is configured on your machine, how to verify your access using the canonical `study` profile, and how to securely restore your credentials when moving to a new laptop.
* **[Secrets & Passphrase Guide](./PASSPHRASE_GUIDE.md)**: Details on how the encrypted secrets system works, the master passphrase, and how the automated local seed ensures you only have to authenticate once per machine.

## How to Use This Folder

1. **Read First:** If you are trying to understand how a tool or integration works within StudyBook, check here first for a quick-start guide.
2. **Add New Guides:** When we establish a new major workflow (like a new database connection, a new API integration, or a deployment process), we should create a new markdown file in this folder to document the "how-to".
3. **Agent Context:** AI agents (like Antigravity) will read these manuals to understand the current state of your machine's setup without having to reverse-engineer the underlying scripts.

---
*If you need to dive deeper into the technical implementation, refer to the `operations/` directory for the underlying scripts and automation workflows.*
