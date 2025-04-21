"""
Data models for project analysis.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class ProjectFile:
    """Represents a source file in the project."""

    path: str
    name: str
    content: str


@dataclass
class ProjectFiles:
    """Contains information about a project."""

    files: List[ProjectFile]

    def get_concatenated_content(self) -> str:
        """
        Returns the concatenated content of all project files.

        Returns:
            str: Contents of all project files.
        """
        file_contents = []

        for file in self.files:
            file_contents.append(f"\n>>>> {file.name}\n")
            file_contents.append(file.content)

        return "".join(file_contents)
