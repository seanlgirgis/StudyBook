from transformers import pipeline

classifier = pipeline(
    task="text-classification",
    model="cross-encoder/qnli-electra-base",
)

examples = [
    "Where is the capital of France?, Paris is the capital of France.",
    "Where is the capital of France?, Brittany is known for its stunning coastline.",
]

for example in examples:
    result = classifier(example)
    print(f"Input: {example}")
    print(f"Result: {result}")
    print()
