from llm_harness.models.project import ProjectFile, ProjectFiles


class TestProjectModels:
    """Tests for the project models."""

    def test_project_file(self):
        """Test ProjectFile model."""
        file = ProjectFile(
            path="/path/to/file.c",
            name="file.c",
            content="int main() { return 0; }",
        )

        assert file.path == "/path/to/file.c"
        assert file.name == "file.c"
        assert file.content == "int main() { return 0; }"

    def test_project_info_empty(self):
        """Test ProjectInfo model with no files."""
        project_info = ProjectFiles(files=[])

        assert len(project_info.files) == 0
        assert project_info.get_concatenated_content() == ""

    def test_project_info_single_file(self):
        """Test ProjectInfo model with a single file."""
        file = ProjectFile(
            path="/path/to/file.c",
            name="file.c",
            content="int main() { return 0; }",
        )
        project_info = ProjectFiles(files=[file])

        assert len(project_info.files) == 1
        concatenated = project_info.get_concatenated_content()

        # Check that the content contains the expected header and file content
        assert "file.c" in concatenated
        assert "int main() { return 0; }" in concatenated

    def test_project_info_multiple_files(self):
        """Test ProjectInfo model with multiple files."""
        file1 = ProjectFile(
            path="/path/to/file1.c",
            name="file1.c",
            content="int func1() { return 1; }",
        )
        file2 = ProjectFile(
            path="/path/to/file2.h", name="file2.h", content="#define VALUE 42"
        )
        project_info = ProjectFiles(files=[file1, file2])

        assert len(project_info.files) == 2
        concatenated = project_info.get_concatenated_content()

        # Check that the content contains both files with their headers
        assert "file1.c" in concatenated
        assert "int func1() { return 1; }" in concatenated
        assert "file2.h" in concatenated
        assert "#define VALUE 42" in concatenated
