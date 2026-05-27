# Linux / Unix Utilities Interview Drill Curriculum

Created for practical WSL2 practice on Windows.

Goal: be ready for pointed interview questions such as:

> "How do you display line 5 through line 10 of a file?"

The simple answer:

```bash
sed -n '5,10p' filename
```

Other valid answers:

```bash
awk 'NR>=5 && NR<=10' filename
head -n 10 filename | tail -n 6
```

Why this matters:
Interviewers often use tiny shell questions to test whether you have
real day-to-day comfort with Linux, Unix, logs, files, pipelines, and
production support. This curriculum is built to make those questions
automatic.

---

# 0. How to Use This Curriculum

## Recommended Practice Setup

Use WSL2 on Windows.

Open Ubuntu / Debian WSL and create a practice folder:

```bash
mkdir -p ~/shell_interview_drills
cd ~/shell_interview_drills
```

Create a sample file:

```bash
cat > sample.txt <<'EOF'
line 1 apple
line 2 banana
line 3 cherry
line 4 date
line 5 error one
line 6 warning one
line 7 info one
line 8 error two
line 9 banana
line 10 cherry
line 11 final
line 12 done
EOF
```

Create a sample CSV:

```bash
cat > employees.csv <<'EOF'
id,name,dept,salary
1,Alice,Data,120000
2,Bob,IT,95000
3,Carol,Data,130000
4,Dan,Finance,90000
5,Eve,IT,105000
EOF
```

Create a sample log:

```bash
cat > app.log <<'EOF'
2026-05-01 10:00:01 INFO service started
2026-05-01 10:01:03 ERROR failed to connect to db
2026-05-01 10:02:15 WARN retrying db connection
2026-05-01 10:03:20 INFO request completed user=100 status=200
2026-05-01 10:04:21 ERROR timeout user=101 status=504
2026-05-01 10:05:30 INFO request completed user=102 status=200
2026-05-01 10:06:44 ERROR failed to connect to db
EOF
```

Practice rule:
Read the question first, try the command without looking, then check
the answer.

---

# 1. Core File Viewing

## Q1. Display an entire file.

```bash
cat sample.txt
```

Also useful:

```bash
less sample.txt
more sample.txt
```

Use `less` for large files because it does not dump everything to the
screen at once.

---

## Q2. Display the first 10 lines.

```bash
head sample.txt
```

Explicit version:

```bash
head -n 10 sample.txt
```

---

## Q3. Display the last 10 lines.

```bash
tail sample.txt
```

Explicit version:

```bash
tail -n 10 sample.txt
```

---

## Q4. Display line 5 through line 10.

Best answer:

```bash
sed -n '5,10p' sample.txt
```

Alternative:

```bash
awk 'NR>=5 && NR<=10' sample.txt
```

Pipeline version:

```bash
head -n 10 sample.txt | tail -n 6
```

Explanation:
`head -n 10` gives lines 1 through 10.
`tail -n 6` then keeps lines 5 through 10.

---

## Q5. Display only line 5.

```bash
sed -n '5p' sample.txt
```

Alternative:

```bash
awk 'NR==5' sample.txt
```

---

## Q6. Display line numbers with the file.

```bash
nl -ba sample.txt
```

Alternative:

```bash
cat -n sample.txt
```

---

## Q7. Display lines 5 through 10 with line numbers.

```bash
nl -ba sample.txt | sed -n '5,10p'
```

---

# 2. Searching Text with grep

## Q8. Find lines containing `error`.

```bash
grep 'error' sample.txt
```

Case-insensitive:

```bash
grep -i 'error' sample.txt
```

---

## Q9. Find lines that do not contain `error`.

```bash
grep -v 'error' sample.txt
```

---

## Q10. Find lines containing either `error` or `warning`.

```bash
grep -E 'error|warning' sample.txt
```

Alternative:

```bash
egrep 'error|warning' sample.txt
```

---

## Q11. Count matching lines.

```bash
grep -c 'error' sample.txt
```

---

## Q12. Show matching line numbers.

```bash
grep -n 'error' sample.txt
```

---

## Q13. Show 2 lines before and after each error in a log.

```bash
grep -C 2 'ERROR' app.log
```

Before only:

```bash
grep -B 2 'ERROR' app.log
```

