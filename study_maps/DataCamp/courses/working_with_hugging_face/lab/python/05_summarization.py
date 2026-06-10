from transformers import pipeline

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6"
)

text = """
Artificial intelligence is increasingly used in data engineering.
It can help classify documents, summarize reports, detect anomalies,
and answer questions from large collections of text.
However, the quality of the result depends on the model,
the source data, and the way the task is designed.
"""

result = summarizer(
    text,
    min_length=10,
    max_length=40
)

print(result[0]["summary_text"])