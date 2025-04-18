"""
Main function utilizing the llm_harness package
"""

from loguru import logger
from llm_harness import parse_arguments, get_project_info, create_harness, write_harness


def main() -> None:
    """
    Gets a project's info and main source code, calls an LLM with those which
    creates a harness for the project. The harness is written in the project's
    directory.
    """

    project_path, model = parse_arguments()

    logger.info("Reading project and collecting information...")
    project_info = get_project_info(project_path)

    logger.info("Calling LLM to generate a harness...")
    harness = create_harness(model=model, project_info=project_info)

    logger.info("Writing harness to project...")
    write_harness(harness=harness, project_path=project_path)

    logger.info("All done!")


if __name__ == "__main__":
    main()