After only:

```bash
grep -A 2 'ERROR' app.log
```

---

## Q14. Search recursively in a folder.

```bash
grep -R 'ERROR' .
```

With line numbers:

```bash
grep -Rni 'ERROR' .
```

---

# 3. Counting and File Size

## Q15. Count lines in a file.

```bash
wc -l sample.txt
```

---

## Q16. Count words in a file.

```bash
wc -w sample.txt
```

---

## Q17. Count bytes in a file.

```bash
wc -c sample.txt
```

---

## Q18. Count files in the current directory.

```bash
ls -1 | wc -l
```

Better for regular files only:

```bash
find . -maxdepth 1 -type f | wc -l
```

---

## Q19. Count `.log` files recursively.

```bash
find . -type f -name '*.log' | wc -l
```

---

# 4. Sorting and Unique Values

## Q20. Sort a file alphabetically.

```bash
sort sample.txt
```

---

## Q21. Sort and remove duplicate lines.

```bash
sort sample.txt | uniq
```

Shorter:

```bash
sort -u sample.txt
```

---

## Q22. Count duplicate values.

```bash
sort sample.txt | uniq -c
```

Sort by most frequent:

```bash
sort sample.txt | uniq -c | sort -nr
```

---

## Q23. Find duplicate lines only.

```bash
sort sample.txt | uniq -d
```

---

## Q24. Find unique lines only.

```bash
sort sample.txt | uniq -u
```

---

# 5. cut, awk, and Column Extraction

## Q25. Print the first column of a CSV.

```bash
cut -d',' -f1 employees.csv
```

---

## Q26. Print name and salary from CSV.

```bash
cut -d',' -f2,4 employees.csv
```

---

## Q27. Print employees in the Data department.

```bash
awk -F',' '$3=="Data"' employees.csv
```

---

## Q28. Print names where salary is greater than 100000.

```bash
awk -F',' 'NR>1 && $4>100000 {print $2}' employees.csv
```

---

## Q29. Sum all salaries.

```bash
awk -F',' 'NR>1 {sum+=$4} END {print sum}' employees.csv
```

---

## Q30. Average salary.

```bash
awk -F',' 'NR>1 {sum+=$4; count++} END {print sum/count}' employees.csv
```

---

# 6. sed Editing and Printing

## Q31. Replace first occurrence of `error` with `ERROR`.

```bash
sed 's/error/ERROR/' sample.txt
```

---

## Q32. Replace all occurrences of `error` with `ERROR`.

```bash
sed 's/error/ERROR/g' sample.txt
```

---

## Q33. Delete blank lines.

```bash
sed '/^$/d' sample.txt
```

---

## Q34. Delete lines containing `banana`.

```bash
sed '/banana/d' sample.txt
```

---

## Q35. Print only lines matching `error`.

```bash
sed -n '/error/p' sample.txt
```

---

# 7. find Command

## Q36. Find all `.txt` files.

```bash
find . -type f -name '*.txt'
```

---

## Q37. Find files modified in the last 1 day.

```bash
find . -type f -mtime -1
```

---

## Q38. Find files larger than 10 MB.

```bash
find . -type f -size +10M
```

---

## Q39. Find empty files.

```bash
find . -type f -empty
```

---

## Q40. Find directories only.

```bash
find . -type d
```

---

## Q41. Delete empty files carefully.

Preview first:

```bash
find . -type f -empty
```

Delete:

```bash
find . -type f -empty -delete
```

---

# 8. xargs and Command Chaining

## Q42. Count lines in all `.txt` files.

```bash
find . -type f -name '*.txt' | xargs wc -l
```

Safer with spaces in filenames:

```bash
find . -type f -name '*.txt' -print0 | xargs -0 wc -l
```

---

## Q43. Search for ERROR in all log files.

```bash
find . -type f -name '*.log' -print0 | xargs -0 grep -n 'ERROR'
```

---

## Q44. Copy all `.log` files into a folder.

```bash
mkdir -p logs_copy
find . -type f -name '*.log' -exec cp {} logs_copy/ \;
```

---

# 9. Permissions and Ownership

## Q45. Show file permissions.

```bash
ls -l sample.txt
```

---

## Q46. Make a script executable.

```bash
chmod +x script.sh
```

---

