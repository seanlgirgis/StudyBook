# Chapter 2 Lab Expansion

Place these files under:

```text
D:\Workarea\StudyBook\study_maps\DataCamp\courses\working_with_hugging_face\lab\python
```

## Run order

```text
08_grammar_checking.py
09_qnli_classification.py
10_zero_shot_science.py
11_summarization_length_compare.py
12_autotokenizer_tokens.py
13_autoclasses_pipeline.py
14_create_employee_policy_pdf.py
15_pdf_document_qa.py
```

## Additional packages

```powershell
python -m pip install pypdf reportlab
```

For the DataCamp-compatible summarization pipeline used in this course:

```powershell
python -m pip install "transformers<5"
```

## What each lab proves

- `08_grammar_checking.py`: same classification pipeline, different label meaning.
- `09_qnli_classification.py`: determine whether a passage supports a question.
- `10_zero_shot_science.py`: supply candidate categories at runtime.
- `11_summarization_length_compare.py`: compare source and summary length.
- `12_autotokenizer_tokens.py`: distinguish token pieces, token IDs, and attention masks.
- `13_autoclasses_pipeline.py`: combine explicit AutoClasses with pipeline convenience.
- `14_create_employee_policy_pdf.py`: create a small local two-page PDF.
- `15_pdf_document_qa.py`: extract all PDF pages, combine text, ask a question, and reject low-confidence answers.

## Important production lessons

- The pipeline task gives the workflow; the model defines the learned behavior and label meanings.
- Zero-shot labels are supplied at inference time.
- QNLI screens whether a passage can answer a question; it does not extract the answer.
- Summarization length limits can truncate output.
- `tokenize()` returns token strings; calling the tokenizer returns IDs and masks.
- Extractive Q&A may force an answer even when none exists, so use a confidence threshold.
- Normal PyPDF extraction works only when the PDF contains a text layer. Scanned images require OCR.
