# Daily Todo System

Use this to track reminders and quickly answer:
- what is due today,
- what is due tomorrow,
- what is leftover (overdue).

## Data File

- `agents/shared/daily_todo.json`

## Command

- `.\scripts\ops\daily_todo.ps1`

## Common Usage

- Show daily summary:
  - `.\scripts\ops\daily_todo.ps1 -Action summary`
- Show all open tasks:
  - `.\scripts\ops\daily_todo.ps1 -Action list`
- Add a task:
  - `.\scripts\ops\daily_todo.ps1 -Action add -Title "Website submission inspection" -DueDate 2026-04-11 -Context "temp/seanlgirgis.github.io"`
- Mark done:
  - `.\scripts\ops\daily_todo.ps1 -Action done -Id TODO-0001`

## Date Format

- Use `yyyy-MM-dd` (example: `2026-04-11`).
