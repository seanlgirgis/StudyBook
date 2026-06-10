from transformers import pipeline

summarizer = pipeline(
    task="summarization",
    model="sshleifer/distilbart-cnn-12-6",
)

original_text = """
Artificial intelligence is increasingly used in data engineering.
It can help classify documents, summarize reports, detect anomalies,
and answer questions from large collections of text.
However, the quality of the result depends on the model,
the source data, and the way the task is designed.
"""

summary = summarizer(
    original_text,
    min_length=10,
    max_length=40,
)

summary_text = summary[0]["summary_text"]

print("Original:")
print(original_text.strip())
print()
print("Summary:")
print(summary_text)
print()
print(f"Original character count: {len(original_text)}")
print(f"Summary character count: {len(summary_text)}")