## Q47. Remove execute permission.

```bash
chmod -x script.sh
```

---

## Q48. What does `chmod 755 script.sh` mean?

Owner: read, write, execute  
Group: read, execute  
Others: read, execute

Command:

```bash
chmod 755 script.sh
```

---

## Q49. What does `chmod 644 file.txt` mean?

Owner: read, write  
Group: read  
Others: read

Command:

```bash
chmod 644 file.txt
```

---

# 10. Processes

## Q50. Show running processes.

```bash
ps aux
```

---

## Q51. Find a running process by name.

```bash
ps aux | grep python
```

Better:

```bash
pgrep -a python
```

---

## Q52. Kill a process by PID.

```bash
kill PID
```

Force kill:

```bash
kill -9 PID
```

Use `kill -9` only when normal kill does not work.

---

## Q53. Monitor processes interactively.

```bash
top
```

Or, if installed:

```bash
htop
```

---

# 11. Disk and Memory

## Q54. Check disk space.

```bash
df -h
```

---

## Q55. Check folder size.

```bash
du -sh .
```

---

## Q56. Show largest folders in current directory.

```bash
du -sh * | sort -hr | head
```

---

## Q57. Check memory.

```bash
free -h
```

---

# 12. Environment Variables and Paths

## Q58. Show PATH.

```bash
echo "$PATH"
```

---

## Q59. Show all environment variables.

```bash
env
```

---

## Q60. Set a temporary environment variable.

```bash
export APP_ENV=dev
```

Check it:

```bash
echo "$APP_ENV"
```

---

## Q61. Find where a command lives.

```bash
which python
```

More complete:

```bash
type python
```

---

# 13. Redirection and Pipes

## Q62. Redirect output to a file.

```bash
ls -l > files.txt
```

---

## Q63. Append output to a file.

```bash
date >> run.log
```

---

## Q64. Redirect errors to a file.

```bash
ls missing_file 2> error.log
```

---

## Q65. Redirect output and errors to one file.

```bash
command > output.log 2>&1
```

Modern Bash version:

```bash
command &> output.log
```

---

## Q66. Pipe output from one command into another.

```bash
cat sample.txt | grep error
```

Better, without unnecessary cat:

```bash
grep error sample.txt
```

---

# 14. Shell Scripting Basics

Create a script:

```bash
cat > hello.sh <<'EOF'
#!/usr/bin/env bash
echo "Hello from shell"
EOF

chmod +x hello.sh
./hello.sh
```

---

## Q67. Use a variable.

```bash
name="Sean"
echo "Hello $name"
```

---

## Q68. Read a command-line argument.

```bash
cat > args.sh <<'EOF'
#!/usr/bin/env bash
echo "First argument: $1"
EOF

chmod +x args.sh
./args.sh test
```

---

## Q69. Check if a file exists.

```bash
if [ -f sample.txt ]; then
  echo "file exists"
else
  echo "file missing"
fi
```

---

## Q70. Loop over files.

```bash
for file in *.txt; do
  echo "File: $file"
done
```

---

## Q71. Exit if a command fails.

```bash
set -e
```

Common robust script header:

```bash
#!/usr/bin/env bash
set -euo pipefail
```

Meaning:
- `-e`: exit on command failure
- `-u`: error on unset variables
- `-o pipefail`: fail pipeline if any command fails

---

# 15. Logs and Production Support Questions

## Q72. Show last 100 lines of a log.

```bash
tail -n 100 app.log
```

---

## Q73. Follow a log live.

```bash
tail -f app.log
```

Last 100 lines and keep following:

```bash
tail -n 100 -f app.log
```

---

## Q74. Count ERROR lines.

```bash
grep -c 'ERROR' app.log
```

---

## Q75. Show unique error messages.

```bash
grep 'ERROR' app.log | cut -d' ' -f4- | sort | uniq -c | sort -nr
```

---

## Q76. Find logs between approximate timestamps.

With simple grep:

```bash
grep '2026-05-01 10:0[2-5]' app.log
```

With awk string comparison:

```bash
awk '$1" "$2 >= "2026-05-01 10:02:00" && $1" "$2 <= "2026-05-01 10:05:59"' app.log
```

---

# 16. Compression and Archives

## Q77. Create a tar.gz archive.

