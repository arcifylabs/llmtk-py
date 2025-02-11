# llmtk (LLM Toolkit)

> Stop writing JSON schemas for your AI functions. Let Python types do it for you. ⚡️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

## Features

- 🎯 **Zero Schema Maintenance**: Your Python types become your OpenAI schemas
- ✨ **Type Safety**: Catch invalid AI responses before they break your code
- 📝 **Rich Types**: Support for Pydantic models, lists, and custom types
- 🚀 **Quick Setup**: One decorator is all you need

## Without llmtk, you write this:


```python
# Define your function
def get_weather(city: str) -> str:
    return f"Weather in {city}: Sunny"

# Manually maintain OpenAI function schema
weather_schema = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather information for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "Name of the city"
                }
            },
            "required": ["city"]
        }
    }
}

# Hope the schema stays in sync with your function
tools = [weather_schema]
```

## With llmtk, just write this:

```python
from llmtk import register_function, get_openai_tools

@register_function
def get_weather(city: str) -> str:
    """Get weather information for a city"""
    return f"Weather in {city}: Sunny"

# Schema automatically generated from your Python types
tools = get_openai_tools()
```

## Quick Start

```bash
pip install llmtk
```

```python
from llmtk import register_function, call_function, get_openai_tools

@register_function
def calculate_price(quantity: int, unit_price: float) -> float:
    """Calculate total price for items"""
    return quantity * unit_price

# Get schema for OpenAI
tools = get_openai_tools()

# Use with OpenAI
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Calculate price for 5 items at $10 each"}],
    tools=tools,
    tool_choice="auto"
)

# Safe function execution with validation
result = call_function(
    response.choices[0].message.tool_calls[0].function.name,
    response.choices[0].message.tool_calls[0].function.arguments
)

if isinstance(result, tuple):
    print(f"Validation error: {result[0]}")
else:
    print(f"Total: ${result:.2f}")  # Total: $50.00
```
## License

MIT License - feel free to use in your projects!
