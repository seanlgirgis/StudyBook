# Module 1 Study Facts — Expanded

> Start with `chapter_01_theory_reinforcement_guide.html` for the full conceptual story. Use this file as the condensed fact and code reference.

## Big picture

A reusable generative-AI application often follows this shape:

```text
runtime input
→ prompt or chat prompt
→ model
→ parser or structured-output layer
→ usable application result
```

## Prompt construction

### `PromptTemplate`

Use it when the provider can receive one formatted text prompt.

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template(
    "Explain {topic} to a {audience} using {tone} language."
)

formatted = prompt.invoke(
    {
        "topic": "vector embeddings",
        "audience": "beginner",
        "tone": "friendly",
    }
)
```

Memory rule:

```text
PromptTemplate.from_template()
→ create the reusable recipe

prompt.invoke({...})
→ fill the variables

formatted.to_string()
→ inspect the completed text
```

### `ChatPromptTemplate`

Use it when you need role-based messages.

```python
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a patient technical tutor."),
        ("human", "Explain {topic} in {sentence_count} sentences."),
    ]
)
```

`prompt.invoke(...)` creates `SystemMessage` and `HumanMessage` objects. It does not call the model.

## The three meanings of `.invoke()`

The object before `.invoke()` determines the behavior:

```text
prompt.invoke(...)
→ prepare the prompt or messages

model.invoke(...)
→ call the model

chain.invoke(...)
→ run the entire connected pipeline
```

## Few-shot prompting

`FewShotPromptTemplate` combines:

```text
prefix
→ formatted examples
→ suffix containing the new request
```

`input_variables=["request"]` declares what the caller must provide at runtime.

## LCEL

LangChain Expression Language connects runnable components:

```python
chain = prompt | model | parser
```

The chain is created once and can be invoked repeatedly with different inputs.

## `RunnableLambda` and automatic coercion

```text
RunnableLambda(function)
→ explicit runnable wrapper

automatic coercion
→ LangChain wraps a compatible callable for you
```

Use explicit `RunnableLambda` for an important named or reusable step. Automatic coercion is convenient for tiny one-off functions.

## `RunnableParallel`

Independent branches receive the same original input:

```python
parallel = RunnableParallel(
    uppercase=RunnableLambda(uppercase_text),
    word_count=RunnableLambda(count_words),
)
```

The argument names become keys in the result dictionary.

## Output handling

### `StrOutputParser`

Converts an AI message into a plain Python string.

### `JsonOutputParser`

Adds JSON format instructions and parses the response into a dictionary.

```python
result["topic"]
```

### Provider-native structured output

```python
structured_model = model.with_structured_output(TopicSummary)
result = structured_model.invoke(...)
```

This returned a validated `TopicSummary` object:

```python
result.topic
result.explanation
result.model_dump()
```

## Provider switching lesson

The same prompt, parser, input, and LCEL shape were run against:

```text
ChatOpenAI
ChatWatsonx
```

Provider-neutral plumbing does not guarantee identical model interpretation. The Watsonx model first interpreted `LCEL` as liquid cooling until the prompt supplied the full phrase and LangChain context.

## Conversation history

`MessagesPlaceholder("history")` inserts a variable-length list of earlier messages.

Manual history pattern:

```python
history.append(HumanMessage(content=question))
history.append(AIMessage(content=answer))
```

The history exists only in memory unless it is stored elsewhere.

`RunnableWithMessageHistory` was tested as optional legacy enrichment, but the installed LangChain version reports that it is deprecated in favor of LangGraph persistence.

## Self-consistency

Layman memory rule:

```text
ask several times
→ compare candidate answers
→ choose the strongest agreement
```

It may improve reliability, but it costs more and takes longer.
