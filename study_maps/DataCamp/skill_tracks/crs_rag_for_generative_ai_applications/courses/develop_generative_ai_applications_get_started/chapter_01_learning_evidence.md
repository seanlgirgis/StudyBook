# Chapter 1 Learning Evidence

## Successfully validated

| Area | Evidence |
|---|---|
| PromptTemplate | One-variable and multi-variable formatted prompts printed successfully |
| ChatPromptTemplate | System and Human message objects were created |
| Few-shot prompting | Prefix, formatted examples, suffix, and runtime request assembled correctly |
| LCEL local pipeline | Prompt, local runnable, and parser executed as one chain |
| OpenAI LCEL | Real OpenAI model returned an LCEL explanation |
| Watsonx connectivity | IBM Cloud API key, project ID, London endpoint, and Lite Runtime worked |
| Provider comparison | Same prompt, parser, input, and chain shape ran against OpenAI and Watsonx |
| RunnableParallel | Uppercase and word-count branches returned a combined dictionary |
| JsonOutputParser | Real model JSON parsed into a Python `dict` |
| Structured output | Three inputs returned validated `TopicSummary` objects |
| MessagesPlaceholder | Prior messages resolved the meaning of “it” |
| Manual history | Human and AI turns were appended correctly |
| Reusable history function | One function performed invocation and history updates |
| Session history wrapper | Separate Sean and Anna histories worked; deprecation warning observed |

## Important corrections discovered

1. `PromptTemplate.invoke()` does not call the model.
2. The meaning of `.invoke()` depends on the object receiving the call.
3. `input_variables=["request"]` declares runtime values for `FewShotPromptTemplate`.
4. Provider-neutral chains do not guarantee identical model interpretation.
5. Watsonx model availability is regional and account-specific.
6. The requested Granite model was unavailable; the listed Mistral model worked.
7. London used `https://eu-gb.ml.cloud.ibm.com`.
8. `max_tokens`, not the earlier attempted parameter shape, removed the Watsonx default warning.
9. The third-party license warning can be selectively suppressed, but broad warning suppression should be avoided.
10. `RunnableWithMessageHistory` is deprecated in the installed version and should remain optional legacy enrichment.

## Reinforcement targets

- write imports from memory;
- distinguish the three `.invoke()` calls;
- reconstruct `PromptTemplate.from_template()`;
- reconstruct `ChatPromptTemplate.from_messages()`;
- remember `MessagesPlaceholder("history")`;
- remember `prompt | model | parser`;
- distinguish `dict` access from Pydantic attribute access;
- explain sequence versus parallel;
- explain provider neutrality without claiming identical model behavior.
