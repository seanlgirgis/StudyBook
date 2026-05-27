# Expected Answers

Do not read this first. Try the exercises before checking.

---

## A. Line Range Drills

```bash
sed -n '5,10p' data/numbered_lines.txt
sed -n '12p' data/numbered_lines.txt
head -n 7 data/numbered_lines.txt
tail -n 5 data/numbered_lines.txt
awk 'NR>=20 && NR<=25' data/numbered_lines.txt
sed -n '20,25p' data/numbered_lines.txt
nl -ba data/numbered_lines.txt
nl -ba data/numbered_lines.txt | sed -n '8,14p'
```

## B. Grep / Search Drills

```bash
grep 'ERROR' logs/app.log
grep 'WARN' logs/app.log
grep -c 'ERROR' logs/app.log
grep -E 'ERROR|WARN' logs/app.log
grep -v 'INFO' logs/app.log
grep -i 'timeout' logs/app.log
grep -A 2 'ERROR' logs/app.log
grep -B 1 -A 1 'ERROR' logs/app.log
```

## C. Log Analysis Drills

```bash
awk '$9 == 500' logs/access.log
awk '$9 == 404 {count++} END {print count}' logs/access.log
awk '{print $1}' logs/access.log | sort | uniq -c | sort -nr | head -5
grep '/api/orders' logs/access.log
awk '{print $9}' logs/access.log
awk '{print $9}' logs/access.log | sort | uniq -c | sort -nr
awk '$4 > "[27/May/2026:10:05:00"' logs/access.log
awk '$9 == 500 {print $1}' logs/access.log | sort -u
```

## D. CSV Drills

```bash
cut -d',' -f2 data/employees.csv
awk -F',' '$3 == "IT"' data/employees.csv
awk -F',' 'NR>1 {count[$3]++} END {for (d in count) print d, count[d]}' data/employees.csv
awk -F',' 'NR>1 && $4 > 100000' data/employees.csv
sort -t',' -k4,4nr data/employees.csv
awk -F',' '{print $2 "," $4}' data/employees.csv
awk -F',' 'NR>1 {sum+=$4; count++} END {print sum/count}' data/employees.csv
sort -t',' -k4,4nr data/employees.csv | head -2

awk -F',' '$3 == "completed"' data/orders.csv
awk -F',' 'NR>1 && $3 == "completed" {sum+=$4} END {print sum}' data/orders.csv
awk -F',' 'NR>1 {count[$3]++} END {for (s in count) print s, count[s]}' data/orders.csv
awk -F',' 'NR>1 && $4 > 500' data/orders.csv
sort -t',' -k4,4nr data/orders.csv
awk -F',' 'NR>1 {sum[$2]+=$4} END {for (c in sum) print c, sum[c]}' data/orders.csv
```

## E. Text Cleanup Drills

```bash
grep -v '^$' data/messy_names.txt
tr '[:upper:]' '[:lower:]' < data/messy_names.txt
sed 's/^ *//' data/messy_names.txt
sed 's/ *$//' data/messy_names.txt
tr -s ' ' < data/messy_names.txt
tr '[:upper:]' '[:lower:]' < data/messy_names.txt | sed 's/^ *//;s/ *$//;s/  */ /g' | grep -v '^$' | sort -u
tr '[:upper:]' '[:lower:]' < data/messy_names.txt | sed 's/^ *//;s/ *$//;s/  */ /g' | grep -v '^$' | sort | uniq -c
```

## F. Find Drills

```bash
find . -name '*.log'
find . -name '*.csv'
find . -type f -size +1k
find . -type f -mtime -1
grep -R 'timeout' .
find . -name '*.log' -print0 | xargs -0 grep 'ERROR'
```

## G. Config File Drills

```bash
grep -v '^#' config/app.conf | grep -v '^$'
grep '^db_host=' config/app.conf
grep 'timeout' config/app.conf
sed 's/debug=false/debug=true/' config/app.conf
cut -d'=' -f1 config/app.conf | grep -v '^#' | grep -v '^$'
cut -d'=' -f2 config/app.conf | grep -v '^#' | grep -v '^$'
```

## H. Process / System Output Drills

```bash
grep 'python' data/processes.txt
sort -k3,3nr data/processes.txt | head -2
sort -k4,4nr data/processes.txt | head -2
awk 'NR>1 {count[$1]++} END {for (u in count) print u, count[u]}' data/processes.txt
awk 'NR==1 {print $2, $5} NR>1 {print $2, $5}' data/processes.txt
grep 'spark' data/processes.txt

awk 'NR>1 {gsub("%","",$5); if ($5 > 80) print}' data/disk_usage.txt
sort -k5,5nr data/disk_usage.txt
awk 'NR>1 {print $6}' data/disk_usage.txt
awk '$6 == "/var"' data/disk_usage.txt
```

## I. Shell Scripting Drills

```bash
head -n 1 scripts/backup.sh
grep '=' scripts/backup.sh
grep '^if' scripts/backup.sh
chmod +x scripts/backup.sh
./scripts/backup.sh data /tmp/practice_backup
```

## J. Mini Mock Interview

```bash
sed -n '5,10p' file.txt
grep -R 'ERROR' .
awk '{print $1}' access.log | sort -u | wc -l
tail -n 100 app.log
tail -f app.log
du -sh *
find . -type f -size +100M
sed -i 's/old/new/g' file.txt
cut -d',' -f2 file.csv
awk '{print $9}' access.log | sort | uniq -c | sort -nr
```
