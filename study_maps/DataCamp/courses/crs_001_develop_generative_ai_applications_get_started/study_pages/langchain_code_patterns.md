# LangChain Code Patterns

## Imports

```python
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
```

## PromptTemplate

```python
prompt = PromptTemplate.from_template(
    "Explain {topic} to a {audience}."
)
formatted = prompt.invoke(
    {"topic": "RAG", "audience": "beginner"}
)
```

## ChatPromptTemplate

```python
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a patient tutor."),
        ("human", "{question}"),
    ]
)
```

## LCEL

```python
chain = prompt | model | StrOutputParser()
result = chain.invoke({"question": "What is LCEL?"})
```

## RunnableParallel

```python
parallel = RunnableParallel(
    uppercase=RunnableLambda(uppercase_text),
    word_count=RunnableLambda(count_words),
)
result = parallel.invoke({"text": "LangChain composes steps."})
```

## Structured output

```python
class TopicSummary(BaseModel):
    topic: str
    explanation: str

structured_model = model.with_structured_output(TopicSummary)
chain = prompt | structured_model
result = chain.invoke({"topic": "prompt templates"})
print(result.topic)
```

## Conversation history

```python
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Use prior conversation context."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)
```

## Provider switching

```python
openai_chain = prompt | openai_model | parser
watsonx_chain = prompt | watsonx_model | parser
```

The pipeline shape stays stable; the provider adapter changes.
