# LlamaChat SDK

A Python SDK for interacting with Llama language models through a chat interface. This SDK provides a simple way to integrate Llama's powerful language models into your applications, with support for function calling and various model sizes.

## Features

- 🤖 Easy integration with Llama language models
- 🔄 Support for multiple model sizes (1B, 3B, 8B, and 70B parameters)
- 🛠️ Function registration and calling capabilities
- 🐞 Debug mode for troubleshooting
- 💬 Conversation history management
- 🔌 Simple API interface

## Installation

```bash
pip install llamachat-sdk
```

## Quick Start

```python
from run import LlamaChat, LlamaModel

# Initialize the chat client
chat = LlamaChat(
    api_key="your_api_key_here",
    model=LlamaModel.LLAMA_8B,
    debug=False
)

# Send a message and get a response
response = chat.chat("Hello, how are you?")
print(response)
```

## Available Models

The SDK supports the following Llama models:

- `LLAMA_1B`: 1 billion parameter model
- `LLAMA_3B`: 3 billion parameter model
- `LLAMA_8B`: 8 billion parameter model (default)
- `LLAMA_70B`: 70 billion parameter model

## Function Registration

You can register custom functions that the AI can call:

```python
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny!"

# Register a single function
chat.register_function(
    func=get_weather,
    description="Get the current weather for a given city"
)

# Register multiple functions
functions = [
    {
        "function": get_weather,
        "description": "Get the current weather for a given city"
    },
    # Add more functions as needed
]
chat.register_functions(functions)
```

## Advanced Usage

### Debug Mode

Enable debug mode to log API responses:

```python
chat = LlamaChat(
    api_key="your_api_key_here",
    model=LlamaModel.LLAMA_8B,
    debug=True
)
```

### Custom Model Selection

Use a custom model string if needed:

```python
chat = LlamaChat(
    api_key="your_api_key_here",
    model="custom-model-identifier"
)
```

### Function Calling Example

```python
# Register a function
def calculate_sum(a: int, b: int) -> int:
    return a + b

chat.register_function(
    calculate_sum,
    "Calculate the sum of two numbers"
)

# The AI can now use this function
response = chat.chat("What is 5 plus 3?")
# The AI might respond with a function call to calculate_sum(5, 3)
```

## API Reference

### LlamaChat Class

```python
class LlamaChat:
    def __init__(
        self,
        api_key: str,
        model: Union[LlamaModel, str] = LlamaModel.LLAMA_8B,
        debug: bool = False
    )
```

#### Parameters:
- `api_key` (str): Your API authentication key
- `model` (Union[LlamaModel, str]): The Llama model to use
- `debug` (bool): Enable debug logging

#### Methods:

- `chat(message: str) -> str`: Send a message and get a response
- `register_function(func: Callable, description: str)`: Register a single function
- `register_functions(functions: List[Dict[str, Any]])`: Register multiple functions

## Error Handling

The SDK includes built-in error handling for:
- API connection issues
- Invalid function calls
- Response parsing errors

## Development

The source code is available in the `run.py` file. To contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.