"""
Core functionality for LLMTK - function registration, validation, and schema generation.
"""

import inspect
import json
from typing import Annotated, Any, Optional, Tuple, Union, get_args, get_origin

from pydantic import BaseModel, Field, ValidationError, create_model

# Function Registry
registry = {}


def map_type(annotation):
    """Maps Python types to OpenAI-compatible JSON schema types."""
    if annotation is int:
        return "integer"
    elif annotation is str:
        return "string"
    elif annotation is bool:
        return "boolean"
    elif annotation is float:
        return "number"
    elif annotation is list or get_origin(annotation) is list:
        item_type = get_args(annotation)[0] if get_args(annotation) else Any
        return {"type": "array", "items": map_type(item_type)}
    elif annotation is dict or get_origin(annotation) is dict:
        return {"type": "object"}
    elif isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return annotation.model_json_schema()
    return "string"  # Default to string if unknown


def register_function(func):
    """
    Register a function and auto-generate an OpenAI-compatible JSON schema.

    Args:
        func: The function to register. Must have type hints for all parameters.

    Returns:
        The original function, unmodified.

    Raises:
        ValueError: If any parameter is missing a type annotation.
    """
    sig = inspect.signature(func)

    fields = {}
    required_fields = []

    for name, param in sig.parameters.items():
        if param.annotation is param.empty:
            raise ValueError(
                f"Parameter '{name}' in function '{func.__name__}' is missing a type annotation."
            )

        annotation = param.annotation
        param_type = annotation
        param_desc = name.replace("_", " ").capitalize()  # Default description

        if get_origin(annotation) is Annotated:
            args = get_args(annotation)
            param_type = args[0]  # First argument is always the actual type
            param_desc = (
                args[1] if len(args) > 1 else param_desc
            )  # Second argument is the description

        field_params = {"description": param_desc}

        if param.default is not param.empty:
            field_params["default"] = param.default
        else:
            required_fields.append(name)

        fields[name] = (param_type, Field(**field_params))

    Model = create_model(f"{func.__name__}Model", **fields)
    json_schema = Model.model_json_schema()
    json_schema.pop("title", None)  # Remove unnecessary title

    generated_schema = {
        "name": func.__name__,
        "description": inspect.getdoc(func) or "No description available.",
        "parameters": {
            "type": "object",
            "properties": {
                key: {**value, "type": map_type(fields[key][0])}
                for key, value in json_schema["properties"].items()
            },
            "required": required_fields,
        },
    }

    registry[func.__name__] = {
        "function": func,
        "model": Model,
        "generated_schema": generated_schema,
    }

    return func


def call_function(
    func_name: str, payload: Union[str, dict]
) -> Union[Any, Tuple[str, dict]]:
    """
    Validates input payload against the registered function's schema and executes the function.

    Args:
        func_name: Name of the registered function to call
        payload: Input data to validate and pass to the function. Can be a JSON string or dict.

    Returns:
        On success: The result of the function execution
        On failure: Tuple of (error_message, validation_schema) for retry handling

    Raises:
        ValueError: If the function is not registered
    """
    if func_name not in registry:
        raise ValueError(f"Function '{func_name}' is not registered.")

    entry = registry[func_name]
    model = entry["model"]
    schema = entry["generated_schema"]

    # Parse JSON if payload is a string
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError as e:
            return (
                f"Invalid JSON in payload: {str(e)}",
                {"error": str(e), "schema": schema, "received_payload": payload},
            )

    # At this point, payload is guaranteed to be a dict
    payload_dict: dict = payload  # type: ignore

    try:
        validated_data = model(**payload_dict)

        # Check for extra fields in payload that are not in the function schema
        extra_fields = set(payload_dict.keys()) - set(
            schema["parameters"]["properties"].keys()
        )
        if extra_fields:
            raise ValueError(
                f"Unexpected fields found in payload: {', '.join(extra_fields)}"
            )

        return entry["function"](**validated_data.model_dump())
    except ValidationError as e:
        # Return error details that can be used for retry if needed
        return (
            f"Validation failed: {str(e)}",
            {"error": str(e), "schema": schema, "received_payload": payload_dict},
        )


def get_openai_tools():
    """Get OpenAI-compatible tools array for chat completion API."""
    return [
        {
            "type": "function",
            "function": {
                "name": f["generated_schema"]["name"],
                "description": f["generated_schema"]["description"],
                "parameters": f["generated_schema"]["parameters"],
            },
        }
        for f in registry.values()
    ]
