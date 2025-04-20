"""
Main function utilizing the llm_harness package.
"""

from loguru import logger
from llm_harness.cli import parse_arguments
from llm_harness.core.analyzer import ProjectAnalyzer
from llm_harness.core.generator import HarnessGenerator
from llm_harness.io.file_manager import FileManager


def main() -> None:
    """
    Main entry point of the application. Collects project info, calls
    LLM to create and write a harness for the project.
    """
    args = parse_arguments()
    project_path, model = args.project_path, args.model

    logger.info("Reading project and collecting information...")
    analyzer = ProjectAnalyzer(project_path)
    project_info = analyzer.collect_project_info()

    logger.info("Calling LLM to generate a harness...")
    generator = HarnessGenerator(model=model)
    harness = generator.create_harness(project_info=project_info)

    logger.info("Writing harness to project...")
    file_manager = FileManager(project_path)
    file_manager.write_harness(harness)

    logger.info("All done!")


if __name__ == "__main__":
    main()
