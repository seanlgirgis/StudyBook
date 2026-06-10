from transformers import pipeline

grammar_checker = pipeline(
    task="text-classification",
    model="abdulmatinomotoso/English_Grammar_Checker",
)

sentences = [
    "I will walk dog",
    "I will walk the dog.",
]

for sentence in sentences:
    result = grammar_checker(sentence)
    print(f"Text: {sentence}")
    print(f"Result: {result}")
    print()
