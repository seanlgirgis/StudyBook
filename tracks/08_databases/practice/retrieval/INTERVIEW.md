# Interview Questions - Retrieval

> Topics covered: search / inverted index
> Levels: Starter | Mid | Senior | Architect

---

## Topic - Search / Inverted Index

### Level 1 - Starter

**Q1: In c090_search_demo.py, what is an inverted index in plain language?**
What a good answer covers:
- It maps a term to the list of document IDs containing it
- It is built by tokenizing each document and recording postings
- It makes term lookups fast without scanning all documents
Why this is asked: Confirms the core inverted-index concept from the demo.

**Q2: In c090_search_demo.py, what is the basic search flow from documents to results?**
What a good answer covers:
- Tokenize documents into terms
- Build the inverted index (term -> doc IDs)
- Use the index to return matches for a query term
Why this is asked: Checks understanding of the end-to-end search pipeline.

**Q3: In c090_search_demo.py, how is lookup (id -> document) different from search (term -> docs)?**
What a good answer covers:
- Lookup retrieves one known document by key
- Search returns multiple documents that match content
- Search uses the inverted index and can rank results
Why this is asked: Tests the foundational difference between lookup and search.

**Q4: In c090_search_demo.py, how do AND vs OR queries change the result set?**
What a good answer covers:
- AND intersects posting lists to narrow results
- OR unions posting lists to widen results
- The demo shows different doc IDs for each operator
Why this is asked: Verifies understanding of multi-term query mechanics.

### Level 2 - Mid

**Q1: In c090_search_demo.py, why does tokenization (the _tokenize function) matter for search quality?**
What a good answer covers:
- Tokenization defines what the index can match
- It normalizes case and strips punctuation
- Poor tokenization leads to missed or noisy matches
Why this is asked: Probes practical indexing mechanics.

**Q2: In c090_search_demo.py, how does term-frequency ranking work and what is its basic intuition?**
What a good answer covers:
- Count how often query terms appear in a document
- Higher counts score higher in the demo
- It is a simple but naive relevance signal
Why this is asked: Tests baseline ranking intuition from the demo.

**Q3: In c091_ranking_demo.py, what changes when you go from match-count ranking to term-frequency ranking?**
What a good answer covers:
- Match-count treats all terms equally (presence/absence)
- Term frequency boosts documents with repeated terms
- The ranked order shifts in the demo output
Why this is asked: Checks understanding of ranking basics.

**Q4: In c091_ranking_demo.py, how does rarity (IDF) alter rankings compared to raw TF?**
What a good answer covers:
- Rare terms contribute more to relevance scores
- Common terms contribute less despite high frequency
- The demo shows a new ordering when IDF is applied
Why this is asked: Ensures candidates understand why IDF exists.

### Level 3 - Senior

**Q1: In c095_bm25_demo.py, why does BM25 produce a better order than raw TF or overlap?**
What a good answer covers:
- It balances term rarity, frequency saturation, and length normalization
- It avoids over-rewarding repetition (Doc 2 in the demo)
- It boosts rare, important terms (xr15) appropriately
Why this is asked: Tests understanding of BM25�s advantages.

**Q2: In c091_ranking_demo.py, what relevance-tuning decision would you make if your results over-emphasize repeated terms?**
What a good answer covers:
- Reduce TF weight or add saturation similar to BM25
- Increase the impact of rarity (IDF)
- Validate ranking shifts against expected results
Why this is asked: Probes practical ranking-tuning judgment.

**Q3: In c090_search_demo.py, what scalability issue appears as documents and terms grow, and how would you address it?**
What a good answer covers:
- Posting lists and the index grow large in memory
- Query latency rises with longer posting lists
- Sharding the index or compressing postings mitigates scale issues
Why this is asked: Evaluates search scaling awareness grounded in the demo.

### Level 4 - Architect

