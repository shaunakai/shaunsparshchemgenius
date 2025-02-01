# This Program simply sends one request to OpenAI and gets a response
# Install openai package
# client = OpenAI(api_key=" PROVIDE YOUR API KEY - BUY it fitst)
# client is your OpenAI object to ask any questions to
# stream = client.chat.completions.create(...) asking AI to give you answer.
# Answer comes back as on stream. Give stream=False/True for one line or multi line response.
from openai import OpenAI
client = OpenAI(api_key="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")
#You can generate a key by signing into platform.openai.com

streamOnelineResponse = client.chat.completions.create(
#    model="gpt-4o-mini",
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "what is machine learning?"}],
    stream=False,
)
print("Beginning of one line response \n")
print(streamOnelineResponse.choices[0].message.content)
print("End of one line response \n")
#The library also supports streaming responses using Server-Side Events (SSE). Here's an example of how to stream responses:
stream = client.chat.completions.create(
#    model="gpt-4o-mini",
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "what is machine learning?"}],
    stream=True,
)
print("Begining of Stream Response")
for part in stream:
    print(part.choices[0].delta.content or "")

print("End of Strem response")

