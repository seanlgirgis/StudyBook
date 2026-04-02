# Search (Retrieval) — Story Map

## 1. Story (library index cards)
A library does not scan every shelf for a word. It keeps index cards: each word points to the books that contain it.

## 2. Core Concepts (street version)
- Lookup = id -> document.
- Search = word -> documents.
- Inverted index flips the mapping.

## 3. What search is vs lookup
Lookup finds one exact record by key. Search finds many documents by content.

## 4. What an inverted index is
A dictionary from token to the list of documents that contain it.

## 5. How queries work (AND / OR intuition)
AND = intersection (only docs with all terms). OR = union (docs with any term).

## 6. Basic ranking idea (frequency / relevance)
Docs with more matches or higher term frequency rise to the top.

## 7. What search is great at
- Finding by content
- Fast multi-document retrieval
- Fuzzy relevance-driven results

## 8. What search is bad at
- Exact transactional updates
- Strong consistency across writes
- Complex joins

## 9. Final mental model
Lookup is a keyhole. Search is a map of words to shelves.

## 10. Run Order
1. c090_search_demo.py