**Q1: Using c091_ranking_demo.py and c090_search_demo.py, how would you design a search service that combines ranking with metadata filtering?**
What a good answer covers:
- Retrieve candidates via the inverted index, then rank with scoring
- Apply metadata filters before or during ranking to narrow candidates
- Ensure ranking signals still work after filters reduce the set
Why this is asked: Tests system design that integrates ranking and metadata filtering.

**Q2: Using c090_search_demo.py and c095_bm25_demo.py, how would you scale an inverted index across distributed search systems without breaking relevance?**
What a good answer covers:
- Shard the index by term or document and merge partial rankings
- Preserve BM25 scoring consistency across shards
- Plan for cross-shard aggregation and latency tradeoffs
Why this is asked: Probes distributed search design with relevance consistency.

---

## Topic - Ranking

### Level 1 - Starter

**Q1: In d02_ranking_story.md, what is ranking in plain language and why is it needed after search?**
What a good answer covers:
- Search finds candidates, ranking orders them
- A score estimates relevance to the query
- Ranking puts the most useful results on top
Why this is asked: Confirms the story-level definition of ranking.

**Q2: In c091_ranking_demo.py, what does the "Candidates only" step show?**
What a good answer covers:
- Candidates are un-ordered matches from the index
- No ranking means results are just a list
- Ranking is required to make results useful
Why this is asked: Checks understanding of the baseline before scoring.

**Q3: In c091_ranking_demo.py, what is match-count scoring and how does it rank results?**
What a good answer covers:
- It counts how many query terms appear in a document
- More matched terms yields a higher score
- It is a simple, explainable ranking signal
Why this is asked: Verifies basic scoring mechanics.

**Q4: In c091_ranking_demo.py, how does term-frequency scoring differ from match-count?**
What a good answer covers:
- It counts repeated terms, not just presence
- Documents with repeated terms score higher
- The ranked order shifts compared to match-count
Why this is asked: Tests basic TF intuition from the demo.

### Level 2 - Mid

**Q1: In c091_ranking_demo.py, when is match-count ranking too weak for real search?**
What a good answer covers:
- It treats all terms equally and ignores repetition
- It can mis-rank when one term is far more important
- The demo shows different order once TF or IDF is applied
Why this is asked: Probes application and tradeoff awareness.

**Q2: In c091_ranking_demo.py, what common mistake is illustrated by over-trusting raw TF?**
What a good answer covers:
- Repeated words can dominate the score unfairly
- TF can drown out more meaningful rare terms
- The demo motivates adding rarity/IDF weighting
Why this is asked: Checks recognition of a common ranking pitfall.

**Q3: In d02_ranking_story.md, what tradeoff exists between simple and complex ranking signals?**
What a good answer covers:
- Simple ranking is fast and explainable
- Complex ranking can be more accurate but harder to tune
- You must balance relevance gains with operational cost
Why this is asked: Tests judgment on ranking design tradeoffs.

**Q4: In c095_bm25_demo.py, why does overlap ranking fail compared to BM25?**
What a good answer covers:
- Overlap ignores frequency saturation and length effects
- It ties documents that should not be equally relevant
- BM25 fixes this by combining rarity, saturation, and length norm
Why this is asked: Evaluates understanding of BM25�s motivation.

### Level 3 - Senior

**Q1: In c095_bm25_demo.py, what failure mode appears when raw TF over-rewards repetition?**
What a good answer covers:
- Documents with spammy repetition float to the top
- The demo shows Doc 2 rising for repeated "refund"
- BM25 reduces this with saturation and length normalization
Why this is asked: Tests reasoning about ranking failure modes.

**Q2: In c096_reranking_demo.py, what is the risk of setting top-k too small in a reranking pipeline?**
What a good answer covers:
- Relevant documents can be excluded from reranking
- The demo shows a relevant doc outside top-k
- Rerank cannot recover items it never sees
Why this is asked: Probes edge-case awareness in two-stage ranking.

**Q3: In c096_reranking_demo.py, what design decision controls the tradeoff between latency and relevance?**
What a good answer covers:
- First-pass scoring must be fast and broad enough
- Reranker is slower but higher quality on top-k
- Choosing top-k and signals balances cost and relevance
Why this is asked: Tests design tradeoffs in ranking pipelines.

