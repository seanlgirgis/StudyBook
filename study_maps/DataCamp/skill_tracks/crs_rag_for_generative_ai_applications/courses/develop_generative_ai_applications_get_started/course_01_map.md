# Course 1 Map — Develop Generative AI Applications: Get Started

## Four-layer learning model

```text
Theory reinforcement
→ understand why the components exist

Code-memory guide
→ remember how to construct them

Starter code
→ prove the patterns run

RemNote
→ strengthen recall
```

## Complete application shape

```text
changing input
→ prompt template or chat prompt
→ provider model adapter
→ output parser or schema
→ usable application result
```

## Chapter 1 preparation completed locally

```text
PromptTemplate
→ ChatPromptTemplate
→ FewShotPromptTemplate
→ LCEL
→ RunnableLambda
→ RunnableParallel
→ real OpenAI call
→ real IBM watsonx call
→ JSON parser
→ Pydantic structured output
→ MessagesPlaceholder
→ manual conversation history
```

## Important proven lessons

- Prompt invocation formats input; chain invocation runs the complete workflow.
- The same LCEL structure can use different provider adapters.
- Provider neutrality does not mean identical interpretation or wording.
- Clear context prevented Watsonx from interpreting LCEL as a liquid-cooling acronym.
- JSON parsing returned a `dict`.
- Provider-native structured output returned a validated Pydantic object.
- One chain can be constructed once and invoked for many runtime inputs.
- Conversation history can be inserted with `MessagesPlaceholder`.
- In-memory history disappears when the process ends.
- `RunnableWithMessageHistory` is now legacy enrichment; LangGraph persistence belongs in later study.

## Course execution order

```text
Chapter 1 concept study
→ RemNote comprehensive learning deck
→ tested local examples
→ RemNote coding and reinforcement deck
→ strengthened documentation
→ Coursera labs and quizzes
→ lab corrections and final reconciliation
```

## Course boundary

Deep RAG, vector stores, agents, and LangGraph persistence remain later topics. This course should introduce their place in the architecture without turning Chapter 1 into a separate framework course.

## Theory coverage added

- AI, machine learning, generative AI, and discriminative AI.
- Foundation models and why organizations use them.
- LLMs as language-focused foundation models.
- Prompt engineering techniques and trade-offs.
- Why LangChain exists, its benefits, and when a direct SDK may be simpler.
- LCEL, runnables, sequence, parallelism, and coercion.
- Plain text, JSON parsing, schemas, and provider-native structured output.
- Provider abstraction versus provider-identical behavior.
- Conversation history as application-managed state.
