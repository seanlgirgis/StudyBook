# What This Teaches

## Website Shell Role
This POC creates a stable, reviewable front-end shell for a synthetic home-services business. It proves page structure, copy tone, and section completeness before any backend complexity is introduced.

## Chat Entry Point Role
The floating chat widget defines how users enter the support flow. Even with placeholder responses, it validates open/close behavior, message capture, and expected user interaction patterns for later milestones.

## Why This Comes Before RAG
RAG and orchestration work are easier to validate when the user-facing entry points are already clear. Building the static shell first reduces ambiguity and prevents backend work from outpacing user experience design.

## Mapping To Integrated Solution
- `website/index.html` maps to the integrated front-end route shell.
- `chat-widget.js` maps to the future chat client/controller that will call FastAPI endpoints.
- Static placeholder responses map to future retrieval-grounded assistant responses.
- This POC acts as the UI contract for later integration under `integrated/servicecall-ai` after POC milestones are validated.
