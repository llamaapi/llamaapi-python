from llamaapi import LlamaAPI

llama = LlamaAPI('LL-5DKCFdHZHBFNwk41oiALtT62ppvcuasponeqowinasdkkasasjsjsfj')


# API Request JSON Cell
api_request_json = {
  "messages": [
    {"role": "user", "content": "Search flight options from San Francisco to Paris between December 8-15."},
  ],
  "functions": [
    {
      "name": "Trip_search_flight_ticket",
      "description": "You are a travel assistant that always utilizes the Trip plugin to deliver precise travel recommendations.",
      "parameters": {
        "type": "object",
        "properties": {
          "originCityCode": {
            "type": "string",
          },
          "destinationCityCode": {
            "type": "string",
          },
          "departureDate": {
            "type": "string",
            "description": "The format of the field should be yyyy-MM-dd"
          },
          "returnDate": {
            "type": "string",
            "description": "The format of the field should be yyyy-MM-dd"
          },
          "locale": {
            "type": "string",
          },
          "oneWayOrRoundTrip": {
            "type": "string",
          },
          "originalInput": {
            "type": "string",
            "description": "The user's original input"
          },
          "originalInputInEnglish": {
            "type": "string",
            "description": "The user's original input, translate to english."
          }
        },
        "stream": False,
        "required": []
      }
    }
  ],
  "stream": True,
  "function_call": {"name": "Trip_search_flight_ticket"},#"force",
  "max_tokens": 800,
}



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
  "stream": True,
  "function_call": "get_current_weather"
}


import asyncio
# Run the streaming API and print each received message
async def print_stream():
    async for seq in llama.run(api_request_json):
        print(seq)

# Run the print_stream() coroutine
asyncio.run(print_stream())