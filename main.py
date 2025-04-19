"""
Main function utilizing the llm_harness package
"""

from loguru import logger
import llm_harness as lh


def main() -> None:
    """
    Gets a project's info and main source code, calls an LLM with those which
    creates a harness for the project. The harness is written in the project's
    directory.
    """

    project_path, model = lh.utils.parse_arguments()

    logger.info("Reading project and collecting information...")
    project_info = lh.utils.get_project_info(project_path)

    logger.info("Calling LLM to generate a harness...")
    harness = lh.harness_utils.create_harness(
        model=model, project_info=project_info
    )

    logger.info("Writing harness to project...")
    lh.harness_utils.write_harness(harness=harness, project_path=project_path)

    logger.info("All done!")


if __name__ == "__main__":
    main()
