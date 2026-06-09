from openai_support import OpenAIService, RequestOptions


ai = OpenAIService()

prompt = """
Suggest one possible cause for this incident:

A dashboard became slow immediately after a deployment.
Database CPU remained normal.
Application errors increased.
Rolling back restored normal performance.

Return one short hypothesis only.
"""

print("TEMPERATURE 0\n")
print(
    ai.get_response(
        prompt=prompt,
        options=RequestOptions(temperature=0.0),
    )
)

print("\n" + "=" * 60 + "\n")

print("TEMPERATURE 0.7\n")

for run_number in range(1, 4):
    response = ai.get_response(
        prompt=prompt,
        options=RequestOptions(temperature=0.7),
    )

    print(f"Run {run_number}: {response}")