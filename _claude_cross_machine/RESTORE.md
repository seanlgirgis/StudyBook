# Claude Cross-Machine Restore Guide

This folder is a backup of Claude Code config and memory files.
It lives inside the git repo so it travels with the codebase.

## What's Here

| Folder | Source | Purpose |
|--------|--------|---------|
| `memory/` | `C:\Users\<user>\.claude\projects\D--StudyBook\memory\` | Auto-memory — persists across conversations |
| `settings/` | `D:\StudyBook\.claude\` | Claude Code project settings and launch config |

## Restore on a New Machine

After cloning the repo, run these two commands:

```bash
# 1. Restore memory files
mkdir -p "C:/Users/$USERNAME/.claude/projects/D--StudyBook/memory"
cp _claude_cross_machine/memory/*.md "C:/Users/$USERNAME/.claude/projects/D--StudyBook/memory/"

# 2. Restore Claude settings
cp _claude_cross_machine/settings/settings.json .claude/settings.json
cp _claude_cross_machine/settings/launch.json .claude/launch.json
```

## Keeping This In Sync

Run this any time memory or settings change:

```bash
cp "C:/Users/$USERNAME/.claude/projects/D--StudyBook/memory/"*.md _claude_cross_machine/memory/
cp .claude/settings.json _claude_cross_machine/settings/settings.json
cp .claude/launch.json _claude_cross_machine/settings/launch.json
```

Then commit and push — memory travels with the repo.