### Level 4 - Architect

**Q1: Using c091_ranking_demo.py, how would you integrate ranking with a cache-aside layer (cache track) at scale?**
What a good answer covers:
- Cache top queries or top-k results to reduce recompute
- Ensure cache keys include query terms and ranking version
- Balance cache freshness with ranking updates and relevance drift
Why this is asked: Connects ranking to cache design at scale.

**Q2: Using c095_bm25_demo.py and c096_reranking_demo.py, how would you design a distributed ranking system that still produces consistent relevance across shards?**
What a good answer covers:
- Compute BM25 consistently per shard and merge global top-k
- Use a reranker on merged candidates to refine ordering
- Address cross-shard aggregation latency and scoring parity
Why this is asked: Tests distributed system design with ranking quality.

---

## Topic - Vector Similarity

### Level 1 - Starter

**Q1: In c092_vector_demo.py, what is vector similarity in plain language?**
What a good answer covers:
- It measures how close two embeddings are in vector space
- Higher similarity means more semantic closeness
- The demo ranks neighbors by similarity score
Why this is asked: Confirms the basic meaning of vector similarity.

**Q2: In c092_vector_demo.py, what does an embedding represent for a document?**
What a good answer covers:
- A numeric representation of meaning across dimensions
- Similar meanings produce similar vectors
- The demo uses hand-crafted dimensions for intuition
Why this is asked: Tests understanding of embeddings as meaning vectors.

**Q3: In c092_vector_demo.py, how does cosine similarity differ from simple keyword overlap?**
What a good answer covers:
- Cosine compares vector direction rather than exact word match
- It can find semantic matches with little or no token overlap
- The demo shows higher similarity for related meanings
Why this is asked: Verifies the value of semantic similarity.

**Q4: In c092_vector_demo.py, why might L2 distance tell a similar story to cosine for normalized vectors?**
What a good answer covers:
- Both measure closeness in vector space
- When vectors are normalized, cosine and L2 rankings align closely
- The key idea is ranking by proximity, not exact words
Why this is asked: Checks basic understanding of similarity metrics.

### Level 2 - Mid

**Q1: In c092_vector_demo.py, why would exact search struggle on "budget laptop deal" compared to vector similarity?**
What a good answer covers:
- Exact keywords don't match "affordable notebook computer"
- Vector similarity still finds semantic neighbors
- The demo shows similarity winning over overlap
Why this is asked: Probes practical motivation for vector search.

**Q2: In c093_hybrid_demo.py, what tradeoff does the hybrid ranking weight (keyword vs vector) represent?**
What a good answer covers:
- More keyword weight favors exact terms
- More vector weight favors semantic similarity
- The blend balances precision vs recall
Why this is asked: Tests tuning intuition for hybrid search.

**Q3: In c092_vector_demo.py, why would approximate nearest neighbor (ANN) be used instead of exact search at scale?**
What a good answer covers:
- Exact similarity over all vectors is too slow at large scale
- ANN trades a small recall loss for major latency gains
- It enables practical vector search in production
Why this is asked: Evaluates understanding of ANN tradeoffs.

**Q4: In c094_metadata_filtering_demo.py, why should metadata filters run before vector ranking?**
What a good answer covers:
- Filtering removes invalid candidates early
- It reduces ranking cost and improves correctness
- The demo shows ranking alone can surface wrong results
Why this is asked: Connects vector retrieval to filtering mechanics.

### Level 3 - Senior

**Q1: In c093_hybrid_demo.py, what failure mode appears if you rely on vector-only search?**
What a good answer covers:
- It can surface semantically related but wrong-intent results
- Exact keyword constraints can be missed
- The demo shows hybrid fixes the mismatch
Why this is asked: Tests judgment on hybrid necessity.

