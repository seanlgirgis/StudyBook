# Working with Hugging Face — Field Guide

## Course status

| Area | Status |
|---|---|
| DataCamp platform | COMPLETE |
| Documentation | STRONG |
| Local lab | STRONG |
| Recall | DEVELOPING |
| Interview readiness | NEEDS REPETITION |

## Course map

```text
Hugging Face Hub
→ model and dataset cards
→ pipeline() or hosted inference
→ tokenization and tensors
→ model output and validation
→ classification, summarization, and document Q&A
```

## Chapter guides

- [Chapter 1 — Getting Started with Hugging Face](chapter_01_getting_started_with_hugging_face_field_guide.html)
- [Chapter 2 — Building Pipelines with Hugging Face](chapter_02_building_pipelines_with_hugging_face_field_guide.html)
- [Hugging Face Code Guide](hugging_face_code_guide.html)
- [Hugging Face Quick Lookup](hugging_face_quick_lookup.html)

## Core concepts

### Hub and model cards

The Hub is a repository for models, datasets, and AI applications. Before using an asset, check:

- task and modality;
- language and domain;
- training data and evaluation;
- license and intended use;
- limitations and bias notes;
- model size and hardware requirements;
- revision when reproducibility matters.

### Pipelines

`pipeline()` combines:

```text
raw input
→ tokenizer
→ input IDs and attention mask
→ model inference
→ readable structured output
```

The pipeline defines the workflow. The trained model defines the learned behavior and label meanings.

### Local and hosted inference

| Local | Hosted |
|---|---|
| More control and privacy | More remote compute |
| No per-request provider fee | Faster access to large models |
| Limited by local CPU, RAM, GPU, and VRAM | Requires network, credentials, cost, and privacy review |

### Datasets

```python
dataset = load_dataset("imdb", split="train")
sample = dataset.shuffle(seed=42).select(range(20))
positive = sample.filter(lambda row: row["label"] == 1)
```

Memory rules:

- `filter()` = keep rows by condition, similar to SQL `WHERE`;
- `select()` = keep rows by position;
- `shuffle(seed=42)` = repeatable random ordering;
- do not assume the first rows are representative.

### Tokenizers and tensors

```python
tokenizer = AutoTokenizer.from_pretrained(model_name)
encoded = tokenizer(text, return_tensors="pt")
```

- `tokenize()` returns token strings;
- `input_ids` are numeric token identifiers;
- `attention_mask` uses `1` for real tokens and `0` for padding;
- `pt` means PyTorch tensors;
- the model must use the tokenizer it was trained with.

### AutoClasses and logits

```python
model = AutoModelForSequenceClassification.from_pretrained(model_name)
outputs = model(**inputs)
predicted_id = outputs.logits.argmax(dim=-1).item()
label = model.config.id2label[predicted_id]
```

- logits are raw unnormalized class scores;
- `argmax()` selects the highest-scoring class;
- `id2label` maps the class ID to a readable label.

### Classification

The course validated:

- sentiment classification;
- grammar classification;
- QNLI;
- zero-shot classification.

Generic labels such as `LABEL_0` and `LABEL_1` are model-specific. Read the model card or inspect `model.config.id2label`.

### Summarization

Extractive summarization selects source wording. Abstractive summarization generates new wording and may omit or invent details.

The local lab used:

```python
summary = summarizer(
    original_text,
    min_length=10,
    max_length=40
)
```

The summary reduced 297 characters to 159 but omitted an important qualification. Always compare important summaries with the source.

### PDF document Q&A

```text
PDF
→ PyPDF extracts text
→ question + context
→ answer span + score
→ threshold and source verification
```

Validated result:

```text
Question: What is the notice period for resignation?
Answer: two weeks
Score: about 0.793
```

Failure case:

```text
Question absent from context
Forced answer score: about 0.088
Action: reject and return “Not enough information”
```

Scanned image PDFs may require OCR because normal PyPDF extraction depends on a text layer.

## Common mistakes

1. Treating confidence as proof of truth.
2. Using one classifier for every classification task.
3. Assuming generic label IDs have universal meanings.
4. Sampling convenient row ranges instead of shuffling.
5. Treating tokens as identical to words.
6. Trusting fluent summaries without checking omissions.
7. Passing an entire long document without chunking or retrieval.
8. Accepting every extractive Q&A answer.

## Interview-ready answers

**How do you select a model?**  
Match the task and modality, then review license, language, training data, evaluation, size, intended use, limitations, and revision. Validate candidates on representative data.

**When do you use pipeline() versus AutoClasses?**  
Use `pipeline()` for quick standard inference. Use AutoModel and AutoTokenizer when you need custom tokenization, tensors, logits, batching, thresholds, or multi-stage integration.

**How do you make document Q&A safer?**  
Validate extraction, retrieve relevant context, inspect confidence, reject weak spans, and return “not enough information” rather than forcing an answer.

## Local lab evidence

The lab includes classification, zero-shot classification, summarization, tokenizer inspection, AutoClasses, PDF creation, PDF extraction, and confidence-threshold Q&A.

See:

- [Code Guide](hugging_face_code_guide.html)
- [Quick Lookup](hugging_face_quick_lookup.html)
- [Lab Run Book](../lab/lab_run_book.md)
