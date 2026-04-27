# Splunk Gotcha Nuggets

## 1) The Noisy Index Ate Your License, and Now Everything Looks Empty
A single chatty sourcetype can burn through your daily license so fast that engineers swear the platform is broken because every search suddenly comes back with 0 results. In a Citi-style environment watching 6,000+ API endpoints, one misconfigured latency feed can flood the wrong index and make healthy data look like it vanished.
**Fix/Lesson:** Check license usage before blaming search—license throttling from one noisy index can make the whole estate feel dead even when the forwarders are still sending.

## 2) `spath` Lies to You When the JSON Shape Changes
Engineers who “know JSON” still get burned when `spath` works on one payload and silently fails on another because HEC-wrapped events often need `spath event.field`, while flat dictionaries need `spath field` directly. That gets nasty in telemetry pipelines when one API error stream is wrapped and another from the same endpoint family is not.
**Fix/Lesson:** Inspect the actual event structure first, then point `spath` at the real path instead of assuming every JSON payload starts at the same root.

## 3) Summary Indexing and Report Acceleration Are Not the Same Shortcut
People reach for summary indexing and report acceleration like they are interchangeable, then wonder why storage, freshness, and query behavior do not line up. In a high-volume Citi monitoring setup, the wrong choice can either bloat your footprint or make an executive latency dashboard lag behind the incident bridge.
**Fix/Lesson:** Use summary indexing when you want explicit control over precomputed rolled-up data, and report acceleration when you want faster access to a specific transforming search without building a parallel data product.

## 4) `count` and `count(*)` Are Close Cousins, Not Twins
A lot of smart users assume `stats count` and `stats count(*)` always mean the same thing, then spend an hour chasing phantom drops in volume. In practice, field-aware counting behavior can surprise you when sparse telemetry fields appear only on certain endpoint categories or severity tiers.
**Fix/Lesson:** Be deliberate—know whether you are counting events generically or counting populated values in a field-shaped context before trusting the number.

## 5) One Bad `LINE_BREAKER` Can Turn a Thousand Events into Ten Monsters
Multi-line logs are where confidence goes to die, because a bad `props.conf` `LINE_BREAKER` can merge separate events into giant blobs that look valid until parsing, timestamps, and alert correlation all go sideways. That is brutal when API stack traces from multiple services get fused together and the on-call team cannot tell which endpoint actually failed.
**Fix/Lesson:** Validate event boundaries early with raw event inspection, because broken line breaking poisons everything downstream—timestamps, fields, and alert fidelity.

## 6) Your HEC Token Works Perfectly—Into the Wrong Index
A HEC token can be valid, authenticated, and still send data somewhere useless because it is scoped to the wrong index or locked down differently than you assumed. In a telemetry estate with endpoint latency, error, and throughput feeds, that mistake creates the illusion that one pipeline is broken when the data is quietly landing elsewhere.
**Fix/Lesson:** Verify token-to-index mapping explicitly, because “HEC accepted it” does not mean “your search is looking where the event landed.”

## 7) `AUTO_KV_JSON` Will Not Save You from a Weird Delimiter
Engineers expect automatic field extraction magic, then lose half a day because the sourcetype uses a custom delimiter and `AUTO_KV` never extracts what the dashboard depends on. This gets especially ugly when a custom application log from a critical API tier ships key-value pairs that look obvious to humans but opaque to Splunk.
**Fix/Lesson:** When delimiters are nonstandard, define the extraction intentionally instead of assuming Splunk will infer structure from vibes.

## 8) Search-Time vs Index-Time Extraction Is a Trade You Feel Later
People love index-time extraction right up until the schema changes, and they love search-time extraction right up until the dashboard gets slow at scale. In a Citi-like environment with 500,000 metrics rows feeding operational analysis, the wrong decision can either lock you into brittle parsing or make every troubleshooting search pay the parsing tax.
**Fix/Lesson:** Put only high-value, stable fields at index time and keep volatile or exploratory parsing at search time where you can adapt without reingesting history.

## 9) The Free License Does Not Warn You Nicely Before It Stops Helping
Splunk Free feels fine for a lab until you cross the 500 MB/day limit and indexing pauses, which makes new engineers think forwarders, inputs, or parsing broke overnight. Even a modest burst of API telemetry or verbose debug logs can hit that ceiling faster than expected.
**Fix/Lesson:** Treat the 500 MB/day limit as a hard operational boundary, not a soft guideline, because once you cross it your ingest story changes immediately.

## 10) Your Summary Index Exists, but Your Search Still Misses It
Teams carefully build summary indexes, populate them, and then wonder why their searches do not improve—because Splunk does not magically search summary data unless you target it. That mistake is common in performance triage when people accelerate a daily latency trend for 6,000+ monitored endpoints but keep querying only the original event indexes.
**Fix/Lesson:** Add `index=summary` explicitly when you want summary data, or you may end up benchmarking the wrong thing and blaming acceleration for not working.