```bash
tar -czf archive.tar.gz sample.txt employees.csv app.log
```

---

## Q78. Extract a tar.gz archive.

```bash
tar -xzf archive.tar.gz
```

---

## Q79. List archive contents without extracting.

```bash
tar -tzf archive.tar.gz
```

---

## Q80. Zip a folder.

```bash
zip -r myfolder.zip myfolder
```

---

## Q81. Unzip a file.

```bash
unzip myfolder.zip
```

---

# 17. Networking Basics

## Q82. Test if a host is reachable.

```bash
ping google.com
```

Stop with `Ctrl+C`.

---

## Q83. Test HTTP response headers.

```bash
curl -I https://example.com
```

---

## Q84. Download a URL.

```bash
curl -O https://example.com/file.txt
```

Or:

```bash
wget https://example.com/file.txt
```

---

## Q85. Check listening ports.

```bash
ss -tulpn
```

Older command:

```bash
netstat -tulpn
```

---

# 18. Date and Scheduling

## Q86. Show current date.

```bash
date
```

---

## Q87. Format date.

```bash
date '+%Y-%m-%d %H:%M:%S'
```

---

## Q88. Show cron jobs.

```bash
crontab -l
```

---

## Q89. Edit cron jobs.

```bash
crontab -e
```

Example: run every day at 2:30 AM.

```cron
30 2 * * * /path/to/script.sh
```

---

# 19. Common Interview Gotchas

## Gotcha 1. `cat file | grep pattern`

This works, but it is usually unnecessary.

Okay:

```bash
cat sample.txt | grep error
```

Better:

```bash
grep error sample.txt
```

---

## Gotcha 2. `grep` is case-sensitive by default.

Use:

```bash
grep -i error app.log
```

---

## Gotcha 3. `uniq` only works on adjacent duplicates.

Wrong if file is unsorted:

```bash
uniq sample.txt
```

Better:

```bash
sort sample.txt | uniq
```

---

## Gotcha 4. Spaces in filenames break simple xargs.

Risky:

```bash
find . -type f | xargs grep ERROR
```

Safer:

```bash
find . -type f -print0 | xargs -0 grep ERROR
```

---

## Gotcha 5. `>` overwrites. `>>` appends.

Overwrite:

```bash
echo "hello" > file.txt
```

Append:

```bash
echo "hello" >> file.txt
```

---

## Gotcha 6. Single quotes vs double quotes.

Single quotes do not expand variables:

```bash
name=Sean
echo '$name'
```

Output:

```text
$name
```

Double quotes expand variables:

```bash
echo "$name"
```

Output:

```text
Sean
```

---

# 20. Practice Exam 1: Core Commands

Try to answer without looking.

1. Show first 20 lines of `app.log`.
2. Show last 50 lines of `app.log`.
3. Show line 5 to line 10 of `sample.txt`.
4. Count how many lines contain `ERROR`.
5. Search for `ERROR` case-insensitively.
6. Show line numbers for matching errors.
7. Find all `.txt` files.
8. Count all `.txt` files.
9. Sort a file and remove duplicates.
10. Find duplicate lines only.

## Answers

```bash
head -n 20 app.log
tail -n 50 app.log
sed -n '5,10p' sample.txt
grep -c 'ERROR' app.log
grep -i 'error' app.log
grep -n 'ERROR' app.log
find . -type f -name '*.txt'
find . -type f -name '*.txt' | wc -l
sort sample.txt | uniq
sort sample.txt | uniq -d
```

---

# 21. Practice Exam 2: Data Engineering Shell Questions

1. From a CSV, print column 2.
2. From a CSV, print rows where department is `Data`.
3. Sum salary column.
4. Count rows excluding header.
5. Show the top 5 most common log messages.
6. Find files larger than 100 MB.
7. Check disk usage.
8. Check memory.
9. Show the largest folders.
10. Make a shell script executable.

## Answers

```bash
cut -d',' -f2 employees.csv
awk -F',' '$3=="Data"' employees.csv
awk -F',' 'NR>1 {sum+=$4} END {print sum}' employees.csv
awk 'NR>1 {count++} END {print count}' employees.csv
grep 'ERROR' app.log | cut -d' ' -f4- | sort | uniq -c | sort -nr | head -n 5
find . -type f -size +100M
df -h
free -h
du -sh * | sort -hr | head
chmod +x script.sh
```

