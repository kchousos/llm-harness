import pytest
import os
from unittest import mock
from llm_harness.io.file_manager import FileManager


class TestFileManager:
    """Tests for the FileManager class."""

    def test_init(self):
        """Test initializing FileManager."""
        manager = FileManager("/path/to/project")
        assert manager.project_path == "/path/to/project"
        assert manager.harness_dir == os.path.join(
            "/path/to/project", "harnesses"
        )

    @mock.patch("os.makedirs")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_write_harness_default_filename(self, mock_file, mock_makedirs):
        """Test write_harness with default filename."""
        # Setup mock for _create_unique_filename
        with mock.patch.object(
            FileManager,
            "_create_unique_filename",
            return_value="/path/to/project/harnesses/fuzz.c",
        ):
            manager = FileManager("/path/to/project")
            result = manager.write_harness("harness content")

            # Assertions
            assert result == "/path/to/project/harnesses/fuzz.c"
            mock_makedirs.assert_called_once_with(
                os.path.join("/path/to/project", "harnesses"), exist_ok=True
            )
            mock_file.assert_called_once_with(
                "/path/to/project/harnesses/fuzz.c", "w", encoding="utf-8"
            )
            mock_file().write.assert_called_once_with("harness content")

    @mock.patch("os.makedirs")
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_write_harness_custom_filename(self, mock_file, mock_makedirs):
        """Test write_harness with custom filename."""
        # Setup mock for _create_unique_filename
        with mock.patch.object(
            FileManager,
            "_create_unique_filename",
            return_value="/path/to/project/harnesses/custom.c",
        ):
            manager = FileManager("/path/to/project")
            result = manager.write_harness("harness content", "custom.c")

            # Assertions
            assert result == "/path/to/project/harnesses/custom.c"
            mock_makedirs.assert_called_once_with(
                os.path.join("/path/to/project", "harnesses"), exist_ok=True
            )
            mock_file.assert_called_once_with(
                "/path/to/project/harnesses/custom.c", "w", encoding="utf-8"
            )
            mock_file().write.assert_called_once_with("harness content")

    @mock.patch("os.makedirs")
    @mock.patch("builtins.open")
    def test_write_harness_io_error(self, mock_open, mock_makedirs):
        """Test write_harness when an IOError occurs."""
        # Setup mock for _create_unique_filename and open
        with mock.patch.object(
            FileManager,
            "_create_unique_filename",
            return_value="/path/to/project/harnesses/fuzz.c",
        ):
            mock_open.side_effect = IOError("Test IO Error")

            manager = FileManager("/path/to/project")

            # Call should raise the IOError
            with pytest.raises(IOError, match="Test IO Error"):
                manager.write_harness("harness content")

    def test_create_unique_filename_no_conflict(self):
        """Test _create_unique_filename with no filename conflict."""
        with mock.patch("os.path.exists", return_value=False):
            manager = FileManager("/path/to/project")
            result = manager._create_unique_filename(
                "/path/to/project/harnesses/fuzz.c"
            )

            # Should return the original path
            assert result == "/path/to/project/harnesses/fuzz.c"

    def test_create_unique_filename_with_conflicts(self):
        """Test _create_unique_filename with filename conflicts."""
        # First two calls to exists return True, third returns False
        with mock.patch("os.path.exists", side_effect=[True, True, False]):
            manager = FileManager("/path/to/project")
            result = manager._create_unique_filename(
                "/path/to/project/harnesses/fuzz.c"
            )

            # Should return a path with _2 appended
            assert result == "/path/to/project/harnesses/fuzz_2.c"
