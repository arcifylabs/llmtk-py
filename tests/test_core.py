"""
Tests for LLMTK core functionality.
"""

from typing import Annotated, List

import pytest
from pydantic import BaseModel

from llmtk import call_function, get_openai_tools, register_function


# Test Models
class UserAddress(BaseModel):
    street: str
    city: str
    zip_code: int


# Test Functions
@register_function
def greet_user(name: Annotated[str, "User's name"]) -> str:
    """Simple greeting function."""
    return f"Hello, {name}!"


@register_function
def complex_function(
    user_id: Annotated[int, "User ID"],
    address: Annotated[UserAddress, "User's address"],
    tags: Annotated[List[str], "User tags"],
) -> dict:
    """Complex function with nested types."""
    return {
        "id": user_id,
        "address": address,  # Pydantic model will handle the conversion
        "tags": tags,
    }


def test_simple_function_valid():
    """Test simple function with valid input."""
    result = call_function("greet_user", {"name": "John"})
    assert result == "Hello, John!"


def test_simple_function_invalid():
    """Test simple function with invalid input."""
    result = call_function("greet_user", {"name": 123})  # Wrong type
    assert isinstance(result, tuple)
    assert "Validation failed" in result[0]


def test_complex_function_valid():
    """Test complex function with valid input."""
    payload = {
        "user_id": 123,
        "address": {"street": "123 Main St", "city": "Springfield", "zip_code": 12345},
        "tags": ["premium", "active"],
    }
    result = call_function("complex_function", payload)
    assert result["id"] == 123
    assert result["address"]["city"] == "Springfield"
    assert "premium" in result["tags"]


def test_complex_function_invalid():
    """Test complex function with invalid input."""
    payload = {
        "user_id": "not_an_int",  # Wrong type
        "address": {
            "street": "123 Main St",
            "city": "Springfield",
            "zip_code": "12345",  # Wrong type
        },
        "tags": "not_a_list",  # Wrong type
    }
    result = call_function("complex_function", payload)
    assert isinstance(result, tuple)
    assert "Validation failed" in result[0]


def test_json_string_payload():
    """Test handling of JSON string payloads."""
    json_payload = '{"name": "John"}'
    result = call_function("greet_user", json_payload)
    assert result == "Hello, John!"


def test_invalid_json_string():
    """Test handling of invalid JSON string."""
    invalid_json = "{name: John}"  # Invalid JSON
    result = call_function("greet_user", invalid_json)
    assert isinstance(result, tuple)
    assert "Invalid JSON" in result[0]


def test_openai_tools_format():
    """Test OpenAI tools format."""
    tools = get_openai_tools()
    assert isinstance(tools, list)
    for tool in tools:
        assert tool["type"] == "function"
        assert "function" in tool
        assert "name" in tool["function"]
        assert "description" in tool["function"]
        assert "parameters" in tool["function"]


def test_extra_fields():
    """Test handling of extra fields in payload."""
    with pytest.raises(ValueError) as exc:
        call_function("greet_user", {"name": "John", "extra": "field"})
    assert "Unexpected fields" in str(exc.value)
    assert "extra" in str(exc.value)


def test_missing_required_field():
    """Test handling of missing required fields."""
    result = call_function("greet_user", {})
    assert isinstance(result, tuple)
    assert "Validation failed" in result[0]


def test_nonexistent_function():
    """Test calling non-existent function."""
    with pytest.raises(ValueError) as exc:
        call_function("nonexistent", {})
    assert "not registered" in str(exc.value)
