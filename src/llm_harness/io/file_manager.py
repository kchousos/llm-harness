"""
File operations for the llm_harness package.
"""

import os
from loguru import logger
from typing import Optional
from llm_harness.config import Config


class FileManager:
    """
    Handles file operations for the harness generator.
    """

    def __init__(self, project_path: str):
        """
        Initialize the file manager.

        Args:
            project_path (str): Path to the project directory.
        """
        self.project_path = project_path
        self.harness_dir = os.path.join(project_path, Config.HARNESS_DIR)

    def write_harness(
        self, harness: str, filename: Optional[str] = None
    ) -> str:
        """
        Writes the harness to the harnesses directory.

        Args:
            harness (str): The harness code to write.
            filename (str, optional): The filename to use.

        Returns:
            str: Path to the written harness file.
        """
        os.makedirs(self.harness_dir, exist_ok=True)

        if not filename:
            filename = Config.DEFAULT_HARNESS_FILENAME

        harness_path = os.path.join(self.harness_dir, filename)
        unique_path = self._create_unique_filename(harness_path)

        try:
            with open(unique_path, "w", encoding="utf-8") as f:
                f.write(harness)
            logger.info(f"Harness written to {unique_path}")
            return unique_path
        except IOError as e:
            logger.error(f"Error writing harness to {unique_path}: {e}")
            raise

    def _create_unique_filename(self, base_path: str) -> str:
        """
        Creates a unique filename by appending an incrementing suffix.

        Args:
            base_path (str): The intended filename.

        Returns:
            str: A unique filename.
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
