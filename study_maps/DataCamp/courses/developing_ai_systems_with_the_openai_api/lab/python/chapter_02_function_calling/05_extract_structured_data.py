import json

from openai import OpenAI


client = OpenAI()


job_tool = {
    "type": "function",
    "function": {
        "name": "extract_job_information",
        "description": (
            "Extract the job title and office location "
            "from a hiring announcement."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "job_title": {
                    "type": "string",
                    "description": "The advertised job title.",
                },
                "location": {
                    "type": "string",
                    "description": "The city or office location.",
                },
            },
            "required": [
                "job_title",
                "location",
            ],
            "additionalProperties": False,
        },
    },
}


response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": (
                "We are hiring a Data Scientist "
                "for our Berlin office."
            ),
        }
    ],
    tools=[job_tool],
    tool_choice="auto",
)


message = response.choices[0].message

if not message.tool_calls:
    raise ValueError(
        "The model did not return a tool call."
    )


tool_call = message.tool_calls[0]

print("Selected function:")
print(tool_call.function.name)

print("-" * 50)

print("Raw arguments:")
print(tool_call.function.arguments)

print("-" * 50)

arguments = json.loads(
    tool_call.function.arguments
)

print("Parsed Python dictionary:")
print(arguments)

print("-" * 50)

print("Job title:")
print(arguments["job_title"])

print("Location:")
print(arguments["location"])