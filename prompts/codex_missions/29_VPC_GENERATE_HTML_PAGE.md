# MISSION 29 — Generate HTML Page: AWS VPC
# Working directory: D:\StudyBook\
# Output: temp\seanlgirgis.github.io\learning\aws-vpc.html (new file)
# Prerequisite: Mission 28 complete and audio uploaded/confirmed

---

## WORKING DIRECTORY REMINDER

```powershell
Get-Location   # must show D:\StudyBook
```
All paths are relative to D:\StudyBook\. Use no absolute paths.

---

## STOP — CONFIRM AUDIO URL BEFORE WRITING HTML

Required audio URL:
`https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-vpc.mp3`

If upload is not confirmed live, STOP and report:
`Waiting for R2 upload confirmation.`

Source-of-truth generated file location:
`C:\temp\studybook_audio\aws-vpc\final_aws-vpc.mp3`

---

## YOUR TASK

Create a full new learning page:
`temp\seanlgirgis.github.io\learning\aws-vpc.html`

Use `temp\seanlgirgis.github.io\learning\aws-ec2.html` as the structural + CSS reference.

This is a NEW page, not a patch.

---

## NON-NEGOTIABLE CSS/STRUCTURE RULES

- Keep the same CSS framework and class structure as existing learning pages.
- Ensure `.cheat-row` uses exactly:
  - `grid-template-columns: 170px 1fr`
- Include:
  - topnav
  - title + subtitle
  - tag row
  - audio box
  - TOC
  - section bodies
  - interview Q&A
  - quick-reference cheat sheet

---

## REQUIRED HEADER CONTENT

- `<title>AWS VPC - Master Engineering Reference | Sean Girgis</title>`
- canonical:
  - `https://seanlgirgis.github.io/learning/aws-vpc.html`
- subtitle:
  - `Engineering reference &middot; Senior Data Engineer &middot; Last updated 2026-04-24 &middot; 20-30 min read`

Topnav:
```html
<div class="topnav">
  <a href="https://seanlgirgis.github.io/#learning">&larr; Learning Hub</a> / AWS VPC - Master Engineering Reference
</div>
```

Tag row must include:
- AWS, VPC, Networking, Security, Route Tables, Subnets, Hybrid

Audio box must include:
- label: `&#127911; Audio Overview`
- source URL: `final_aws-vpc.mp3`
- type: `audio/mpeg`

---

## REQUIRED TOC + SECTION IDS

Create TOC entries and matching sections for:
- `s1` What VPC Is
- `s2` CIDR and Subnet Design
- `s3` Route Tables and Routing
- `s4` Internet Gateway and NAT Gateway
- `s5` Public and Private Subnets
- `s6` Security Groups vs NACLs
- `s7` VPC Endpoints
- `s8` VPC Peering and Transit Gateway
- `s9` Hybrid Connectivity
- `s10` DNS in VPC
- `s11` High Availability Patterns
- `s12` Common Mistakes
- `s13` Debugging Checklist
- `qa` Interview Q&A
- `cheat` Quick Reference

Each section includes:
- `<h2 id="sN">...`
- explanatory paragraphs
- at least one `.hi` or `.warn` callout
- back-to-top link using `&uarr;`

---

## INTERVIEW Q&A RULES

Create 6 realistic senior data engineering VPC Q&A pairs using:
- `.qa`
- `.qa-q`
- `.qa-a`

---

## QUICK REFERENCE RULES

Use `.cheat` container with multiple `.cheat-row` rows.
Include at minimum:
- VPC
- Subnet
- Route Table
- Internet Gateway
- NAT Gateway
- Security Group
- NACL
- VPC Endpoint (Gateway)
- VPC Endpoint (Interface)
- VPC Peering
- Transit Gateway
- VPN
- Direct Connect
- Private Hosted Zone

---

## ENCODING SAFETY (MANDATORY)

- Save UTF-8
- Use HTML entities for glyphs: `&larr;`, `&middot;`, `&uarr;`, `&#127911;`, `&amp;`
- Do not allow mojibake tokens: `�`, `Â`, `Ã`, `â`, `ï`, `ð`
- Prefer ASCII hyphens in subtitle and labels

---

## VERIFICATION COMMANDS

Run:

```powershell
Test-Path "temp\seanlgirgis.github.io\learning\aws-vpc.html"
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-vpc.html" -Pattern 'final_aws-vpc.mp3'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-vpc.html" -Pattern 'audio/mpeg'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-vpc.html" -Pattern '170px 1fr'
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-vpc.html" -Pattern 'id="s' | Measure-Object
Select-String -Path "temp\seanlgirgis.github.io\learning\aws-vpc.html" -Pattern 'Ã|â|ï|Â|ð|�'
```

Expected:
- file exists
- mp3 source found
- `audio/mpeg` found
- `170px 1fr` found
- 13 `s` section anchors present (`s1` to `s13`)
- no mojibake matches

Repo cleanliness guard (must be no matches):
```powershell
rg --files -g "*.mp3" -g "*.m4a" -g "*filelist.txt" temp\jobsearch\data\interview_prep\audio_prep\aws-vpc
```

Report:
- `MISSION 29 COMPLETE — aws-vpc.html created — [N] sections — [N] QA pairs — [N] cheat rows`
- or `MISSION 29 BLOCKED — [reason]`
