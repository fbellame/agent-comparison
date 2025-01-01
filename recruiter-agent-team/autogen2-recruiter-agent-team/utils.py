import os
import json

def load_prompt(file_path: str) -> str:
    """Loads a text prompt from a file."""
    with open(file_path, 'r') as file:
        return file.read()

def load_vars(file_path: str) -> dict:
    """Loads variables from a JSON file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def format_prompt(prompt: str, variables: dict) -> str:
    """Formats a prompt by replacing placeholders with variable values."""
    return prompt.format(**variables)