---

# 22. Practice Exam 3: Production Support Scenario

Scenario:
A batch job failed overnight. You have a log file named `batch.log`.

Answer these:

1. Show the last 200 lines.
2. Search for errors.
3. Count errors.
4. Show 3 lines before and after every error.
5. Find unique error messages.
6. Save errors into `errors_only.log`.
7. Check if the file is empty.
8. Compress the log for sending.
9. Find the job script in the current project.
10. Check whether a related Python process is still running.

## Answers

```bash
tail -n 200 batch.log
grep -i 'error' batch.log
grep -ic 'error' batch.log
grep -i -C 3 'error' batch.log
grep -i 'error' batch.log | sort | uniq -c | sort -nr
grep -i 'error' batch.log > errors_only.log
[ -s errors_only.log ] && echo "has content" || echo "empty"
tar -czf batch_log_bundle.tar.gz batch.log errors_only.log
find . -type f -name '*.sh'
pgrep -a python
```

---

# 23. Mini Daily Drill Plan

## Day 1: Viewing and searching

Practice:
- `cat`
- `less`
- `head`
- `tail`
- `sed -n`
- `grep`
- `grep -i`
- `grep -n`
- `grep -C`

Key target:
Be able to answer line-range questions instantly.

---

## Day 2: Sorting, counting, and duplicate handling

Practice:
- `wc`
- `sort`
- `uniq`
- `sort | uniq -c`
- `sort -u`

Key target:
Be able to count and summarize text quickly.

---

## Day 3: CSV and awk

Practice:
- `cut -d',' -f`
- `awk -F','`
- `NR`
- `$1`, `$2`, `$3`
- simple filters
- sums and averages

Key target:
Be able to manipulate small structured files from the shell.

---

## Day 4: find, xargs, and files

Practice:
- `find`
- `-name`
- `-type f`
- `-mtime`
- `-size`
- `xargs`
- `-print0 | xargs -0`

Key target:
Be able to find and process files safely.

---

## Day 5: Shell scripting

Practice:
- variables
- arguments
- if statements
- loops
- executable scripts
- `set -euo pipefail`

Key target:
Be able to write a small safe script.

---

## Day 6: Production support

Practice:
- logs
- errors
- disk
- memory
- processes
- permissions
- compression

Key target:
Sound like someone who can support real jobs.

---

## Day 7: Mock interview

Use the practice exams.
Time yourself.
Do not look at answers until done.

---

# 24. Interview Answer Style

When asked:

> How do you display line 5 through line 10 of a file?

Say:

```text
I would usually use sed:
sed -n '5,10p' filename

The -n suppresses normal output, and 5,10p prints only lines 5
through 10. Another way is awk with NR between 5 and 10.
```

When asked:

> How do you find errors in a log?

Say:

```text
I would start with grep, usually case-insensitive:
grep -i error app.log

If I need context around the error:
grep -i -C 3 error app.log

Then I might count or summarize:
grep -ic error app.log
```

When asked:

> How do you find large files?

Say:

```text
find . -type f -size +100M
```

When asked:

> How do you check disk usage?

Say:

```text
df -h for filesystem space.
du -sh folder_name for folder size.
```

---

# 25. Commands to Memorize Cold

```bash
sed -n '5,10p' file
awk 'NR>=5 && NR<=10' file
head -n 10 file
tail -n 10 file
grep -i 'error' file
grep -n 'error' file
grep -C 3 'error' file
wc -l file
sort file | uniq -c | sort -nr
cut -d',' -f2 file.csv
awk -F',' 'NR>1 {print $2}' file.csv
find . -type f -name '*.log'
find . -type f -size +100M
df -h
du -sh *
free -h
ps aux | grep process_name
pgrep -a process_name
chmod +x script.sh
tar -czf archive.tar.gz folder_or_files
```

---

# 26. Final Advice

This topic is not about memorizing hundreds of commands.
It is about becoming fluent with a small toolbelt:

- view files
- search files
- extract lines
- count things
- sort and summarize
- find files
- check logs
- check disk/memory/processes
- write tiny scripts safely

If you master these, the interviewer can still ask a tricky question,
but it will not feel like an ambush.
