# Chapter 1 and LangChain Learning Evidence

## Local examples completed

- PromptTemplate with one variable
- PromptTemplate with several variables
- ChatPromptTemplate with system and human messages
- FewShotPromptTemplate classification pattern
- LCEL local-function demonstration
- Real OpenAI LCEL pipeline
- Real Watsonx smallest test
- OpenAI and Watsonx provider-switching comparison
- RunnableParallel with independent branches
- JsonOutputParser returning a dictionary
- Provider-native structured output returning TopicSummary
- MessagesPlaceholder with prior conversation
- Manual history growth
- Reusable chat function with history
- RunnableWithMessageHistory legacy comparison

## Important observed lessons

- `prompt.invoke()` formats a prompt.
- `model.invoke()` generates a model response.
- `chain.invoke()` executes the complete pipeline.
- Provider-neutral structure does not guarantee identical interpretation.
- Clear context prevented Watsonx from interpreting LCEL as liquid cooling.
- `JsonOutputParser` returned a `dict`.
- `with_structured_output(TopicSummary)` returned a validated `TopicSummary`.
- In-memory history disappears when the process ends.
- `RunnableWithMessageHistory` worked but emitted a deprecation warning; it remains enrichment rather than core curriculum.
