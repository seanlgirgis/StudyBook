import os

from openai import OpenAI


def generate_response(query: str, context_sections: str) -> str:
    """
    Uses OpenAI when OPENAI_API_KEY is set, otherwise returns a deterministic simulated answer.
    """
    if not os.getenv("OPENAI_API_KEY"):
        context_hint = context_sections.strip()
        if context_hint:
            return (
                "Thanks for the details. Based on what you described, this sounds like a service request we can help with. "
                f"Here is the most relevant guidance from our knowledge base: {context_hint[:260]}"
            )
        return (
            "Thanks for sharing that. I could not find a confident match in the current knowledge base, "
            "so the best next step is to clarify the service type (AC, heating, plumbing, or water heater) and the main symptom."
        )

    client = OpenAI()
    prompt = (
        "Answer the question based on the context below.\n\n"
        f"{context_sections}\n\n"
        f"Question: {query}"
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    return response.choices[0].message.content or ""
