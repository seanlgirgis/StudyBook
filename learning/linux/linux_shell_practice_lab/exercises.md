# Linux / Unix Shell Interview Practice Exercises

Try each command before checking the answers.

---

## A. Line Range Drills

Use `data/numbered_lines.txt`.

1. Display lines 5 through 10.
2. Display only line 12.
3. Display the first 7 lines.
4. Display the last 5 lines.
5. Display lines 20 through 25 using `awk`.
6. Display lines 20 through 25 using `sed`.
7. Show the file with line numbers.
8. Show lines 8 through 14 with line numbers.

---

## B. Grep / Search Drills

Use `logs/app.log`.

1. Show all ERROR lines.
2. Show all WARN lines.
3. Count the number of ERROR lines.
4. Show ERROR or WARN lines.
5. Show lines that do not contain INFO.
6. Search case-insensitively for `timeout`.
7. Show 2 lines after every ERROR.
8. Show 1 line before and 1 line after every ERROR.

---

## C. Log Analysis Drills

Use `logs/access.log`.

1. Show only HTTP 500 errors.
2. Count how many 404 responses exist.
3. Show the top 5 IP addresses by request count.
4. Show all requests to `/api/orders`.
5. Show only the status-code column.
6. Count requests by status code.
7. Show requests made after 10:05.
8. Find IP addresses that generated 500 errors.

---

## D. CSV Drills

Use `data/employees.csv`.

1. Show only employee names.
2. Show only employees in IT.
3. Count employees by department.
4. Show employees with salary greater than 100000.
5. Sort employees by salary descending.
6. Show only name and salary.
7. Find the average salary using `awk`.
8. Show the highest-paid employee.

Use `data/orders.csv`.

9. Show only completed orders.
10. Sum the amount of completed orders.
11. Count orders by status.
12. Show orders over 500.
13. Sort orders by amount descending.
14. Show total order amount by customer.

---

## E. Text Cleanup Drills

Use `data/messy_names.txt`.

1. Remove blank lines.
2. Convert all text to lowercase.
3. Trim leading spaces.
4. Trim trailing spaces.
5. Replace multiple spaces with one space.
6. Sort unique names.
7. Count duplicate names after normalization.

---

## F. Find Drills

Use the full lab folder.

1. Find all `.log` files.
2. Find all `.csv` files.
3. Find all files larger than 1 KB.
4. Find files modified today.
5. Search all files for the word `timeout`.
6. Search only `.log` files for `ERROR`.

---

## G. Config File Drills

Use `config/app.conf`.

1. Show lines that are not comments.
2. Show the database host.
3. Show all timeout settings.
4. Change `debug=false` to `debug=true` using `sed`.
5. Extract only config keys.
6. Extract only config values.

---

## H. Process / System Output Drills

Use `data/processes.txt`.

1. Show only python processes.
2. Show the process using the most CPU.
3. Show the process using the most memory.
4. Count processes by user.
5. Show only PID and command.
6. Find processes containing `spark`.

Use `data/disk_usage.txt`.

7. Show filesystems over 80%.
8. Sort filesystems by usage percentage.
9. Show only mount points.
10. Show `/var` usage.

---

## I. Shell Scripting Drills

Use `scripts/backup.sh`.

1. Identify the shebang line.
2. Find all variables.
3. Find all `if` statements.
4. Explain what the script does.
5. Modify the script to print a timestamp.
6. Modify the script to exit if source directory does not exist.
7. Make the script executable.
8. Run the script safely with sample arguments.

---

## J. Mini Mock Interview

Answer from memory first.

1. How do you print lines 5 to 10 of a file?
2. How do you find all files containing the word ERROR?
3. How do you count unique IP addresses in a log?
4. How do you show the last 100 lines of a log?
5. How do you follow a live log?
6. How do you find disk usage by folder?
7. How do you find files bigger than 100 MB?
8. How do you replace text in a file?
9. How do you get the second column of a CSV?
10. How do you count how many times each status code appears?
