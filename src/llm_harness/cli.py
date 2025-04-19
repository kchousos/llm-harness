"""
Command-line interface for llm_harness.
"""

import os
import argparse
from dataclasses import dataclass
from loguru import logger
from typing import List
from llm_harness.config import Config


@dataclass
class Arguments:
    """Command line arguments."""

    project_path: str
    model: str
    file_patterns: List[str]


def parse_arguments() -> Arguments:
    """
    Parses the command-line arguments.

    Returns:
        Arguments: The parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Generate fuzzing harnesses for C/C++ projects"
    )

    parser.add_argument(
        "project",
        help="Name of the project under the `assets/` directory, for which "
        "harnesses are to be generated.",
    )

    parser.add_argument(
        "-m",
        "--model",
        default=Config.DEFAULT_MODEL,
        type=str,
        help=f"LLM model to be used. Available: {', '.join(Config.AVAILABLE_MODELS)}",
    )

    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        default=Config.DEFAULT_FILES,
        help="File patterns to include in analysis (e.g. *.c *.h)",
    )

    args = parser.parse_args()

    # Build the project path
    project_path = os.path.join(".", "assets", args.project)
    if not os.path.exists(project_path):
        logger.error(f"Project path does not exist: {project_path}")
        raise FileNotFoundError(f"Project path does not exist: {project_path}")

    # Validate model
    model = args.model
    if model not in Config.AVAILABLE_MODELS:
        logger.warning(
            f"Model {model} not available. Available models: "
            f"{Config.AVAILABLE_MODELS}. "
            f"Will use the default model ({Config.DEFAULT_MODEL})"
        )
        model = Config.DEFAULT_MODEL

    return Arguments(
        project_path=project_path, model=model, file_patterns=args.files
    )
