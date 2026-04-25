# Data Anonymization & PII Masking — ChatGPT Project Prompts

Priority: 🔴 Critical — financial services, healthcare, and any regulated industry requires this

---

## Project 1 — Audio Script

Paste into ChatGPT Project 1 (Audio Script Writer).

```
Topic: Data Anonymization and PII Masking for Data Engineers
Slug: data-anonymization-pii
Extra coverage required: PII definition — what counts as personally identifiable information, direct identifiers vs quasi-identifiers,
regulatory landscape — GDPR, CCPA, HIPAA, PCI-DSS — what each requires from a data engineering perspective,
anonymization vs pseudonymization — the legal and technical distinction, why pseudonymization is not anonymization under GDPR,
tokenization — replacing a sensitive value with a non-sensitive token, the token vault, reversible vs irreversible,
masking strategies — full masking, partial masking (last 4 digits), format-preserving masking, consistent masking across tables,
hashing for anonymization — SHA-256, salted hashing, why unsalted hashing of PII is not safe (rainbow tables),
data generalization — reducing precision (exact age → age range, full ZIP → 3-digit ZIP) to reduce re-identification risk,
k-anonymity — what it means for a record to be indistinguishable from k-1 others, the suppression trade-off,
differential privacy — adding calibrated noise to aggregate queries, epsilon parameter, the trade-off between privacy and accuracy,
PII in pipelines — detection (presidio, regex patterns), transformation at ingestion, not storing what you don't need,
synthetic data as an alternative to anonymization — generating statistically realistic but entirely fake datasets,
data classification — tagging columns as PII, sensitive, internal, public — the metadata governance layer,
right to erasure (right to be forgotten) — the engineering challenge of deleting one person's data from a data lake,
anonymization in dev and test environments — why you must never copy production PII to non-production, anonymized replicas,
audit logging for PII access — who accessed what sensitive data when, compliance evidence,
real scenario: handling server ownership and departmental data in the Citi pipeline — what's sensitive, what needs masking.

SCOPE FENCE: Target 12-16 HOST/SEAN exchanges total. Each bullet above = at most
one exchange. SEAN answers: 3-5 sentences maximum, no monologues. If the bullet list
has more items than exchanges, merge the least distinct ones. Do not elaborate into
a textbook - this feeds a reference audio script, not a lecture series.
```\r\n\r\nRun pipeline after saving the script:
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

SCOPE FENCE: 8-10 sections maximum. 2-3 tight paragraphs per section.
One code block per section, 20 lines max. Cheat sheet: 12-15 rows.
Reference page only - no step-by-step tutorials or full worked examples.
Generate the complete HTML page.
```

Save output to:
D:\StudyBook\temp\seanlgirgis.github.io\learning\data-anonymization-pii.html
