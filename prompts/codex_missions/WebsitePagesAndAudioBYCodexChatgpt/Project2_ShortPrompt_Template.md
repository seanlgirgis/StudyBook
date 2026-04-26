# Project 2 Short Prompt Template (Fast Method)

Use this with ChatGPT Project 2 after `AGENTS.md` and `learning/_page-template.html` are in the website repo.

## Prompt

```md
Generate a complete learning page using the repo rules in `AGENTS.md` and the CSS/page shell in `learning/_page-template.html`.

Topic: {TOPIC}
Slug: {SLUG}
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_{SLUG}.mp3
Output path: learning/{SLUG}.html

Audience:
Senior Data Engineer interview prep.

Emphasize:
- {EMPHASIS_1}
- {EMPHASIS_2}
- {EMPHASIS_3}
- {EMPHASIS_4}
- {EMPHASIS_5}
- {EMPHASIS_6}
- {EMPHASIS_7}
- {EMPHASIS_8}
- {EMPHASIS_9}
- Interview-focused Q&A and quick-reference entries

Acceptance checks:
- HTML file exists at output path
- Audio source matches the provided URL
- No `<video>` tag
- `.cheat-row` remains `170px 1fr`
- No mojibake tokens
- 8-10 content sections
- Exactly 6 Q&A pairs
- 10-16 cheat rows
- Ends with: `PAGE COMPLETE - {SLUG}.html - [N] sections - 6 QA pairs - [N] cheat rows - audio src confirmed`
```

## Example

```md
Generate a complete learning page using the repo rules in `AGENTS.md` and the CSS/page shell in `learning/_page-template.html`.

Topic: AWS EventBridge
Slug: aws-eventbridge
Audio URL: https://pub-174bd65326be4562b4618ccf6a4a8864.r2.dev/final_aws-eventbridge.mp3
Output path: learning/aws-eventbridge.html

Audience:
Senior Data Engineer interview prep.

Emphasize:
- EventBridge architecture and event flow
- Rule design and event pattern precision
- Scheduler use cases and limitations
- Integration patterns with Lambda, Step Functions, SQS/SNS
- Cross-account event bus strategy
- Failure handling, retries, DLQ, replay/idempotency patterns
- Security/governance and permissions boundaries
- Monitoring/observability and troubleshooting
- Cost and scale tradeoffs
- Interview-focused Q&A and quick-reference entries

Acceptance checks:
- HTML file exists at output path
- Audio source matches the provided URL
- No `<video>` tag
- `.cheat-row` remains `170px 1fr`
- No mojibake tokens
- 8-10 content sections
- Exactly 6 Q&A pairs
- 10-16 cheat rows
- Ends with: `PAGE COMPLETE - aws-eventbridge.html - [N] sections - 6 QA pairs - [N] cheat rows - audio src confirmed`
```
