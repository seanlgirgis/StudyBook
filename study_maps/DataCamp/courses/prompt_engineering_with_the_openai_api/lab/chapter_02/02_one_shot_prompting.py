from openai_support import Message, OpenAIService


ai = OpenAIService()

messages = [
    Message(
        role="system",
        content="""You are an expert reviws sentiment classifier. 
        Classify the sentiment of this review as Positive, Negative, or Neutral.
        Return only the label without any explanation.""",
    ),
    
    Message(
        role="user",
        content="Classify the sentiment: The service was excellent.",
    ),
    Message(
        role="assistant",
        content="Positive",
    ),
    Message(
        role="user",
        content="Classify the sentiment: The delivery was late and the box was damaged.",
    ),
]

response = ai.get_response(messages=messages)

print(response)