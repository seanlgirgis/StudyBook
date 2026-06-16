# Module 2 Study Facts

## Big picture

LangChain supplies standard interfaces for prompts, messages, models, parsers, documents, retrievers, tools, and agents.

## Core components

### Language model

Usually accepts text and returns text.

### Chat model

Accepts structured messages and returns an AI message.

### Message roles

- `SystemMessage` — overall behavior and rules
- `HumanMessage` — user input
- `AIMessage` — prior model response
- `ToolMessage` — result returned by a tool

### PromptTemplate

Produces formatted text.

### ChatPromptTemplate

Produces structured chat messages.

### MessagesPlaceholder

Inserts a variable-length message history into a chat prompt.

### FewShotPromptTemplate

Combines examples, an example formatter, and the new input.

### Example selectors

- semantic similarity — examples closest in meaning
- maximal marginal relevance — balances relevance and diversity
- n-gram overlap — favors similar wording

### Output parsers

Transform model output into application-friendly data.

Examples:

- `StrOutputParser`
- comma-separated list parser
- `JsonOutputParser`
- XML parser
- CSV/DataFrame parsing patterns

### Document

A piece of content plus metadata.

### Loader

Reads a source such as PDF or webpage into documents.

### Text splitter

Breaks documents into smaller pieces.

### Embeddings and vector stores

Convert meaning into vectors and store them for similarity search.

### Retriever

Given a query, returns relevant documents.

### Memory

Stores conversation history for later turns.

### Chain

Connects components into a workflow.

### Tool

A callable capability the model or agent can use.

### Agent

Lets a model choose actions and tools dynamically.

## Course-boundary rule

Learn the names and shapes here, but defer deep implementation of loaders, splitters, embeddings, vector stores, retrievers, RAG, and agents to their dedicated later courses.
