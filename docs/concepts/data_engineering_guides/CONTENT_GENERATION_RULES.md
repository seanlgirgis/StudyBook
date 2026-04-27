# Content Generation Rules — First Swipe

## 1. Interaction Trigger
The user will request content using the following simplified "Skill" format:
`First_Swipe: <TOPIC_NAME>`

*   **TOPIC_NAME**: The technology or concept (e.g., `PySpark`, `Redshift`).
*   **The Agent Will**:
    1.  Check the file list to determine the next available **DOC_NUMBER**.
    2.  Automatically generate **Type A** (Concepts) as `<DOC_NUMBER>.<TopicName>.md`.
    3.  Automatically generate **Type B** (Interview Questions) as `<DOC_NUMBER+1>.<TopicName>.Q.md`.
    4.  Update `task.md` to track the new files.

**Example**:
User: `First_Swipe: PySpark`
Agent: Creates `00020.PySpark.md` AND `00021.PySpark.Q.md`.

---

## 2. Type A: High-Level Concepts
*   **Filename**: `<DOC_NUMBER>.<TopicName>.md` (e.g., `00020.PySpark.md`)
*   **Title**: `# <Topic Name>` followed by `### The English Version`.
*   **Tone**: "Plain English," conversational but professional. Focus on *why* it exists before *how* it works. Use Capital One (financial services) analogies where possible.

### Structure
1.  **What is it and Why Does it Exist?**
    *   Start with the problem it solves (e.g., "Python was slow...").
    *   Explain the historical context if relevant.
2.  **Core Concepts in Plain English**
    *   Define key terms (RDD, DataFrame, Catalyst, Tungsten) using simple analogies.
    *   **Formatting**: **Bold** terms, standard text definitions.
3.  **Architecture / Deep Dive**
    *   Explain the internal mechanics (Driver, Executor, Slot, Shuffle).
4.  **<Topic> at Capital One**
    *   Specific use cases (ETL, Feature Engineering).
5.  **Comparison Table**
    *   Contrast with the "Old Way" (MapReduce) or alternative technologies (Pandas).
    *   Use Markdown tables.

### Visuals
*   Use ASCII diagrams for architectural flows.
*   **Style**: Use box drawing characters (`╔`, `═`, `║`, `╚`) for clean, professional borders.

---

## 3. Type B: Top Interview Questions
*   **Filename**: `<DOC_NUMBER+1>.<TopicName>.Q.md` (e.g., `00021.PySpark.Q.md`)
*   **Title**: `# Mock Interview — <Topic Name>`

### Structure Per Question
Each question **MUST** follow this exact format:

#### 1. The Question
*   Header: `## Question X — <Level>`
*   Bold text of the question.

#### 2. Feedback First
*   Header: `# Feedback First`
*   **Subheader**: `## What You Nailed ✅`
*   **Subheader**: `## What to Tighten Up 🔧`
    *   Bullet points highlighting missing depth, nuance, or specific keywords.

#### 3. Model Answer
*   Header: `# Model Answer`
*   Use a separator `---`.
*   Provide a spoken-word, professional answer (Lead Engineer persona).

#### 4. Diagrams
*   Header: `# Diagrams`
*   ASCII art illustrating the specific concept discussed in the answer.

---

## 4. General Formatting Guidelines
*   **Separators**: Use `---` between major sections.
*   **Tone**: Authoritative yet accessible. Mentor-like.
