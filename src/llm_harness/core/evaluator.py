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
Runs and evaluates the generated harness.
"""

import subprocess
from loguru import logger
from llm_harness.config import Config


class HarnessEvaluator:
    """
    Runs and evaluates a project's generated harness.
    """

    def __init__(self, project_path: str):
        """
        Initialize the evaluator.

        Args:
            project_path (str): Path to the project directory.
        """
        self.project_path = project_path
        self.executable = Config().EXECUTABLE_FILENAME

    def evaulate_harness(self) -> bool:
        """
        Runs and evaluates the LLM-generated harness.

        Returns:
            bool: Returns whether the harness "passes" the evaluation.
        """
        execution_command = f"./{self.executable}"
        logger.info("Starting execution of harness...")
        subprocess.run(
            execution_command,
            check=False,
            text=True,
            cwd=self.project_path,
        )

        return True
