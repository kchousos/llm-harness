"""
This project uses *LLMs* to automatically generate *fuzzing harnesses* for your
C/C++ project.

---
"""

from dotenv import load_dotenv
import argparse
import sys
import dspy
import os
from pathlib import Path


def unique_filename(base_path: str) -> str:
    """
    Creates a unique filename by appending an index when a file with the same
    name exists.
    """
    path = Path(base_path)
    stem = path.stem
    suffix = path.suffix
    parent = path.parent

    counter = 1
    new_path = path

    while new_path.exists():
        new_name = f"{stem}_{counter}{suffix}"
        new_path = parent / new_name
        counter += 1

    return str(new_path)


def parse_arguments() -> tuple[str, str]:
    """
    Parse the project to be fuzzed and the LLM model to be used.
    """
    parser = argparse.ArgumentParser()

    available_models = ["gpt-4.1-mini", "o4-mini", "o3-mini", "gpt-4o", "gpt-4o-mini"]

    parser.add_argument(
        "project",
        help="Name of the project under the `assets/` directory, for which harnesses are to be generated.",
    )
    parser.add_argument(
        "-m", "--model", default="gpt-4.1-mini", type=str, help="LLM model to be used."
    )

    args = parser.parse_args()

    path = "./assets/" + args.project
    model = args.model

    if model not in available_models:
        print(
            f"Model {model} not available. Available models: {available_models}",
            file=sys.stderr,
        )
        exit(-1)

    return path, model


def get_project_info(project_path: str) -> str:
    """
    Returns the contents of all related project files.
    """

    # hardcoding for now, will fix later
    project_files = [project_path + "/dateparse.c", project_path + "/dateparse.h"]

    file_contents = []

    for path in project_files:
        with open(path, "r", encoding="utf-8") as f:
            file_contents.append(
                "\n"
                + "/" * 30
                + " " * 5
                + os.path.basename(f.name)
                + " " * 5
                + "/" * 30
                + "\n\n"
            )
            file_contents.append(f.read())

    return "".join(file_contents)


def create_harness(model: str, project_info: str) -> str:
    """
    Calls the LLM to create a harness for the project.
    """

    load_dotenv()  # used for OpenAI API key

    lm = dspy.LM(f"openai/{model}")
    dspy.configure(lm=lm)

    response = lm(
        """
        I have this C project, for which you will find the contents below.
        Write me a fuzzing harness for the dateparse function. Respond **only**
        with the harness' code. Make sure to write all the necessary includes
        etc. The harness will be located in a `harnesses/` subdirectory from
        the project root, so make sure the includes work appropriately.
         
        Do not even wrap the code in markdown fences, e.g. ```, because it
        will be automatically written to a .c file.

        === Source Code ===

        """
        + project_info
    )

    return response[0]


def write_harness(harness: str, project_path: str) -> None:
    """
    Writes the harness in the project's `harnesses/` directory.

    If other harnessess with the same filename exist, a new file is created
    with an incremented index.
    """
    directory = project_path + "/harnesses"
    if not os.path.exists(directory):
        os.makedirs(directory)

    harness_path = unique_filename(directory + "/fuzz.c")

    with open(harness_path, "w", encoding="utf-8") as f:
        f.write(harness)


def main() -> None:
    """
    Gets a project's info and main source code, calls an LLM with those which
    creates a harness for the project. The harness is written in the project's
    directory.
    """

    project_path, model = parse_arguments()

    project_info = get_project_info(project_path)

    harness = create_harness(model=model, project_info=project_info)
    write_harness(harness=harness, project_path=project_path)


if __name__ == "__main__":
    main()
