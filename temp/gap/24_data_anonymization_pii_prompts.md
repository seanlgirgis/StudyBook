# Data Anonymization & PII Masking — ChatGPT Project Prompts

Priority: 🔴 Critical — financial services, healthcare, and any regulated industry requires this

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Anonymization and PII Masking for Data Engineers
Slug: data-anonymization-pii

Extra coverage required:
- PII definition — direct identifiers (name, SSN, email, phone) vs quasi-identifiers (age, ZIP, gender) that enable re-identification when combined
- Regulatory landscape — GDPR (EU, right to erasure, explicit consent), CCPA (California consumer rights), HIPAA (PHI in healthcare), PCI-DSS (cardholder data); what each demands from pipelines
- Anonymization vs pseudonymization — pseudonymization replaces identifiers with tokens but is reversible; anonymization is irreversible; GDPR treats them very differently
- Tokenization — replace a sensitive value with a random token stored in a vault; reversible only with vault access; format-preserving tokenization keeps column format intact
- Masking strategies — full masking (redact all), partial masking (show last 4 digits), format-preserving masking (fake SSN with valid format), consistent masking (same input → same output across tables)
- Hashing for anonymization — SHA-256 of PII is not safe without a salt; rainbow table attacks; salted hashing with per-record salt makes reversal computationally infeasible
- Data generalization — reduce precision to reduce re-identification risk: exact age → age range, full ZIP → 3-digit ZIP, timestamp → date; trades analytical value for privacy
- k-anonymity — a record is k-anonymous if it is indistinguishable from at least k-1 other records on quasi-identifiers; suppression or generalization to achieve it
- Differential privacy — add calibrated statistical noise to aggregate query results; epsilon controls privacy/accuracy trade-off; used in census data and ML training
- PII detection in pipelines — Microsoft Presidio and regex patterns to scan incoming data; tag PII columns at ingestion; transform before storing, not after
- Right to erasure — the engineering challenge: deleting one person's data from immutable Parquet partitions, Kafka topics, and backup snapshots; partition by user_id enables targeted deletes
- Anonymization for dev/test environments — never copy production PII to non-production; generate anonymized replicas; synthetic data as an alternative
- Audit logging for PII access — log who accessed which sensitive columns, when, and from which system; required for HIPAA and PCI compliance evidence

SCOPE FENCE:
- Target 12–16 HOST/SEAN exchanges total
- Each bullet = at most one exchange
- SEAN answers: 3–5 sentences max, no monologues
- Merge the least distinct bullets if the list runs long
- Do NOT elaborate into a textbook — this feeds a reference audio script
```

Run pipeline after saving the script:
```
run_mission_audio.ps1 -Slug data-anonymization-pii -ChunkSize 750
```

Upload final_data-anonymization-pii.mp3 to R2, then run Project 2.

---

## Project 2 — HTML Page

Run after `final_data-anonymization-pii.mp3` is live on R2.

```
Topic: Data Anonymization and PII Masking for Data Engineers
Slug: data-anonymization-pii
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_data-anonymization-pii.mp3
Today's date: 2026-04-25

SCOPE FENCE:
- Create exactly these sections, in this order:
  1. PII Definition — direct vs quasi-identifiers
  2. Regulatory Landscape — GDPR, CCPA, HIPAA, PCI-DSS
  3. Anonymization vs Pseudonymization
  4. Tokenization & Masking Strategies
  5. Hashing for Anonymization — salting & rainbow tables
  6. Data Generalization & k-Anonymity
  7. Differential Privacy
  8. PII Detection & Transformation in Pipelines
  9. Right to Erasure, Dev Environments & Audit Logging
  10. Interview Q&A — 6 realistic senior-level pairs
  11. Quick Reference — 12–15 rows
- Per section: 2–3 tight paragraphs, one code block max (20 lines)
- No step-by-step tutorials, no full worked examples
- Cheat sheet rows must each earn their place — no padding

Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\data-anonymization-pii.html
