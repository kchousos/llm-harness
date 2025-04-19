"""
Project analysis functionality.
"""

import os
import glob
from typing import List, Optional
from loguru import logger
from llm_harness.models.project import ProjectFile, ProjectInfo
from llm_harness.config import Config


class ProjectAnalyzer:
    """
    Analyzes project files and extracts relevant information.
    """

    def __init__(
        self, project_path: str, file_patterns: Optional[List[str]] = None
    ):
        """
        Initialize the project analyzer.

        Args:
            project_path (str): Path to the project directory.
            file_patterns (List[str], optional): File patterns to include.
        """
        self.project_path = project_path
        self.file_patterns = file_patterns or Config.DEFAULT_FILES

    def collect_project_info(self) -> ProjectInfo:
        """
        Collects information about the project by reading files.

        Returns:
            ProjectInfo: Information about the project.
        """
        project_files = self._find_project_files()
        files = []

        for file_path in project_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    files.append(
                        ProjectFile(
                            path=file_path,
                            name=os.path.basename(file_path),
                            content=f.read(),
                        )
                    )
            except IOError as e:
                logger.error(f"Error reading file {file_path}: {e}")

        if not files:
            logger.warning("No project files found!")

        return ProjectInfo(files=files)

    def _find_project_files(self) -> List[str]:
        """
        Finds all project files matching the specified patterns.

        Returns:
            List[str]: List of file paths.
        """
        all_files = []
        for pattern in self.file_patterns:
            matched_files = glob.glob(os.path.join(self.project_path, pattern))
            all_files.extend(matched_files)

        return all_files