**Q2: In c092_vector_demo.py, how would you tune recall vs latency for a vector index?**
What a good answer covers:
- Increase search breadth for higher recall
- Reduce search breadth for lower latency
- Validate tradeoffs with nearest-neighbor quality checks
Why this is asked: Probes tuning decisions in vector systems.

**Q3: In c094_metadata_filtering_demo.py, what edge case appears if filters are too strict before vector search?**
What a good answer covers:
- The candidate set can become empty
- Even relevant semantic matches are excluded
- The demo shows over-filtering dropping all results
Why this is asked: Checks awareness of filtering failure modes.

### Level 4 - Architect

**Q1: Using c093_hybrid_demo.py and c092_vector_demo.py, how would you design a RAG retrieval stage that blends inverted index search and vector similarity with ranking?**
What a good answer covers:
- Use inverted index to fetch exact matches and vector search for semantic recall
- Merge candidates and apply a ranker/reranker to produce the final top-k
- Balance keyword precision with semantic recall for RAG quality
Why this is asked: Connects vector similarity to search and ranking tracks.

**Q2: Using c094_metadata_filtering_demo.py and c093_hybrid_demo.py, how would you scale vector + keyword retrieval across distributed shards while keeping ranking consistent?**
What a good answer covers:
- Apply filters per shard to reduce candidate volume
- Merge shard top-k for both keyword and vector signals
- Use a global reranker to normalize scores across shards
Why this is asked: Tests distributed retrieval design with hybrid ranking.

---

## Topic - Hybrid Search

### Level 1 - Starter

**Q1: In c093_hybrid_demo.py, what is hybrid search in plain language?**
What a good answer covers:
- It blends keyword matching with vector similarity
- Keyword captures exact terms; vector captures meaning
- The demo shows a combined score per document
Why this is asked: Confirms the basic hybrid definition.

**Q2: In c093_hybrid_demo.py, why combine keyword and vector signals instead of using just one?**
What a good answer covers:
- Keyword-only can miss semantic matches
- Vector-only can miss exact intent terms
- The hybrid blend keeps precision and recall balanced
Why this is asked: Tests motivation for hybrid retrieval.

**Q3: In c090_search_demo.py, what does keyword search provide that hybrid wants to preserve?**
What a good answer covers:
- Exact term matching with an inverted index
- Fast candidate retrieval for precise queries
- Clear intent matching for specific terms
Why this is asked: Links hybrid search to inverted index behavior.

**Q4: In c092_vector_demo.py, what does vector similarity provide that hybrid adds on top of keyword search?**
What a good answer covers:
- Semantic matches without exact overlap
- Meaning-based proximity ranking
- Coverage for paraphrases and related terms
Why this is asked: Checks the semantic side of the hybrid blend.

### Level 2 - Mid

**Q1: In c093_hybrid_demo.py, how does the keyword vs vector weight affect ranking outcomes?**
What a good answer covers:
- Increasing keyword weight favors exact term matches
- Increasing vector weight favors semantic matches
- The demo shows different orders as the blend shifts
Why this is asked: Tests tuning intuition for score fusion.

**Q2: In c096_reranking_demo.py, how would you use reranking as a fusion strategy for hybrid search?**
What a good answer covers:
- Use a cheap first-pass (keyword or vector) to get candidates
- Apply a smarter reranker that uses both signals
- Keep the candidate set small for latency
Why this is asked: Probes practical fusion strategy design.

**Q3: In c090_search_demo.py, what tradeoff appears when you add vector search on top of inverted index retrieval?**
What a good answer covers:
- More recall but higher compute cost
- Extra scoring and candidate merging steps
- Latency increases unless you limit candidates
Why this is asked: Checks awareness of hybrid tradeoffs.

**Q4: In c093_hybrid_demo.py, what common mistake leads to irrelevant results despite hybrid scoring?**
What a good answer covers:
- Poor weight calibration between keyword and vector
- Not normalizing scores before combining
- Letting one signal dominate all queries
Why this is asked: Tests common tuning pitfalls.

### Level 3 - Senior

