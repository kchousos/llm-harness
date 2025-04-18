"""
_summary_

_extended_summary_

Returns:
    _type_: _description_
"""

import os
import argparse
from loguru import logger


def unique_filename(base_path: str) -> str:
    """
    Creates a unique filename by appending an incrementing suffix
    (e.g. file_1.txt)

    Args:
        base_path (str): The intended filename, besides the suffix.

    Returns:
        str: The generated unique filename.
    """
    parent = os.path.dirname(base_path)
    filename = os.path.basename(base_path)
    stem, suffix = os.path.splitext(filename)

    counter = 1
    new_path = base_path

    while os.path.exists(new_path):
        new_filename = f"{stem}_{counter}{suffix}"
        new_path = os.path.join(parent, new_filename)
        counter += 1

    return new_path


def parse_arguments() -> tuple[str, str]:
    """
    Parses the command-line arguments.

    Specifically, it reads the project to be fuzzed and the LLM model to be
    used, if specified.

    Returns:
        tuple[str, str]: A string tuple of the project root directory and
        the model to be used.
    """
    parser = argparse.ArgumentParser()

    available_models = [
        "gpt-4.1-mini",
        "o4-mini",
        "o3-mini",
        "gpt-4o",
        "gpt-4o-mini",
    ]

    parser.add_argument(
        "project",
        help="Name of the project under the `assets/` directory, for which \
              harnesses are to be generated.",
    )
    model_arg = parser.add_argument(
        "-m",
        "--model",
        default="gpt-4.1-mini",
        type=str,
        help="LLM model to be used.",
    )

    args = parser.parse_args()

    path = f"./assets/{args.project}"
    model = args.model

    if model not in available_models:
        logger.warning(
            f" Model {model} not available. Available models:"
            f"{available_models}. "
            f"Will use the default model ({model_arg.default})"
        )
        model = model_arg.default

    return (path, model)
