# TASK_BOARD.md

## TODO
- Build basic retrieval POC
- Discuss `03g_retrieval_decision` design only (no implementation yet)
- Product Direction Add-On: Guided Customer Input (future UX layer before retrieval; no implementation in current 03e scope)
- Build answer-with-citations POC
- Build intake classifier POC
- Build guardrails/escalation POC
- Build outcome logging POC
- Build FastAPI POC
- Dockerize backend
- Deploy manually to ECS Fargate
- Add GitHub Actions CI/CD
- Add CloudWatch observability
- Final integrated demo

## IN PROGRESS
- none

## BLOCKED
- none

## DONE
- initial repo shell
- documentation structure
- testing structure
- demo scenario structure
- add permanent agent memory / closed-loop protocol
- Build static website shell
- Create aux_scripts helper utilities
- Record Milestone 1 Cloudflare static hosting smoke test
- Create synthetic business docs
- Stage Milestone 3 retrieval-learning structure
- Implement 03a_load_documents
- Add educational comments to 03a_load_documents source
- Implement 03b_chunk_documents
- Implement 03c_text_normalization
- Implement 03d_word_tfidf_index
- Implement 03e_char_tfidf_typo_search
- Standardize `03f_hybrid_retrieval` planned runner naming to `src/run_hybrid_search.py` (documentation only)
- Record standing POC doc/acceptance rule in project control files
- Implement `03f_hybrid_retrieval` schema/contracts + tests (no retrieval/search logic yet)
- Implement `03f_hybrid_retrieval` reusable core retrieval module + tests (no runner/output file yet)
- Implement `03f_hybrid_retrieval` runner script + sample output generation
- Close `03f_hybrid_retrieval` as PASS (tests passed, runner passed, sample output written)