**Q1: In c096_reranking_demo.py, how does top-k selection affect recall in a hybrid pipeline?**
What a good answer covers:
- If top-k is too small, relevant docs never reach reranking
- Hybrid quality depends on a sufficiently broad candidate set
- The demo shows a relevant doc missed outside top-k
Why this is asked: Evaluates recall vs latency tradeoffs.

**Q2: In c093_hybrid_demo.py, what tuning decision controls precision vs recall the most?**
What a good answer covers:
- The weighting between keyword and vector scores
- Candidate set size from each retriever
- Normalization strategy for combined scores
Why this is asked: Tests pipeline tuning decisions.

**Q3: In c092_vector_demo.py, how would you keep hybrid latency low without losing semantic recall?**
What a good answer covers:
- Use ANN to reduce vector search cost
- Limit vector candidates while preserving quality
- Cache popular query embeddings or results
Why this is asked: Probes latency optimization with vector search.

### Level 4 - Architect

**Q1: Using c090_search_demo.py, c092_vector_demo.py, and c096_reranking_demo.py, how would you design an end-to-end RAG retrieval stack that combines inverted index, vector similarity, and reranking?**
What a good answer covers:
- Use inverted index for precise candidates and vector for semantic recall
- Merge and rerank with a learned or rules-based scorer
- Control latency with top-k limits and staged retrieval
Why this is asked: Tests full-system design across keyword, vector, and reranking.

**Q2: Using c093_hybrid_demo.py and c096_reranking_demo.py, how would you scale hybrid retrieval across shards while keeping ranking consistent?**
What a good answer covers:
- Score normalization per shard before fusion
- Merge shard top-k and rerank globally
- Balance cross-shard latency with relevance quality
Why this is asked: Probes distributed hybrid retrieval design.

---

## Topic - Metadata Filtering

### Level 1 - Starter

**Q1: In c094_metadata_filtering_demo.py, what is metadata filtering in plain language?**
What a good answer covers:
- Filtering by structured fields like region, product, or status
- Removing invalid candidates before ranking
- Ensuring results match required constraints
Why this is asked: Confirms the basic definition using the demo.

**Q2: In c094_metadata_filtering_demo.py, what changes between "ranking without filtering" and "ranking after filtering"?**
What a good answer covers:
- Unfiltered ranking can surface invalid results
- Filtering narrows candidates to valid metadata matches
- The top result shifts after filtering
Why this is asked: Checks understanding of the demo�s core contrast.

**Q3: In c094_metadata_filtering_demo.py, what does the FILTERS dictionary represent?**
What a good answer covers:
- Required constraints for the query context
- Fields that must match (product, region, status)
- A gate before ranking happens
Why this is asked: Tests basic mechanics of filter application.

**Q4: In c090_search_demo.py, why is filtering different from keyword search?**
What a good answer covers:
- Keyword search matches text terms via inverted index
- Filtering uses structured metadata fields
- Filters enforce constraints that keywords cannot guarantee
Why this is asked: Distinguishes filtering from text retrieval.

### Level 2 - Mid

**Q1: In c094_metadata_filtering_demo.py, why is pre-filtering safer than post-filtering?**
What a good answer covers:
- Pre-filtering prevents invalid results from being ranked
- Post-filtering can waste compute on disallowed docs
- The demo shows ranking can be wrong without filters
Why this is asked: Probes filtering order tradeoffs.

**Q2: In c092_vector_demo.py, how would metadata filters change vector search behavior?**
What a good answer covers:
- Filters limit which vectors are eligible to rank
- They reduce candidate volume and improve relevance
- Semantic matches outside constraints are excluded
Why this is asked: Tests vector + filter integration.

**Q3: In c093_hybrid_demo.py, where would you insert metadata filtering in a hybrid pipeline?**
What a good answer covers:
- Apply filters before merging keyword and vector candidates
- Or filter each candidate set before fusion
- This avoids invalid results dominating the blend
Why this is asked: Checks pipeline placement decisions.

