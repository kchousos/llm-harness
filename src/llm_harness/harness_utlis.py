"""
_summary_2

_extended_summary_

Returns:
    _type_: _description_
"""

import os
import dspy
from dotenv import load_dotenv
from llm_harness.utils import unique_filename


def get_project_info(project_path: str) -> str:
    """
    Returns the contents of all related project files.
    """

    # hardcoding for now, will fix later
    project_files = [f"{project_path}/dateparse.c", f"{project_path}/dateparse.h"]

    file_contents = []

    for path in project_files:
        with open(path, "r", encoding="utf-8") as f:
            file_contents.append(
                f"\n{'/' * 30}{' ' * 5}{os.path.basename(f.name)}{' ' * 5}{'/' * 30}\n\n"
            )
            file_contents.append(f.read())

    return "".join(file_contents)


def create_harness(model: str, project_info: str) -> str:
    """
    Calls the LLM to create a harness for the project.
    """

    load_dotenv()  # used for OpenAI API key

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

    If other harnessess with the same filename exist, a new file is created
    with an incremented index.
    """
    directory = f"{project_path}/harnesses"
    if not os.path.exists(directory):
        os.makedirs(directory)

    harness_path = unique_filename(f"{directory}/fuzz.c")

    with open(harness_path, "w", encoding="utf-8") as f:
        f.write(harness)
