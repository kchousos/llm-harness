"""
Configuration management for the llm_harness package.
"""

import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration for llm_harness."""

    # List of available models
    AVAILABLE_MODELS = [
        "gpt-4.1-mini",
        "o4-mini",
        "o3-mini",
        "gpt-4o",
        "gpt-4o-mini",
    ]

    # Default model if none provided
    DEFAULT_MODEL = "gpt-4.1-mini"

    # Default files to include if none specified
    DEFAULT_FILES = ["*.c", "*.h", "*.cpp", "*.hpp", "Makefile"]

    # Harness directory name
    HARNESS_DIR = "harnesses"

    # Harness default filename
    DEFAULT_HARNESS_FILENAME = "fuzz.c"

    @staticmethod
    def load_env():
        """Load environment variables from .env file."""
        load_dotenv()
        return os.environ.get("OPENAI_API_KEY")
