# Hybrid Retrieval - Story Map

## 1. Story (support desk search)
A support agent searches tickets for "refund xr15 headset." The model code is exact, but the best ticket might say "returning a broken audio device." You need words and meaning.

## 2. Core Concepts (street version)
- Keyword retrieval catches exact terms.
- Vector retrieval catches similar meaning.
- Hybrid uses both signals, then ranks with both.

## 3. What hybrid retrieval is
A retrieval method that blends keyword match scores with vector similarity scores.

## 4. Why keyword-only is not enough
Exact words miss synonyms and paraphrases. "Refund" and "return" can mean the same thing but look different.

## 5. Why vector-only is not enough
Vectors can ignore exact tokens like model numbers, error codes, and legal terms that matter a lot.

## 6. How hybrid combines both
Use keyword match to catch literal terms, use vectors to catch semantic neighbors, and rank with a weighted blend.

## 7. What hybrid retrieval is great at
- Real-world search where exact terms and meaning both matter
- Strong first-pass retrieval with fewer obvious misses

## 8. What hybrid retrieval is bad at
- Hard filters (compliance, permissions)
- Deep reasoning or multi-hop answers

## 9. Final mental model
Two nets: one for words, one for meaning. Keep what either net catches. Rank with both.

## 10. Run Order
1. c093_hybrid_demo.py