**Q4: In c094_metadata_filtering_demo.py, what common mistake leads to empty results?**
What a good answer covers:
- Overly strict filters (pending status example)
- Filters that conflict with actual data distribution
- The demo shows an empty candidate set
Why this is asked: Tests awareness of over-filtering risks.

### Level 3 - Senior

**Q1: In c094_metadata_filtering_demo.py, what performance tradeoff appears as filters become more complex?**
What a good answer covers:
- More filter dimensions require more index lookups
- Filtering can become a bottleneck if not indexed
- You trade correctness for extra query cost
Why this is asked: Evaluates performance reasoning.

**Q2: In c094_metadata_filtering_demo.py, how would you index metadata to keep filtering fast at scale?**
What a good answer covers:
- Build inverted indexes or hash maps on metadata fields
- Precompute candidate sets per common filter values
- Avoid full scans of metadata for each query
Why this is asked: Tests scaling strategy for filtering.

**Q3: In c092_vector_demo.py, what edge case appears if you filter after vector ranking?**
What a good answer covers:
- Top-ranked vectors may be discarded by filters
- You may end up with too few results
- It wastes vector compute on invalid candidates
Why this is asked: Probes post-filtering failure modes.

### Level 4 - Architect

**Q1: Using c093_hybrid_demo.py, c092_vector_demo.py, and c090_search_demo.py, how would you design a retrieval system that combines inverted index search, vector similarity, and metadata filtering?**
What a good answer covers:
- Use metadata filters as a first gate for both keyword and vector retrieval
- Fetch keyword and vector candidates, then fuse and rank
- Ensure constraints are enforced before final ranking
Why this is asked: Tests end-to-end design across search and vector tracks.

**Q2: Using c094_metadata_filtering_demo.py and c093_hybrid_demo.py, how would you scale filtering in a hybrid system without harming relevance?**
What a good answer covers:
- Pre-index metadata to prune candidates quickly
- Apply filters before hybrid score fusion
- Preserve recall by avoiding overly strict filters
Why this is asked: Probes system design for filtering at scale.

---

## Topic - BM25

### Level 1 - Starter

**Q1: In c095_bm25_demo.py, what is BM25 in plain language?**
What a good answer covers:
- A ranking formula for keyword search relevance
- It combines term frequency, rarity, and document length
- The demo shows BM25 reordering results more sensibly
Why this is asked: Confirms the basic BM25 definition from the demo.

**Q2: In c095_bm25_demo.py, what does TF + IDF mean in the BM25 intuition?**
What a good answer covers:
- TF rewards terms that appear in a document
- IDF rewards rare terms across the corpus
- BM25 blends both so rare, relevant terms matter more
Why this is asked: Tests understanding of BM25�s core signals.

**Q3: In c095_bm25_demo.py, why is length normalization part of BM25?**
What a good answer covers:
- Longer documents naturally contain more terms
- Normalization prevents long docs from dominating scores
- The demo shows shorter, cleaner docs rising
Why this is asked: Checks the length-normalization intuition.

**Q4: In c091_ranking_demo.py, how does BM25 relate to the rarity intuition shown in IDF-weighted scoring?**
What a good answer covers:
- BM25 builds on the same IDF idea
- It adds saturation and length normalization on top
- It refines the simple rarity weighting shown in the demo
Why this is asked: Links BM25 to the ranking demo concepts.

### Level 2 - Mid

**Q1: In c095_bm25_demo.py, what components make up the BM25 score?**
What a good answer covers:
- Term frequency for each query term
- Inverse document frequency for rarity
- A length normalization factor using average doc length
Why this is asked: Checks knowledge of BM25�s scoring components.

**Q2: In c095_bm25_demo.py, why is BM25 better than raw TF scoring?**
What a good answer covers:
- Raw TF over-rewards repetition (Doc 2 in the demo)
- BM25 saturates term frequency to avoid spammy boosts
- It balances repetition with rarity and length
Why this is asked: Tests BM25�s practical advantage over TF.

