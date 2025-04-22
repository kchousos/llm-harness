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
Main function utilizing the llm_harness package.
"""

from loguru import logger
from llm_harness.cli import parse_arguments
from llm_harness.core.analyzer import ProjectAnalyzer
from llm_harness.core.generator import HarnessGenerator
from llm_harness.core.builder import HarnessBuilder
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

    logger.info("Building harness...")
    builder = HarnessBuilder(project_path)
    builder.build_harness()

    logger.info("All done!")


if __name__ == "__main__":
    main()
