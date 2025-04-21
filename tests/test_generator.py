import pytest
from unittest import mock
from llm_harness.core.generator import HarnessGenerator
from llm_harness.models.project import ProjectFiles, ProjectFile


class TestHarnessGenerator:
    """Tests for the HarnessGenerator class."""

    @mock.patch("llm_harness.config.Config.load_env")
    def test_init(self, mock_load_env):
        """Test initializing HarnessGenerator."""
        mock_load_env.return_value = "test-api-key"
        generator = HarnessGenerator("gpt-4o")
        assert generator.model == "gpt-4o"
        mock_load_env.assert_called_once()

    @mock.patch("llm_harness.config.Config.load_env")
    @mock.patch("dspy.LM")
    @mock.patch("dspy.configure")
    def test_create_harness(self, mock_configure, mock_lm, mock_load_env):
        """Test create_harness method."""
        # Setup mocks
        mock_load_env.return_value = "test-api-key"
        mock_lm_instance = mock.MagicMock()
        mock_lm_instance.return_value = ["Generated harness code"]
        mock_lm.return_value = mock_lm_instance

        # Create test project info
        project_file = ProjectFile(
            path="/path/to/file.c",
            name="file.c",
            content="int main() { return 0; }",
        )
        project_info = ProjectFiles(files=[project_file])

        # Create generator and call method
        generator = HarnessGenerator("gpt-4o")
        result = generator.create_harness(project_info)

        # Assertions
        assert result == "Generated harness code"
        mock_lm.assert_called_once_with("openai/gpt-4o", cache=False)
        mock_configure.assert_called_once()
        mock_lm_instance.assert_called_once()

    @mock.patch("llm_harness.config.Config.load_env")
    @mock.patch("dspy.LM")
    def test_create_harness_exception(self, mock_lm, mock_load_env):
        """Test create_harness method when an exception occurs."""
        # Setup mocks
        mock_load_env.return_value = "test-api-key"
        mock_lm.side_effect = Exception("Test exception")

        # Create test project info
        project_file = ProjectFile(
            path="/path/to/file.c",
            name="file.c",
            content="int main() { return 0; }",
        )
        project_info = ProjectFiles(files=[project_file])

        # Create generator and call method - should raise exception
        generator = HarnessGenerator("gpt-4o")
        with pytest.raises(Exception, match="Test exception"):
            generator.create_harness(project_info)
