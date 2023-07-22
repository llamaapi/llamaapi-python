# LlamaAPI SDK

LlamaAPI is a Python SDK for interacting with the Llama API. It abstracts away the handling of aiohttp sessions and headers, allowing for a simplified interaction with the API.

## Installation
You can install the LlamaAPI SDK using pip:

```python
pip install llamaapi
```

## Usage
After installing the SDK, you can use it in your Python projects like so:

```python
from llamaapi import llamaapi

# Initialize the llamaapi with your api_token
llama = LlamaAPI('<your_api_token>')

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
              "description": "The city and state, e.g. San Francisco, CA"
            },
            "days": {
              "type": "number",
              "description": "for how many days ahead you wants the forecast"
            },
            "unit": {
              "type": "string",
              "enum": ["celsius", "fahrenheit"]
            }
          }
      },
      "required": ["location", "days"]
    }
  ],
  "stream": False,
  "function_call": "get_current_weather"
}

# Make your request and handle the response
response = llama.run(api_request_json)
print(seq)
```

Note: Stream is still not working, so it is recommended to submit with `stream: False`.

## Change Log
Version 0.1: Initial release

## Contributing
We welcome contributions to this project. Please see the Contributing Guidelines for more details.

## License
llamaapi SDK is licensed under the MIT License. Please see the License File for more details.