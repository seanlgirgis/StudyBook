# `sed` — The Stream Editor: A Complete Guide for Data Engineers & Production Support

> **"Simplicity and clarity is Gold."**  
> Mastering `sed` means editing streams of text with surgical precision — no editor, no GUI, just pipeline power.

---

## Table of Contents

1. [What Is `sed`?](#1-what-is-sed)
2. [How `sed` Works — The Mental Model](#2-how-sed-works--the-mental-model)
3. [Basic Syntax](#3-basic-syntax)
4. [The Core Commands](#4-the-core-commands)
   - [4.1 Substitution — `s`](#41-substitution--s)
   - [4.2 Delete — `d`](#42-delete--d)
   - [4.3 Print — `p`](#43-print--p)
   - [4.4 Quit — `q`](#44-quit--q)
   - [4.5 Insert / Append / Change — `i`, `a`, `c`](#45-insert--append--change--i-a-c)
   - [4.6 Read / Write File — `r`, `w`](#46-read--write-file--r-w)
   - [4.7 Transform — `y`](#47-transform--y)
   - [4.8 Labels and Branching — `b`, `t`, `T`](#48-labels-and-branching--b-t-t)
   - [4.9 Hold Space — `h`, `H`, `g`, `G`, `x`](#49-hold-space--h-h-g-g-x)
   - [4.10 Multiple Expressions — `-e`](#410-multiple-expressions---e)
5. [Address Types — Line Targeting](#5-address-types--line-targeting)
   - [5.1 Line Number Address](#51-line-number-address)
   - [5.2 Regex Address](#52-regex-address)
   - [5.3 Range Address](#53-range-address)
   - [5.4 Step Address (GNU sed)](#54-step-address-gnu-sed)
   - [5.5 Negation with `!`](#55-negation-with-)
6. [Flags & Options](#6-flags--options)
7. [Regex Basics in `sed`](#7-regex-basics-in-sed)
   - [7.1 BRE vs ERE](#71-bre-vs-ere)
   - [7.2 Capture Groups and Back-References](#72-capture-groups-and-back-references)
   - [7.3 Common Patterns](#73-common-patterns)
8. [In-Place Editing — The `-i` Flag](#8-in-place-editing--the--i-flag)
9. [Delimiters — Not Just `/`](#9-delimiters--not-just-)
10. [Multi-line Operations](#10-multi-line-operations)
11. [Practical Examples Library](#11-practical-examples-library)
    - [11.1 Text Substitution](#111-text-substitution)
    - [11.2 Line Operations](#112-line-operations)
    - [11.3 Extracting Data](#113-extracting-data)
    - [11.4 Formatting & Cleanup](#114-formatting--cleanup)
    - [11.5 Config File Manipulation](#115-config-file-manipulation)
12. [Data Engineering Use Cases](#12-data-engineering-use-cases)
    - [12.1 ETL Pipeline Preprocessing](#121-etl-pipeline-preprocessing)
    - [12.2 Schema & DDL Transformations](#122-schema--ddl-transformations)
    - [12.3 Log File Processing](#123-log-file-processing)
    - [12.4 CSV / Delimited File Manipulation](#124-csv--delimited-file-manipulation)
    - [12.5 Environment & Config Management](#125-environment--config-management)
    - [12.6 Batch File Operations](#126-batch-file-operations)
13. [Production Support Use Cases](#13-production-support-use-cases)
    - [13.1 Incident Triage — Log Filtering](#131-incident-triage--log-filtering)
    - [13.2 Masking Sensitive Data](#132-masking-sensitive-data)
    - [13.3 Hotfix Deployments](#133-hotfix-deployments)
    - [13.4 Redacting PII Before Sharing Logs](#134-redacting-pii-before-sharing-logs)
14. [sed in Shell Scripts & Pipelines](#14-sed-in-shell-scripts--pipelines)
15. [sed vs. Other Tools — When to Use What](#15-sed-vs-other-tools--when-to-use-what)
16. [Common Pitfalls & Gotchas](#16-common-pitfalls--gotchas)
17. [Quick Reference Cheat Sheet](#17-quick-reference-cheat-sheet)

---

## 1. What Is `sed`?

[↑ Back to TOC](#table-of-contents)

`sed` stands for **Stream EDitor**. It is a non-interactive, line-oriented text transformation utility found on every Unix/Linux system. It was written at Bell Labs by Lee McMahon in the 1970s and remains one of the most powerful one-liner tools in a DE or sysadmin's toolkit.

**Key characteristics:**

| Property | Description |
|---|---|
| **Non-interactive** | No editor opens — transforms happen automatically |
| **Stream-based** | Reads line by line; does not load the whole file into memory |
| **In-memory** | Default: does not modify source files (use `-i` for in-place) |
| **Scriptable** | Supports complex multi-command scripts |
| **Pipeline-friendly** | Works seamlessly with `cat`, `grep`, `awk`, `cut`, pipes |
| **Regex-powered** | Uses Basic Regular Expressions (BRE) by default, ERE with `-E` |

`sed` is the right tool when you need to:
- Find and replace text at scale
- Delete or extract specific lines
- Transform file content as part of a pipeline
- Make automated edits to config files in CI/CD

---

## 2. How `sed` Works — The Mental Model

[↑ Back to TOC](#table-of-contents)

Think of `sed` as a two-buffer machine riding a conveyor belt of lines:

```
Input File / stdin
        │
        ▼  (one line at a time)
┌─────────────────────────────────────────┐
│            Pattern Space                │  ← active working buffer
│         (current line lives here)       │
└─────────────────────────────────────────┘
        │
        │  commands execute here (s, d, p, etc.)
        ▼
┌─────────────────────────────────────────┐
│             Hold Space                  │  ← persistent scratch buffer
│        (survives across lines)          │
└─────────────────────────────────────────┘
        │
        ▼ (end of cycle: print pattern space, load next line)
     stdout / output file
```

**The cycle for each line:**
1. Read a line into the **Pattern Space** (newline stripped)
2. Execute all `sed` commands against Pattern Space
3. (Unless `-n` is set) **Auto-print** Pattern Space to stdout
4. Clear Pattern Space, load next line → repeat

**Hold Space** is a secondary buffer that persists across lines. You manually copy data in/out with `h`, `H`, `g`, `G`, `x`. This is the secret to multi-line operations.

---

## 3. Basic Syntax

[↑ Back to TOC](#table-of-contents)

```bash
sed [OPTIONS] 'SCRIPT' [FILE...]
sed [OPTIONS] -e 'COMMAND1' -e 'COMMAND2' [FILE...]
sed [OPTIONS] -f script.sed [FILE...]
```

**Simplest form:**

```bash
sed 's/old/new/' file.txt
```

This substitutes the first occurrence of `old` with `new` on each line and prints to stdout. The source file is **not modified**.

**Multiple input files:**

```bash
sed 's/foo/bar/' file1.txt file2.txt file3.txt
```

`sed` processes them as a single concatenated stream.

**From stdin (pipeline):**

```bash
cat file.txt | sed 's/foo/bar/'
echo "Hello World" | sed 's/World/Sean/'
```

---

## 4. The Core Commands

[↑ Back to TOC](#table-of-contents)

---

### 4.1 Substitution — `s`

[↑ Back to TOC](#table-of-contents)

The most-used command by far. Replaces a pattern with a replacement string.

**Syntax:**

```bash
s/PATTERN/REPLACEMENT/[FLAGS]
```

**Basic substitution — first occurrence per line:**

```bash
sed 's/error/ERROR/' app.log
```

**Global — all occurrences per line:**

```bash
sed 's/error/ERROR/g' app.log
```

**Case-insensitive (GNU sed):**

```bash
sed 's/error/ERROR/gI' app.log
```

**Nth occurrence only:**

```bash
# Replace only the 2nd occurrence on each line
sed 's/foo/bar/2' file.txt

# Replace from the 3rd occurrence onward
sed 's/foo/bar/3g' file.txt
```

**Using & — reference the matched text:**

```bash
# Wrap every number in brackets
echo "ID 42 and 99" | sed 's/[0-9]*/[&]/g'
# Output: ID [42] and [99]
```

**Write substitution results to a file:**

```bash
sed 's/INFO/PROCESSED/w output.txt' app.log
```

---

### 4.2 Delete — `d`

[↑ Back to TOC](#table-of-contents)

Deletes lines matching an address or pattern. The deleted line is NOT printed.

```bash
# Delete blank lines
sed '/^$/d' file.txt

# Delete lines containing "DEBUG"
sed '/DEBUG/d' app.log

# Delete line 5
sed '5d' file.txt

# Delete lines 3 through 7
sed '3,7d' file.txt

# Delete from line 10 to end of file
sed '10,$d' file.txt

# Delete lines starting with #  (comments in config files)
sed '/^#/d' config.properties
```

---

### 4.3 Print — `p`

[↑ Back to TOC](#table-of-contents)

Explicitly prints the Pattern Space. Most useful with `-n` to suppress default printing.

```bash
# Print only lines containing "ERROR" (like grep)
sed -n '/ERROR/p' app.log

# Print only lines 5–10
sed -n '5,10p' file.txt

# Print only the last line
sed -n '$p' file.txt

# Print line numbers and content (GNU sed)
sed -n '/ERROR/{=;p}' app.log
```

---

### 4.4 Quit — `q`

[↑ Back to TOC](#table-of-contents)

Stops processing after a given line. Very efficient for large files when you only need the top.

```bash
# Print first 10 lines (like head)
sed '10q' file.txt

# Quit when a pattern is found
sed '/FATAL/q' app.log

# Quit immediately after printing first match
sed -n '/ERROR/{p;q}' app.log
```

**`Q`** (GNU sed) quits without printing the current line.

---

### 4.5 Insert / Append / Change — `i`, `a`, `c`

[↑ Back to TOC](#table-of-contents)

```bash
# INSERT before line 3
sed '3i\--- NEW LINE BEFORE ---' file.txt

# APPEND after a pattern match
sed '/HEADER/a\column1,column2,column3' data.csv

# CHANGE (replace entire matching line)
sed '/^version=/c\version=2.0.0' config.properties

# Insert before every line matching a pattern
sed '/^ERROR/i\--- BEGIN ERROR BLOCK ---' app.log
```

---

### 4.6 Read / Write File — `r`, `w`

[↑ Back to TOC](#table-of-contents)

```bash
# Read contents of header.txt and insert after line 1
sed '1r header.txt' data.csv

# Write lines matching ERROR to a separate file
sed -n '/ERROR/w errors.log' app.log

# Append matching lines to a file (use >> in wrapper script, or w appends in sed)
sed '/WARN/w warnings.log' app.log
```

---

### 4.7 Transform — `y`

[↑ Back to TOC](#table-of-contents)

Character-by-character substitution. Like `tr` but inside a `sed` script.

```bash
# Convert lowercase to uppercase (basic ASCII)
sed 'y/abcdefghijklmnopqrstuvwxyz/ABCDEFGHIJKLMNOPQRSTUVWXYZ/' file.txt

# Convert commas to pipes (CSV to pipe-delimited)
sed 'y/,/|/' file.csv

# Replace colons with equals signs
sed 'y/:/=/' config.txt
```

---

### 4.8 Labels and Branching — `b`, `t`, `T`

[↑ Back to TOC](#table-of-contents)

Used for loops and conditional logic within `sed` scripts.

```bash
# Branch to end (skip remaining commands) if line contains "SKIP"
sed '/SKIP/b; s/foo/bar/' file.txt

# t: branch if a substitution was made since last line/t
# Example: loop to collapse multiple spaces into one
sed ':loop; s/  / /g; t loop' file.txt

# T (GNU sed): branch if NO substitution was made
sed 's/ERROR/ALERT/; T skip; s/$/ CRITICAL/; :skip' app.log
```

---

### 4.9 Hold Space — `h`, `H`, `g`, `G`, `x`

[↑ Back to TOC](#table-of-contents)

The hold space is your scratch pad that persists across line cycles.

| Command | Action |
|---|---|
| `h` | Copy Pattern Space → Hold Space (overwrite) |
| `H` | Append Pattern Space → Hold Space (with `\n`) |
| `g` | Copy Hold Space → Pattern Space (overwrite) |
| `G` | Append Hold Space → Pattern Space (with `\n`) |
| `x` | Exchange Pattern Space and Hold Space |

```bash
# Reverse line order (tac equivalent)
sed -n '1!G; h; $p' file.txt

# Double-space a file (add blank line after each line)
sed 'G' file.txt

# Print lines in pairs: current + previous
sed -n 'H; ${g; s/^\n//; p}' file.txt
```

---

### 4.10 Multiple Expressions — `-e`

[↑ Back to TOC](#table-of-contents)

```bash
# Multiple substitutions in one command
sed -e 's/foo/bar/g' -e 's/baz/qux/g' file.txt

# Semicolon separator (equivalent)
sed 's/foo/bar/g; s/baz/qux/g' file.txt

# Using a script file
sed -f transformations.sed file.txt
```

---

## 5. Address Types — Line Targeting

[↑ Back to TOC](#table-of-contents)

An **address** tells `sed` *which lines* a command applies to. Without an address, the command applies to every line.

---

### 5.1 Line Number Address

[↑ Back to TOC](#table-of-contents)

```bash
sed '1s/^/# /' file.txt        # Add comment marker to line 1 only
sed '$d' file.txt               # Delete the last line
sed '1,5d' file.txt             # Delete lines 1 through 5
sed '3s/old/new/' file.txt      # Substitute only on line 3
```

---

### 5.2 Regex Address

[↑ Back to TOC](#table-of-contents)

```bash
sed '/pattern/command'

sed '/ERROR/d' app.log          # Delete ERROR lines
sed '/^#/d' config.ini          # Delete comment lines
sed '/^$/d' file.txt            # Delete blank lines
sed '/START/,/END/d' file.txt   # Delete from START to END (inclusive)
```

---

### 5.3 Range Address

[↑ Back to TOC](#table-of-contents)

```bash
# Line range
sed '5,20s/foo/bar/' file.txt

# Regex range — from match1 to match2
sed '/BEGIN DATA/,/END DATA/p' file.txt

# From line 5 to first match of pattern
sed '5,/ERROR/d' file.txt

# First match to end of file
sed '/HEADER/,$p' file.txt
```

---

### 5.4 Step Address (GNU sed)

[↑ Back to TOC](#table-of-contents)

`first~step` — match every Nth line starting from `first`.

```bash
# Every other line (even lines)
sed -n '0~2p' file.txt

# Every 3rd line starting from line 1
sed -n '1~3p' file.txt

# Delete every 2nd line
sed '0~2d' file.txt
```

---

### 5.5 Negation with `!`

[↑ Back to TOC](#table-of-contents)

```bash
# Apply command to all lines EXCEPT those matching
sed '/ERROR/!d' app.log           # Keep only ERROR lines (delete all non-ERROR)
sed '/^#/!s/$/;/' config.ini      # Add semicolon to end of non-comment lines
sed '1!G; h; $p' file.txt         # Classic reverse-file one-liner
```

---

## 6. Flags & Options

[↑ Back to TOC](#table-of-contents)

| Flag | Meaning | Example |
|---|---|---|
| `-n` | Suppress default output (silent mode) | `sed -n '/ERROR/p'` |
| `-e` | Add an expression (multiple commands) | `sed -e 's/a/b/' -e 's/c/d/'` |
| `-f FILE` | Read commands from script file | `sed -f rules.sed` |
| `-i` | Edit file in-place | `sed -i 's/v1/v2/' config.yml` |
| `-i.bak` | In-place with backup | `sed -i.bak 's/v1/v2/' config.yml` |
| `-E` or `-r` | Extended Regular Expressions (ERE) | `sed -E 's/([0-9]+)/NUM/g'` |
| `--sandbox` | Disable file writes (GNU sed 4.5+) | `sed --sandbox 's/x/y/'` |

> ⚠️ **macOS note:** BSD `sed` (macOS default) requires a backup suffix with `-i`: `sed -i '' 's/foo/bar/' file.txt`  
> GNU sed (Linux): `sed -i 's/foo/bar/' file.txt`

---

## 7. Regex Basics in `sed`

[↑ Back to TOC](#table-of-contents)

---

### 7.1 BRE vs ERE

[↑ Back to TOC](#table-of-contents)

| Feature | BRE (default) | ERE (`-E`) |
|---|---|---|
| Grouping | `\(` `\)` | `(` `)` |
| Alternation | `\|` | `\|` |
| One or more | `\+` | `+` |
| Zero or one | `\?` | `?` |
| Any char | `.` | `.` |
| Character class | `[a-z]` | `[a-z]` |
| Anchors | `^` `$` | `^` `$` |

```bash
# BRE: must escape + and ()
sed 's/\([0-9]\+\)/NUM/g' file.txt

# ERE: cleaner syntax
sed -E 's/([0-9]+)/NUM/g' file.txt
```

---

### 7.2 Capture Groups and Back-References

[↑ Back to TOC](#table-of-contents)

Back-references let you reuse matched groups in the replacement string.

```bash
# Swap first and last name (BRE)
echo "Smith John" | sed 's/\([A-Za-z]*\) \([A-Za-z]*\)/\2 \1/'
# Output: John Smith

# Same with ERE
echo "Smith John" | sed -E 's/([A-Za-z]+) ([A-Za-z]+)/\2 \1/'

# Add quotes around a value
sed 's/=\(.*\)/="\1"/' config.properties

# Extract just the IP from a log line
echo "2024-01-15 10:23:11 client 192.168.1.105 connected" | \
  sed -E 's/.*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*/\1/'
```

---

### 7.3 Common Patterns

[↑ Back to TOC](#table-of-contents)

| Pattern | Matches |
|---|---|
| `^` | Start of line |
| `$` | End of line |
| `.` | Any single character |
| `.*` | Zero or more of any char (greedy) |
| `[0-9]` | Any digit |
| `[a-zA-Z]` | Any letter |
| `[[:digit:]]` | POSIX digit class |
| `[[:space:]]` | Space, tab, etc. |
| `[[:upper:]]` | Uppercase letters |
| `\b` | Word boundary (GNU sed ERE) |
| `\t` | Tab character |
| `\n` | Newline (in Pattern Space after `N`) |

```bash
# Trim leading whitespace
sed 's/^[[:space:]]*//' file.txt

# Trim trailing whitespace
sed 's/[[:space:]]*$//' file.txt

# Trim both
sed 's/^[[:space:]]*//; s/[[:space:]]*$//' file.txt

# Remove all blank lines
sed '/^[[:space:]]*$/d' file.txt
```

---

## 8. In-Place Editing — The `-i` Flag

[↑ Back to TOC](#table-of-contents)

`-i` makes `sed` edit the file directly, replacing its contents. **This is irreversible without a backup.**

```bash
# In-place edit — Linux/GNU sed
sed -i 's/v1\.0/v2\.0/g' config.yml

# In-place with backup (.bak suffix)
sed -i.bak 's/v1\.0/v2\.0/g' config.yml

# In-place — macOS BSD sed (requires empty string argument)
sed -i '' 's/v1\.0/v2\.0/g' config.yml

# Cross-platform safe pattern (always make a backup)
cp config.yml config.yml.bak && sed -i 's/v1\.0/v2\.0/g' config.yml

# In-place edit on multiple files
sed -i 's/localhost/prod-db-host/g' *.properties

# In-place edit across a directory tree
find /etc/myapp -name "*.conf" -exec sed -i 's/staging/production/g' {} \;
```

> ⚠️ **Production rule:** Always use `-i.bak` or take a backup before in-place editing in production environments.

---

## 9. Delimiters — Not Just `/`

[↑ Back to TOC](#table-of-contents)

You can use **any character** as the delimiter after `s`. This avoids the "leaning toothpick" problem when your pattern or replacement contains forward slashes.

```bash
# Problem: URLs contain /  — escaping is ugly
sed 's/http:\/\/old\.example\.com/http:\/\/new\.example\.com/g' urls.txt

# Solution: use a different delimiter
sed 's|http://old.example.com|http://new.example.com|g' urls.txt

# Using # as delimiter (common in path substitutions)
sed 's#/old/path#/new/path#g' paths.txt

# Using @ as delimiter
sed 's@/data/raw@/data/processed@g' pipeline.sh

# Even works with addresses
sed '\|/var/log/app|d' paths.txt
```

---

## 10. Multi-line Operations

[↑ Back to TOC](#table-of-contents)

By default, `sed` works on one line at a time. These commands let you work across line boundaries.

| Command | Action |
|---|---|
| `N` | Append next line to Pattern Space with `\n` |
| `P` | Print up to first `\n` in Pattern Space |
| `D` | Delete up to first `\n`, restart cycle |

```bash
# Join lines that end with backslash continuation
sed -E ':a; /\\$/N; s/\\\n//; ta' file.txt

# Replace newline between two specific patterns
sed '/OPEN/{N; s/OPEN\n/OPEN /}' file.txt

# Delete blank lines between paragraphs (collapse to single blank)
sed '/^$/{N; /^\n$/d}' file.txt

# Collapse two-line entries into one (CSV repair)
sed 'N; s/\n/,/' file.txt

# Match pattern spanning two lines
sed -n '/START/{N; /START.*END/p}' file.txt
```

---

## 11. Practical Examples Library

[↑ Back to TOC](#table-of-contents)

---

### 11.1 Text Substitution

[↑ Back to TOC](#table-of-contents)

```bash
# Simple word replacement
sed 's/foo/bar/g' file.txt

# Case-insensitive replacement (GNU sed)
sed 's/error/ERROR/gI' app.log

# Replace only whole words (word boundary)
sed -E 's/\berror\b/ERROR/g' app.log

# Replace from 2nd occurrence onward
sed 's/foo/bar/2g' file.txt

# Substitute on specific line range only
sed '10,50s/old/new/g' file.txt

# Substitute only on lines matching a pattern
sed '/^data_/s/null/NULL/g' data.sql

# Replace text between delimiters
echo "VALUE=old_setting" | sed 's/=.*/=new_setting/'

# Convert tabs to spaces
sed 's/\t/    /g' file.txt

# Escape special chars in replacement
sed 's/&/\&amp;/g' file.html
```

---

### 11.2 Line Operations

[↑ Back to TOC](#table-of-contents)

```bash
# Print specific line (line 42)
sed -n '42p' file.txt

# Print range (lines 10–20)
sed -n '10,20p' file.txt

# Print between two patterns (inclusive)
sed -n '/START/,/END/p' file.txt

# Delete header line (line 1)
sed '1d' data.csv

# Delete last line
sed '$d' file.txt

# Delete blank lines
sed '/^$/d' file.txt

# Delete comment lines
sed '/^#/d; /^;/d' config.ini

# Add line number prefix to every line
sed = file.txt | sed 'N; s/\n/\t/'

# Print total line count (faster than wc -l for pipelines)
sed -n '$=' file.txt

# Reverse line order (tac)
sed -n '1!G; h; $p' file.txt

# Remove duplicate consecutive lines (uniq equivalent)
sed '$!N; /^\(.*\)\n\1$/!P; D' file.txt
```

---

### 11.3 Extracting Data

[↑ Back to TOC](#table-of-contents)

```bash
# Extract lines between two patterns (exclusive)
sed -n '/START/{n; /END/!p}' file.txt

# Extract value after "=" key=value format
sed -n 's/^server=//p' config.properties

# Extract lines matching a pattern to another file
sed -n '/ERROR/w errors.log' app.log

# Extract first 100 lines
sed '100q' file.txt

# Extract last 10 lines (use tail; or for sed purism:)
sed -n -e :a -e '$p; N; 11,$D; ba' file.txt

# Extract unique first column (pipe to sort -u after)
sed 's/\(^[^,]*\).*/\1/' data.csv

# Extract IP addresses from log
sed -nE 's/.*([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*/\1/p' app.log
```

---

### 11.4 Formatting & Cleanup

[↑ Back to TOC](#table-of-contents)

```bash
# Trim leading whitespace
sed 's/^[[:space:]]*//' file.txt

# Trim trailing whitespace
sed 's/[[:space:]]*$//' file.txt

# Trim both ends
sed 's/^[[:space:]]*//; s/[[:space:]]*$//' file.txt

# Collapse multiple spaces to single space
sed 's/  */ /g' file.txt

# Add blank line between paragraphs
sed '/^./{G}' file.txt

# Double-space a file
sed 'G' file.txt

# Remove HTML tags
sed 's/<[^>]*>//g' page.html

# Remove ANSI color codes from log output
sed 's/\x1b\[[0-9;]*m//g' colored.log

# Remove Windows line endings (CRLF → LF)
sed 's/\r//' file.txt
# OR
sed 's/\r$//' file.txt

# Convert Unix to DOS (add \r)
sed 's/$/'$'\r'/ file.txt
```

---

### 11.5 Config File Manipulation

[↑ Back to TOC](#table-of-contents)

```bash
# Uncomment a line
sed '/^#server=/s/^#//' config.properties

# Comment out a line
sed '/^server=/s/^/#/' config.properties

# Change a key's value
sed 's/^db\.host=.*/db.host=prod-server-01/' app.properties

# Add a new key after a specific line
sed '/^db\.port=/a db.pool.size=20' app.properties

# Enable a feature flag
sed 's/FEATURE_X=false/FEATURE_X=true/' feature-flags.env

# Change port number in nginx conf
sed 's/listen 8080/listen 80/g' nginx.conf

# Update version in pom.xml or package.json
sed -i 's/"version": "1\.0\.0"/"version": "1.1.0"/' package.json

# Replace a YAML value
sed 's/^\(\s*replicas:\s*\).*/\12/' deployment.yaml
```

---

## 12. Data Engineering Use Cases

[↑ Back to TOC](#table-of-contents)

---

### 12.1 ETL Pipeline Preprocessing

[↑ Back to TOC](#table-of-contents)

```bash
# Strip BOM (Byte Order Mark) from UTF-8 files before loading
sed -i '1s/^\xEF\xBB\xBF//' input.csv

# Normalize NULL strings to empty before CSV load
sed 's/\bNULL\b//g' raw_data.csv

# Remove header line before loading to DB
sed '1d' export.csv > import.csv

# Replace empty fields with a default value
sed 's/,,/,0,/g; s/,,/,0,/g' data.csv

# Convert pipe-delimited to comma-delimited
sed 's/|/,/g' data.psv > data.csv

# Strip enclosing double-quotes from all fields
sed 's/"//g' data.csv

# Normalize date format: MM/DD/YYYY → YYYY-MM-DD
echo "12/25/2024" | sed -E 's|([0-9]{2})/([0-9]{2})/([0-9]{4})|\3-\1-\2|'

# Remove rows where first field is empty (bad records)
sed '/^,/d' data.csv

# Add a header row to a file missing one
sed '1i id,name,value,timestamp' headerless_data.csv

# Lowercase all column values in a specific column positionally
# (limited — for complex column ops use awk)
sed 's/\(^[^,]*,[^,]*,\)\([^,]*\)/\1\L\2/' data.csv   # GNU sed \L
```

---

### 12.2 Schema & DDL Transformations

[↑ Back to TOC](#table-of-contents)

```bash
# Convert PostgreSQL CREATE TABLE to Redshift (remove SERIAL)
sed 's/SERIAL/INTEGER/g; s/BIGSERIAL/BIGINT/g' create_table.sql

# Convert MySQL backtick identifiers to double-quotes (ANSI SQL)
sed 's/`/"/g' mysql_schema.sql

# Strip schema prefix from table references
sed 's/public\.\([a-z_]*\)/\1/g' query.sql

# Change VARCHAR to VARCHAR2 (Oracle migration)
sed 's/VARCHAR(/VARCHAR2(/g' create_table.sql

# Add IF NOT EXISTS to all CREATE TABLE statements
sed 's/CREATE TABLE /CREATE TABLE IF NOT EXISTS /g' schema.sql

# Extract table names from DDL
sed -nE 's/CREATE TABLE .*?([a-z_]+) \(.*/\1/p' schema.sql

# Rename a column across a SQL file
sed 's/\bcreated_at\b/created_timestamp/g' queries.sql

# Convert CTAS to INSERT INTO ... SELECT
sed 's/CREATE TABLE \([^ ]*\) AS/INSERT INTO \1/' etl.sql
```

---

### 12.3 Log File Processing

[↑ Back to TOC](#table-of-contents)

```bash
# Extract only ERROR and FATAL lines
sed -n '/\(ERROR\|FATAL\)/p' app.log

# Filter logs from a specific date
sed -n '/^2024-01-15/p' app.log

# Extract lines in a time range
sed -n '/10:00:00/,/11:00:00/p' app.log

# Remove DEBUG lines to reduce noise
sed '/DEBUG/d' verbose.log

# Extract stack traces (lines starting with whitespace after EXCEPTION)
sed -n '/Exception/{:a; p; n; /^\s/ba}' app.log

# Count occurrences of a pattern (pipeline)
sed -n '/ERROR/p' app.log | wc -l

# Strip log timestamps for diff comparison
sed 's/^[0-9\-]\{10\} [0-9:]\{8\} //' app.log

# Extract transaction IDs
sed -nE 's/.*txId=([A-F0-9]+).*/\1/p' app.log

# Parse Splunk-style key=value logs and extract a field
sed -nE 's/.*duration=([0-9]+).*/\1/p' app.log

# Rotate / trim log file to last N lines in-place
sed -i -n '1000,$p' app.log
```

---

### 12.4 CSV / Delimited File Manipulation

[↑ Back to TOC](#table-of-contents)

```bash
# Extract only columns 1 and 3 (sed approach — awk better for complex cases)
sed -E 's/^([^,]+),[^,]+,([^,]+).*/\1,\2/' data.csv

# Change delimiter from comma to tab
sed 's/,/\t/g' data.csv > data.tsv

# Quote all fields
sed 's/[^,]*/\"&\"/g' data.csv

# Remove quotes from a quoted CSV
sed 's/"//g' data.csv

# Skip the header and process only data rows
sed '1d' data.csv | sed 's/old/new/g'

# Insert a constant new column at the end of every row
sed 's/$/,2024-01-15/' data.csv

# Replace a specific column value conditionally
# If column 3 is "NULL", replace with 0
sed -E 's/^(([^,]+,){2})NULL(.*)/\10\3/' data.csv

# Validate: print rows with wrong number of commas (should be 4 fields = 3 commas)
sed -n '/^\([^,]*,\)\{3\}[^,]*$/!p' data.csv
```

---

### 12.5 Environment & Config Management

[↑ Back to TOC](#table-of-contents)

```bash
# Update .env file variable
sed -i 's/^DB_HOST=.*/DB_HOST=prod-db-01/' .env

# Generate environment-specific config from a template
sed 's/__ENV__/production/g; s/__DB__/prod-db-01/g' app.conf.template > app.conf

# Promote staging config to prod
sed -e 's/staging/production/g' \
    -e 's/stg-db/prd-db/g' \
    -e 's/8080/80/g' \
    staging.conf > production.conf

# Inject secrets from environment (used in CI/CD startup scripts)
sed "s/__SECRET__/${MY_SECRET}/" config.template > config.yaml

# Set Kubernetes replica count dynamically in pipeline
sed -i "s/replicas: .*/replicas: ${REPLICAS}/" k8s/deployment.yaml

# Enable TLS in a config
sed -i 's/ssl=false/ssl=true/; s/port=5432/port=5433/' db.conf
```

---

### 12.6 Batch File Operations

[↑ Back to TOC](#table-of-contents)

```bash
# Replace a string across all SQL files in a directory
find ./sql -name "*.sql" -exec sed -i 's/old_schema/new_schema/g' {} \;

# Add file header comment to all Python files
find . -name "*.py" -exec sed -i '1i\# Auto-generated. Do not edit manually.' {} \;

# Remove trailing whitespace from all files
find . -name "*.txt" -exec sed -i 's/[[:space:]]*$//' {} \;

# Rename a function across a codebase (in-place)
find . -name "*.py" -exec sed -i 's/get_user_data/fetch_user_profile/g' {} \;

# Mass update version strings
find . -name "*.yaml" | xargs sed -i 's/image: myapp:1\.2\.3/image: myapp:1.2.4/g'
```

---

## 13. Production Support Use Cases

[↑ Back to TOC](#table-of-contents)

---

### 13.1 Incident Triage — Log Filtering

[↑ Back to TOC](#table-of-contents)

```bash
# SITUATION: App is down, you need to find the first ERROR fast
sed -n '/ERROR/{p;q}' /var/log/myapp/app.log

# Get last 500 lines, filter ERRORs only
tail -500 app.log | sed -n '/ERROR\|FATAL/p'

# Look for OOM kill or crash signals in syslog
sed -n '/Out of memory\|Killed process/p' /var/log/syslog

# Count ERRORs in the last hour by extracting log lines with current hour
HOUR=$(date +%H)
sed -n "/$(date +%Y-%m-%d) ${HOUR}:/p" app.log | grep -c ERROR

# Strip noise from logs (DEBUG + INFO lines) for faster scan
sed '/DEBUG/d; /INFO/d' app.log | less

# Find all unique error messages (normalize dynamic IDs first)
sed -n '/ERROR/p' app.log | \
  sed -E 's/txId=[A-F0-9]+/txId=XXX/g; s/userId=[0-9]+/userId=NNN/g' | \
  sort -u

# Extract a specific request ID's full trace
REQUEST_ID="abc-123"
sed -n "/${REQUEST_ID}/p" app.log
```

---

### 13.2 Masking Sensitive Data

[↑ Back to TOC](#table-of-contents)

```bash
# Mask Social Security Numbers  XXX-XX-XXXX
sed -E 's/[0-9]{3}-[0-9]{2}-[0-9]{4}/XXX-XX-XXXX/g' logs.txt

# Mask credit card numbers (16 digits, optionally grouped)
sed -E 's/[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}[ -]?[0-9]{4}/XXXX-XXXX-XXXX-XXXX/g' data.txt

# Mask email addresses
sed -E 's/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/REDACTED@EMAIL/g' logs.txt

# Mask IP addresses
sed -E 's/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/X.X.X.X/g' access.log

# Mask passwords in config files before sharing
sed 's/password=.*/password=REDACTED/' app.properties

# Mask API keys / tokens (common formats)
sed -E 's/[Aa]pi[_-]?[Kk]ey[[:space:]]*=[[:space:]]*[^ ]*/API_KEY=REDACTED/g' config.env
sed -E 's/Bearer [A-Za-z0-9\._\-]+/Bearer REDACTED/g' http.log

# Mask AWS access keys
sed -E 's/AKIA[0-9A-Z]{16}/AWS_KEY_REDACTED/g' deploy.log
```

---

### 13.3 Hotfix Deployments

[↑ Back to TOC](#table-of-contents)

```bash
# SITUATION: Need to update config on 20 servers in a hurry

# 1. Test the change first (no -i)
sed 's/max_connections=100/max_connections=200/' db.conf

# 2. Apply with backup
sed -i.bak "$(date +%Y%m%d)" 's/max_connections=100/max_connections=200/' db.conf

# 3. Verify the change took effect
grep max_connections db.conf

# 4. Rollback if needed
mv db.conf.20240115 db.conf

# Update Docker image tag in deployment manifest
sed -i "s|image: myapp:.*|image: myapp:${NEW_TAG}|" k8s/deployment.yaml

# Disable a feature flag emergency toggle
sed -i 's/CIRCUIT_BREAKER_ENABLED=true/CIRCUIT_BREAKER_ENABLED=false/' feature.flags

# Comment out a bad cron job entry
sed -i 's|^\(0 2 \* \* \* /scripts/bad_job.sh\)|#\1|' /etc/crontab

# Fix a bad DSN connection string across config files
find /etc/myapp -name "*.conf" \
  -exec sed -i 's/old-db-host\.internal/new-db-host\.internal/g' {} \;
```

---

### 13.4 Redacting PII Before Sharing Logs

[↑ Back to TOC](#table-of-contents)

```bash
# Full PII scrub pipeline — chain multiple sed expressions
cat app.log \
  | sed -E 's/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[EMAIL]/g' \
  | sed -E 's/[0-9]{3}-[0-9]{2}-[0-9]{4}/[SSN]/g' \
  | sed -E 's/[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[IP]/g' \
  | sed -E 's/"password":"[^"]*"/"password":"[REDACTED]"/g' \
  > sanitized_app.log

# Create a reusable PII scrub script file: pii_scrub.sed
cat > pii_scrub.sed << 'EOF'
# Emails
s/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/[EMAIL]/g
# SSNs
s/[0-9]{3}-[0-9]{2}-[0-9]{4}/[SSN]/g
# Credit Cards
s/[0-9]{4}[ -][0-9]{4}[ -][0-9]{4}[ -][0-9]{4}/[CC]/g
# Phone numbers
s/\+?[0-9]{1,3}[-. ]?\(?[0-9]{3}\)?[-. ]?[0-9]{3}[-. ]?[0-9]{4}/[PHONE]/g
EOF

# Apply it with ERE mode
sed -E -f pii_scrub.sed raw.log > clean.log
```

---

## 14. `sed` in Shell Scripts & Pipelines

[↑ Back to TOC](#table-of-contents)

```bash
# Extract config value in a bash script
DB_HOST=$(sed -n 's/^db\.host=//p' app.properties)
echo "Connecting to: ${DB_HOST}"

# Use sed output as a variable
VERSION=$(sed -n 's/^version=//p' build.properties)
echo "Building version: ${VERSION}"

# sed as a step in a data pipeline
cat raw_data.csv \
  | sed '1d' \                          # Remove header
  | sed '/^$/d' \                       # Remove blanks
  | sed 's/\r//' \                      # Fix Windows line endings
  | sed 's/NULL//g' \                   # Normalize NULLs
  | awk -F',' '{print $1,$3,$5}' \      # Select columns
  > processed_data.txt

# Template rendering at deploy time
sed \
  -e "s/__APP_VERSION__/${APP_VERSION}/g" \
  -e "s/__DB_HOST__/${DB_HOST}/g" \
  -e "s/__ENV__/${ENVIRONMENT}/g" \
  app-config.template.yaml > app-config.yaml

# Validate output before applying (dry-run pattern)
EXPECTED="db.host=prod-db-01"
RESULT=$(sed -n 's/^db\.host=//p' app.properties | sed 's/^/db.host=/')
if [[ "${RESULT}" == "${EXPECTED}" ]]; then
    echo "Config OK"
else
    echo "Config mismatch: ${RESULT}"
    exit 1
fi
```

---

## 15. `sed` vs. Other Tools — When to Use What

[↑ Back to TOC](#table-of-contents)

| Task | Best Tool | Why |
|---|---|---|
| Simple find & replace | **`sed`** | One-liner, no overhead |
| Column extraction | **`awk`** | Handles fields natively |
| Complex multi-condition transforms | **`awk`** | Has variables and math |
| Sorting lines | **`sort`** | Built for it |
| Unique lines | **`sort -u` / `uniq`** | Built for it |
| Pattern search only (no transform) | **`grep`** | Faster, simpler |
| JSON manipulation | **`jq`** | Regex on JSON is fragile |
| Large-scale structured data | **Python/pandas** | Type-aware, testable |
| Multi-file search + replace (IDE) | **`find` + `sed`** | Scriptable, no GUI needed |
| Character-by-character translation | **`tr`** or `sed y//` | Both work |
| Binary files | **`dd`**, `xxd` | `sed` is line-text only |

**Rule of thumb:**
- `sed` = transform/edit the *stream* (substitution, line ops)
- `awk` = compute/aggregate the *fields* (column math, conditionals)
- `grep` = *find* (no transform needed)
- `python` = *complex logic* (multi-pass, types, modules)

---

## 16. Common Pitfalls & Gotchas

[↑ Back to TOC](#table-of-contents)

```bash
# PITFALL 1: Greedy matching grabs too much
echo "START middle END" | sed 's/START.*END/REPLACED/'
# Output: REPLACED  (correct here, but can destroy unintended parts of line)

# FIX: Use [^E]* or be specific with your pattern
echo "START1 middle END1 and START2 END2" | sed 's/START[^ ]*/REPLACED/g'

# PITFALL 2: Forgetting -n makes sed print everything
sed '/ERROR/p' app.log      # prints ALL lines + ERROR lines twice
sed -n '/ERROR/p' app.log   # prints ONLY error lines

# PITFALL 3: In-place -i without backup
sed -i 's/foo/bar/' important.conf   # No backup! Data loss risk
sed -i.bak 's/foo/bar/' important.conf   # SAFE — creates important.conf.bak

# PITFALL 4: macOS BSD sed vs GNU sed
sed -i 's/foo/bar/' file.txt        # Works on Linux GNU sed
sed -i '' 's/foo/bar/' file.txt     # Required on macOS BSD sed
# Cross-platform fix: use gsed on macOS (brew install gnu-sed)

# PITFALL 5: Special characters in replacement string
# & means "the matched text" in replacement
echo "hello" | sed 's/hello/&world/'   # Output: helloworld (& = hello)
echo "hello" | sed 's/hello/\&world/'  # Output: &world (escaped &)

# PITFALL 6: Newlines in patterns
sed 's/\n/ /' file.txt   # Does NOT work — pattern space has no \n
# Use N to load two lines into pattern space first
sed 'N; s/\n/ /' file.txt  # Works

# PITFALL 7: Regex special chars in the search pattern
# Dots, slashes, brackets must be escaped
sed 's/192.168.1.1/REDACTED/'    # . matches ANY char — wrong
sed 's/192\.168\.1\.1/REDACTED/' # Correct — escape the dots

# PITFALL 8: CRLF line endings (Windows files)
# sed on Linux won't match $ correctly with \r\n files
sed 's/value$/new/'     # May not match if line ends with \r
sed 's/\r//' file.txt   # Strip \r first, then process

# PITFALL 9: Empty pattern reuses last regex
sed -n '/ERROR/ { s//[ERROR]/p }' app.log   # Empty s// reuses /ERROR/
# Output: [ERROR] lines with ERROR replaced by [ERROR]
```

---

## 17. Quick Reference Cheat Sheet

[↑ Back to TOC](#table-of-contents)

### Commands

| Command | Description |
|---|---|
| `s/PAT/REP/` | Substitute (1st match per line) |
| `s/PAT/REP/g` | Substitute all matches per line |
| `s/PAT/REP/2` | Substitute 2nd match only |
| `s/PAT/REP/I` | Case-insensitive substitute |
| `d` | Delete line |
| `p` | Print line (use with `-n`) |
| `q` | Quit after current line |
| `Q` | Quit without printing |
| `i\TEXT` | Insert TEXT before line |
| `a\TEXT` | Append TEXT after line |
| `c\TEXT` | Replace line with TEXT |
| `y/SRC/DST/` | Translate chars |
| `=` | Print line number |
| `r FILE` | Read file and insert |
| `w FILE` | Write line to file |
| `N` | Append next line to Pattern Space |
| `P` | Print first line of Pattern Space |
| `D` | Delete first line, restart cycle |
| `h` | Copy Pattern → Hold |
| `H` | Append Pattern → Hold |
| `g` | Copy Hold → Pattern |
| `G` | Append Hold → Pattern |
| `x` | Exchange Pattern and Hold |
| `b LABEL` | Branch to label |
| `t LABEL` | Branch if substitution made |
| `:LABEL` | Define a label |

### Options

| Option | Description |
|---|---|
| `-n` | Suppress default output |
| `-e CMD` | Add command expression |
| `-f FILE` | Read script from file |
| `-i[.EXT]` | In-place edit (optional backup) |
| `-E` or `-r` | Use Extended Regex (ERE) |

### Address Syntax

| Address | Matches |
|---|---|
| `N` | Line N |
| `$` | Last line |
| `/regex/` | Lines matching regex |
| `N,M` | Lines N through M |
| `/A/,/B/` | From line matching A to line matching B |
| `N~S` | Every Sth line starting at N |
| `ADDR!` | Negate — all lines NOT matching ADDR |

### Substitution Flags

| Flag | Meaning |
|---|---|
| `g` | Global (all matches per line) |
| `N` (number) | Replace Nth match |
| `I` | Case-insensitive |
| `p` | Print if substitution was made |
| `w FILE` | Write to file if substitution was made |

### Replacement Special Characters

| Char | Meaning |
|---|---|
| `&` | The entire matched text |
| `\1` … `\9` | Capture group back-reference |
| `\n` | Newline |
| `\L` | Lowercase following text (GNU) |
| `\U` | Uppercase following text (GNU) |
| `\E` | End `\L`/`\U` transformation (GNU) |

---

*Guide version 1.0 — Built for Staff/Principal Data Engineers working in Linux, ETL, and production environments.*  
*"Simplicity and clarity is Gold."*
