"""Run two independent transformations from the same input."""

from langchain_core.runnables import RunnableLambda, RunnableParallel


def uppercase_text(data):
    return data["text"].upper()


def count_words(data):
    return len(data["text"].split())


parallel = RunnableParallel(
    uppercase=RunnableLambda(uppercase_text),
    word_count=RunnableLambda(count_words),
)

print(
    parallel.invoke(
        {"text": "LangChain composes reusable application steps."}
    )
)
