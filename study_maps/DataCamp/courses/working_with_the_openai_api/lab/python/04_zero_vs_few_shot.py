from openai import OpenAI

client = OpenAI()

zero_shot_prompt = """
Classify this review as Positive or Negative:

"The battery lasts all day."
"""

few_shot_prompt = """
Classify each review as Positive or Negative.
Return only the label.

"Excellent quality." = Positive
"Very disappointing." = Negative

"The battery lasts all day." =
"""

for label, prompt in [
    ("Zero-shot", zero_shot_prompt),
    ("Few-shot", few_shot_prompt),
]:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print(f"\n{label}")
    print(response.choices[0].message.content)