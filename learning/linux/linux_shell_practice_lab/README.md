# Linux / Unix Shell Interview Practice Lab

This folder gives you sample files to practice the shell interview drills.

## How to use in WSL2

Copy or unzip this folder somewhere inside WSL2, then run:

```bash
cd linux_shell_practice_lab
ls -R
```

Start with:

```bash
cat exercises.md
```

## Main files

- `data/numbered_lines.txt` — practice `sed`, `awk`, `head`, `tail`
- `logs/app.log` — practice `grep`, `tail`, `awk`, `sort`, `uniq`
- `logs/access.log` — practice web/server log analysis
- `data/employees.csv` — practice CSV filtering and counting
- `data/orders.csv` — practice sorting, summing, grouping
- `data/messy_names.txt` — practice cleanup with `tr`, `sed`, `awk`
- `config/app.conf` — practice config searching
- `data/processes.txt` — practice process-style questions
- `data/disk_usage.txt` — practice disk/memory style questions
- `scripts/backup.sh` — practice shell script reading

## Interview mindset

These questions are often not about memorizing every command.
They test whether you know the everyday tools:

- `cat`
- `less`
- `head`
- `tail`
- `sed`
- `awk`
- `grep`
- `cut`
- `sort`
- `uniq`
- `wc`
- `find`
- `xargs`
- `chmod`
- `ps`
- `df`
- `du`

Use the `expected_answers/answers.md` file after you try the exercises.
