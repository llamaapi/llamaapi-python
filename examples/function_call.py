import json
from llamaapi import LlamaAPI

# Initialize the llamaapi with your api_token
llama = LlamaAPI("<your_api_token>")

# Define your API request
api_request_json = {
    "messages": [
        {"role": "user", "content": "What is the weather like in Boston?"},
    ],
    "functions": [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "days": {
                        "type": "number",
                        "description": "for how many days ahead you wants the forecast",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
            },
            "required": ["location", "days"],
        }
    ],
    "stream": False,
    "function_call": "get_current_weather",
}

# Make your request and handle the response
response = llama.run(api_request_json)
print(json.dumps(response.json(), indent=2))
