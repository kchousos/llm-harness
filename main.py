"""
Main function utilizing the llm_harness package.
"""

from loguru import logger
import llm_harness.utils as utils
import llm_harness.harness_utils as lh


def main() -> None:
    """
    Main entry point of the application. Collects project info, calls
    LLM to create and write a harness for the project.
    """

    project_path, model = utils.parse_arguments()

    logger.info("Reading project and collecting information...")
    project_info = lh.get_project_info(project_path)

    logger.info("Calling LLM to generate a harness...")
    harness = lh.create_harness(model=model, project_info=project_info)

    logger.info("Writing harness to project...")
    lh.write_harness(harness=harness, project_path=project_path)

    logger.info("All done!")


if __name__ == "__main__":
    main()
