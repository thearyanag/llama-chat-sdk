import requests
import json
from datetime import datetime
from typing import List, Dict, Optional, Callable, Any, Union
from enum import Enum

class LlamaModel(str, Enum):
    LLAMA_1B = "meta-llama/llama-3.2-1b-instruct/fp-8"
    LLAMA_3B = "meta-llama/llama-3.2-3b-instruct/fp-8"
    LLAMA_8B = "meta-llama/llama-3.1-8b-instruct/fp-8"
    LLAMA_70B = "meta-llama/llama-3.1-70b-instruct/fp-8"

class Function:
    def __init__(self, name: str, func: Callable, description: str):
        self.name = name
        self.func = func
        self.description = description
        # Get the function's parameters
        self.parameters = func.__code__.co_varnames[:func.__code__.co_argcount]

class LlamaChat:
    def __init__(
        self,
        api_key: str,
        model: Union[LlamaModel, str] = LlamaModel.LLAMA_8B,
        debug: bool = False
    ):
        """
        Initialize the LlamaChat SDK.
        
        Args:
            api_key (str): Your API key for authentication
            model (Union[LlamaModel, str]): The Llama model to use
            debug (bool): Whether to enable debug logging
        """
        self.api_key = api_key
        self.model = model if isinstance(model, str) else model.value
        self.debug = debug
        self.api_url = "https://api.inference.net/v1/chat/completions"
        self.functions: Dict[str, Function] = {}
        self.messages = []
        self._initialize_system_message()

    def _initialize_system_message(self):
        """Initialize the system message with available functions."""
        system_content = "You are a helpful assistant."
        if self.functions:
            system_content += " You have access to the following functions:\n\n"
            for idx, (name, func) in enumerate(self.functions.items(), 1):
                system_content += f"{idx}. {name}{func.parameters}: {func.description}\n"
            
            system_content += ("\nWhen you need to use a function, output a JSON object "
                             "in the following format:\n\n"
                             "{\n  \"function\": \"function_name\",\n  \"arguments\": "
                             "{\n    \"arg1\": \"value1\",\n    \"arg2\": \"value2\"\n  }\n}\n")

        self.messages = [{"role": "system", "content": system_content}]

    def register_function(self, func: Callable, description: str):
        """
        Register a function that can be called by the AI.
        
        Args:
            func (Callable): The function to register
            description (str): Description of what the function does
        """
        function = Function(func.__name__, func, description)
        self.functions[func.__name__] = function
        self._initialize_system_message()

    def register_functions(self, functions: List[Dict[str, Any]]):
        """
        Register multiple functions at once.
        
        Args:
            functions (List[Dict]): List of dictionaries containing function and description
        """
        for func_info in functions:
            self.register_function(func_info['function'], func_info['description'])

    def _call_api(self, messages: List[Dict[str, str]]) -> Optional[str]:
        """Make an API call to the Llama chat endpoint."""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            response_data = response.json()
            
            if self.debug:
                debug_filename = f"response-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.json"
                with open(debug_filename, "w") as f:
                    json.dump({"response": response_data, "messages": messages}, f)
                    
            return response_data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            if self.debug:
                print(f"API call failed: {str(e)}")
            return None

    def _parse_function_call(self, response_text: str) -> Optional[Dict]:
        """Parse the response text to check for function calls."""
        try:
            function_call = json.loads(response_text)
            if "function" in function_call and "arguments" in function_call:
                return function_call
        except json.JSONDecodeError:
            pass
        return None

    def _execute_function(self, function_call: Dict) -> str:
        """Execute the called function with the provided arguments."""
        function_name = function_call["function"]
        arguments = function_call["arguments"]
        
        if function_name in self.functions:
            return self.functions[function_name].func(**arguments)
        return "Error: Function not recognized."

    def chat(self, message: str) -> str:
        """
        Send a message to the AI and get a response.
        
        Args:
            message (str): The user's message
            
        Returns:
            str: The AI's response
        """
        self.messages.append({"role": "user", "content": message})
        
        assistant_response = self._call_api(self.messages)
        if assistant_response is None:
            self.messages.pop()
            return "Sorry, I encountered an error. Please try again."
            
        function_call = self._parse_function_call(assistant_response)
        
        if function_call:
            function_result = self._execute_function(function_call)
            self.messages.append({"role": "assistant", "content": function_result})
            return function_result
        else:
            self.messages.append({"role": "assistant", "content": assistant_response})
            return assistant_response