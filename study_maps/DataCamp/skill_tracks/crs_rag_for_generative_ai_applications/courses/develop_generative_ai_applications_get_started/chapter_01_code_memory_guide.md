# Chapter 1 Code Memory Guide

## The six-part memory map

```text
Prompt
→ prepares input

Model
→ generates output

Parser
→ converts output

Chain
→ connects steps

Schema
→ validates shape

History
→ carries prior messages
```

## 1. PromptTemplate skeleton

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic}."
)

formatted = prompt.invoke(
    {"topic": "RAG"}
)

print(formatted.to_string())
```

Say it aloud:

```text
import
→ create template
→ invoke with dictionary
→ inspect formatted text
```

## 2. ChatPromptTemplate skeleton

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a patient tutor."),
        ("human", "{question}"),
    ]
)
```

Memory hook:

```text
from_template
→ one text prompt

from_messages
→ role-based messages
```

## 3. Real LCEL chain

```python
from langchain_core.output_parsers import StrOutputParser

chain = prompt | model | StrOutputParser()

result = chain.invoke(
    {"topic": "LCEL"}
)
```

Say it aloud:

```text
prepare
→ generate
→ parse
```

## 4. RunnableParallel skeleton

```python
from langchain_core.runnables import RunnableLambda, RunnableParallel

parallel = RunnableParallel(
    uppercase=RunnableLambda(uppercase_text),
    word_count=RunnableLambda(count_words),
)

result = parallel.invoke(
    {"text": "LangChain composes reusable steps."}
)
```

Memory hook:

```text
names on the left
→ output dictionary keys

branches on the right
→ independent runnables

all branches
→ receive the same input
```

## 5. JSON parser skeleton

```python
from langchain_core.output_parsers import JsonOutputParser

parser = JsonOutputParser(
    pydantic_object=TopicSummary
)

prompt = PromptTemplate(
    template="Explain {topic}.\n{format_instructions}",
    input_variables=["topic"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    },
)

chain = prompt | model | parser
```

Memory hook:

```text
get_format_instructions
→ tell the model the shape

JsonOutputParser
→ parse response into dict
```

## 6. Provider-native structured output

```python
structured_model = model.with_structured_output(
    TopicSummary
)

chain = prompt | structured_model

result = chain.invoke(
    {"topic": "prompt templates"}
)

print(result.topic)
print(result.model_dump())
```

Memory hook:

```text
with_structured_output
→ schema-aware model

result.topic
→ attribute access

model_dump
→ convert to dict
```

## 7. MessagesPlaceholder skeleton

```python
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Use prior context."),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)
```

Invoke with:

```python
chain.invoke(
    {
        "history": history,
        "question": question,
    }
)
```

Then append:

```python
history.append(HumanMessage(content=question))
history.append(AIMessage(content=answer))
```

## 8. Provider comparison skeleton

```python
openai_chain = prompt | openai_model | parser
watsonx_chain = prompt | watsonx_model | parser

openai_result = openai_chain.invoke(input_data)
watsonx_result = watsonx_chain.invoke(input_data)
```

What stays stable:

```text
prompt
parser
input
chain shape
```

What changes:

```text
model adapter
credentials
model ID
provider parameters
```

## High-risk confusion review

```text
prompt.invoke
→ formats

model.invoke
→ generates

chain.invoke
→ runs everything
```

```text
PromptTemplate
→ text

ChatPromptTemplate
→ messages
```

```text
JsonOutputParser
→ dict

with_structured_output(PydanticModel)
→ validated Pydantic object
```

```text
sequence
→ later step depends on earlier output

parallel
→ independent branches share the same input
```
