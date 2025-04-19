"""
Functions for creating harnesses with LLMs.
"""

import os
import dspy
from dotenv import load_dotenv
from llm_harness.utils import _unique_filename
from loguru import logger


def get_project_info(project_path: str) -> str:
    """
    Returns the contents of all related project files.

    Args:
        project_path (str): Path to the project directory.

    Returns:
        str: Contents of project files.
    """
    project_files = [
        os.path.join(project_path, "dateparse.c"),
        os.path.join(project_path, "dateparse.h"),
    ]

    file_contents = []

    for path in project_files:
        with open(path, "r", encoding="utf-8") as f:
            file_contents.append(
                f"\n{'/' * 30}{' ' * 5}{os.path.basename(f.name)}{' ' * 5}\
                    {'/' * 30}\n\n"
            )
            file_contents.append(f.read())

    return "".join(file_contents)


def create_harness(model: str, project_info: str) -> str:
    """
    Calls the LLM to create a harness for the project.

    Args:
        model (str): The model to be used for LLM.
        project_info (str): The project code.

    Returns:
        str: The generated harness code.
    """
    load_dotenv()  # Load environment variables

    lm = dspy.LM(f"openai/{model}", cache=False)
    dspy.configure(lm=lm)

    response = lm(
        f"""
        I have this C project, for which you will find the contents below.
        Write me a fuzzing harness for the dateparse function. Respond **only**
        with the harness' code. Make sure to write all the necessary includes
        etc. The harness will be located in a `harnesses/` subdirectory from
        the project root, so make sure the includes work appropriately.

        Do not even wrap the code in markdown fences, e.g. ```, because it
        will be automatically written to a .c file.

        === Source Code ===

        {project_info}
        """
    )

    return response[0]


def write_harness(harness: str, project_path: str) -> None:
    """
    Writes the harness in the project's `harnesses/` directory.

    Args:
        harness (str): The harness code to write.
        project_path (str): Path to the project directory.
    """
    directory = os.path.join(project_path, "harnesses")
    os.makedirs(directory, exist_ok=True)
    harness_path = _unique_filename(os.path.join(directory, "fuzz.c"))

    try:
        with open(harness_path, "w", encoding="utf-8") as f:
            f.write(harness)
    except IOError as e:
        logger.error(f"Error writing harness to {harness_path}: {e}")