**Q3: In c091_ranking_demo.py, what limitation of TF-IDF does BM25 address?**
What a good answer covers:
- TF-IDF does not normalize for document length well
- It does not saturate repeated term counts
- BM25 improves both with length norm and saturation
Why this is asked: Evaluates understanding of why BM25 exists.

**Q4: In c096_reranking_demo.py, where would BM25 fit in a two-stage ranking pipeline?**
What a good answer covers:
- BM25 can serve as a fast first-pass ranker
- Top-k candidates are then reranked by a smarter model
- The demo shows the importance of top-k selection
Why this is asked: Connects BM25 to reranking workflows.

### Level 3 - Senior

**Q1: In c095_bm25_demo.py, how would tuning k1 change the ranking behavior?**
What a good answer covers:
- Higher k1 increases the impact of term frequency
- Lower k1 saturates TF sooner, reducing repetition boosts
- The tradeoff changes which docs rise in the demo
Why this is asked: Tests parameter tuning intuition.

**Q2: In c095_bm25_demo.py, how would adjusting b affect long vs short documents?**
What a good answer covers:
- Higher b increases length normalization for long docs
- Lower b reduces the length penalty
- It shifts the balance between verbose and concise docs
Why this is asked: Probes length-normalization tuning decisions.

**Q3: In c095_bm25_demo.py, what edge case appears when a query term is extremely common?**
What a good answer covers:
- IDF becomes small, reducing the term�s influence
- Scores depend more on other query terms
- This prevents common words from dominating relevance
Why this is asked: Evaluates understanding of BM25 edge cases.

### Level 4 - Architect

**Q1: Using c095_bm25_demo.py and c096_reranking_demo.py, how would you position BM25 in a modern ranking stack that also uses reranking?**
What a good answer covers:
- Use BM25 for fast candidate retrieval
- Apply reranking for intent-aware ordering
- Balance recall and latency with top-k sizing
Why this is asked: Connects BM25 to ranking and reranking design.

**Q2: Using c095_bm25_demo.py, c093_hybrid_demo.py, and c092_vector_demo.py, how would you blend BM25 with vector similarity in a hybrid search system?**
What a good answer covers:
- Use BM25 for precise keyword matches and vector for semantic recall
- Merge or rerank combined candidates to unify scoring
- Calibrate the blend to avoid over-weighting one signal
Why this is asked: Tests cross-signal system design with hybrid and vector search.

---

## Topic - Reranking + Top-k / Recall@k

### Level 1 - Starter

**Q1: In c096_reranking_demo.py, what is reranking in plain language?**
What a good answer covers:
- A cheap first-pass scorer retrieves a small candidate set
- A smarter second-pass scorer reorders those candidates with richer signals
- The demo uses overlap score for the first pass and a weighted reranker for the second
Why this is asked: Confirms the basic two-stage reranking definition from the demo.

**Q2: In c096_reranking_demo.py, why does the first-pass ranker use overlap score instead of something more complex?**
What a good answer covers:
- Overlap score is fast to compute across all documents
- The goal of the first pass is to narrow candidates cheaply, not to produce perfect order
- The reranker handles quality; the first pass handles speed
Why this is asked: Checks understanding of the speed vs quality split in two-stage pipelines.

**Q3: In c097_topk_recall_demo.py, what is Recall@k in plain language?**
What a good answer covers:
- It measures what fraction of the truly relevant documents appear in the top-k results
- RELEVANT is the ground-truth set; top-k is the ranked shortlist
- The demo evaluates Recall@k at multiple k values to show how it changes
Why this is asked: Verifies the core definition of Recall@k using the demo's RELEVANT set.

**Q4: In c097_topk_recall_demo.py, what happens to Recall@k as k increases?**
What a good answer covers:
- Recall@k rises or stays flat as k grows because more candidates are included
- At k equal to the full corpus, recall is 1.0 if all relevant docs are present
- The demo shows recall improving across K_VALUES = [1, 3, 5]
Why this is asked: Tests the basic monotonic property of recall with increasing k.

### Level 2 - Mid

