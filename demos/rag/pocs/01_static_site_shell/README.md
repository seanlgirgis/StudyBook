# 01_static_site_shell

## Purpose
Build a synthetic, static website shell for a fake home-services business and include a floating chat widget entry point for future AI workflow integration.

## Files
- `website/index.html`: synthetic business landing page and chat widget markup
- `website/assets/styles.css`: layout, section, and chat widget styles
- `website/assets/chat-widget.js`: open/close behavior and placeholder chat responses
- `notes/what_this_teaches.md`: learning notes for this milestone
- `notes/questions.md`: review questions after manual walkthrough

## How To Run
1. Open `website/index.html` in a browser.
2. Scroll through each section to verify layout and copy.
3. Click the floating chat button in the bottom-right corner.
4. Send a message to confirm the placeholder assistant response appears.

## What This Teaches
- How to ship a low-risk UI shell before any backend dependency exists.
- How to define chat interaction expectations using static placeholders.
- How to create a milestone-ready artifact that can later connect to FastAPI/RAG.

## What Is Intentionally Not Included
- No backend service calls
- No FastAPI integration
- No RAG logic or retrieval pipeline
- No AI API keys or model calls
- No deployment or AWS setup

## Next Step
Implement `pocs/02_job_search_rag` only when Milestone 1 review is approved.
