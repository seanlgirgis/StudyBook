from datasets import load_dataset

dataset = load_dataset("imdb", split="train")

sample = dataset.shuffle(seed=42).select(range(20))

positive_rows = sample.filter(
    lambda row: row["label"] == 1
)

print(sample)
print("Positive rows:", len(positive_rows))