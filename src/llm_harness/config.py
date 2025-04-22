# Copyright (C) 2025 Konstantinos Chousos
#
# This file is part of LLM-Harness.
#
# LLM-Harness is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LLM-Harness is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LLM-Harness.  If not, see <https://www.gnu.org/licenses/>.

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
        "gpt-4.1",
        "gpt-4.1-mini",
    ]

    # Default model if none provided
    DEFAULT_MODEL = "gpt-4.1-mini"

    # Default files to include if none specified
    DEFAULT_FILES = ["*.c", "*.h", "*.cpp", "*.hpp", "Makefile"]

    # Harness directory name
    # Defaults to project's root directory
    HARNESS_DIR = "."

    # Harness default filename
    DEFAULT_HARNESS_FILENAME = "harness.c"

    @staticmethod
    def load_env():
        """Load environment variables from .env file."""
        load_dotenv()
        return os.environ.get("OPENAI_API_KEY")