**Q1: In c096_reranking_demo.py, what is the risk of setting TOP_K too small?**
What a good answer covers:
- Relevant documents outside the top-k window are never seen by the reranker
- The reranker cannot recover items it never receives as candidates
- The demo sets TOP_K = 3, which can exclude relevant docs ranked lower by the first pass
Why this is asked: Probes the candidate-cutoff failure mode in two-stage ranking.

**Q2: In c097_topk_recall_demo.py, how do you interpret a Recall@3 of 0.67 for query "xr15 refund denied"?**
What a good answer covers:
- Two of the three truly relevant documents appear in the top-3 results
- One relevant document is ranked outside the top-3
- Improving first-pass ranking or increasing k would raise recall toward 1.0
Why this is asked: Tests practical interpretation of a Recall@k value from the demo.

**Q3: In c096_reranking_demo.py, how does the reranker_score function differ from overlap_score in its signal design?**
What a good answer covers:
- Overlap score counts matching terms with equal weight
- Reranker assigns higher weights to specific high-signal tokens like "denied" and "xr15"
- The weighted design produces a different, more intent-aware ordering
Why this is asked: Evaluates understanding of signal design differences between the two scoring stages.

**Q4: In c097_topk_recall_demo.py, why is Recall@k a more useful metric than raw accuracy for retrieval systems?**
What a good answer covers:
- Accuracy assumes one correct answer; retrieval can have multiple relevant items
- Recall@k measures coverage of the relevant set within the shortlist
- It is grounded in a known RELEVANT set, as the demo shows with {1, 4, 8}
Why this is asked: Checks why Recall@k is the standard retrieval evaluation metric.

### Level 3 - Senior

**Q1: In c096_reranking_demo.py, how would you tune TOP_K to balance latency and recall without running the reranker on too many candidates?**
What a good answer covers:
- Measure Recall@k at several k values using the c097 approach to find the recall knee
- Choose the smallest k where recall is acceptably high
- Profile reranker latency per candidate to set a compute budget
Why this is asked: Tests the recall vs latency tradeoff design decision in production pipelines.

**Q2: In c097_topk_recall_demo.py, how would poor first-pass ranking distort the Recall@k curve?**
What a good answer covers:
- A weak first-pass ranker places relevant docs far down the list
- Recall@k stays low until k is large enough to capture them
- The curve rises slowly instead of sharply, signaling a first-pass quality problem
Why this is asked: Evaluates ability to diagnose first-pass quality from a recall curve.

**Q3: In c096_reranking_demo.py, how would you validate that the reranker actually improves end-to-end ranking quality beyond what the first pass provides?**
What a good answer covers:
- Compare Recall@k and NDCG before and after reranking using a labeled RELEVANT set
- Use the c097 framework to measure recall at multiple k values for both stages
- Confirm the reranker moves relevant documents higher without harming precision
Why this is asked: Tests diagnostic rigor for measuring two-stage pipeline improvement.

### Level 4 - Architect

**Q1: Using c096_reranking_demo.py and c097_topk_recall_demo.py, how would you design a search evaluation framework that tracks recall and ranking quality continuously as models are updated?**
What a good answer covers:
- Maintain a curated RELEVANT set per query as a ground-truth benchmark
- Run Recall@k and NDCG evaluations automatically on each model or pipeline change
- Alert when recall drops below a threshold at any k value in K_VALUES
- Connect evaluations to the data quality track to catch label drift and stale relevance sets
Why this is asked: Tests system-level thinking about continuous ML evaluation and data quality governance.

**Q2: Using c096_reranking_demo.py and c097_topk_recall_demo.py, how would you scale a two-stage reranking pipeline across distributed shards without degrading Recall@k?**
What a good answer covers:
- Run first-pass ranking per shard to get shard-level top-k candidates
- Merge shard top-k into a global candidate set before the reranker
- Validate global Recall@k after merging to confirm no relevant docs are lost to per-shard cutoffs
- Use the recall curve from c097 to set per-shard k high enough to preserve global recall
Why this is asked: Connects reranking and recall evaluation to distributed search design.
