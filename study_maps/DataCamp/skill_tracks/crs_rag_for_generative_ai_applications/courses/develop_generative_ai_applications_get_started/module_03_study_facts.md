# Module 3 Study Facts

## Big picture

Module 3 turns LangChain components into an application and introduces model-selection and Flask integration.

## Model selection factors

- task quality;
- latency;
- cost;
- context window;
- structured output;
- tool calling;
- deployment options;
- data sensitivity;
- provider risk;
- transparency and governance.

## Provider neutrality

LangChain can keep much of this stable:

```text
prompt → model → parser
```

The model adapter can often change, but advanced capabilities must be retested:

- structured output;
- tools;
- streaming;
- token metadata;
- multimodal input;
- provider-specific parameters.

## Prompting, RAG, and fine-tuning

### Prompting

Change instructions at request time.

### RAG

Retrieve outside knowledge and give it to the model as context.

### Fine-tuning

Change model behavior using training examples.

## Flask application shape

```text
browser/client
→ Flask route
→ validate request
→ invoke LangChain chain
→ return JSON response
```

## Minimal endpoint responsibilities

- accept a request;
- validate required fields;
- call application logic;
- handle errors safely;
- return a structured response.

## Production ideas introduced

- dependency pinning;
- logging;
- testing;
- monitoring;
- governance;
- deployment;
- security and input handling.

## Scope for our local application

Build a small educational Flask app. Do not turn Course 1 into a production platform.
