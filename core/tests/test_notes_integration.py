#!/usr/bin/env python3
"""
Integration test for notes converter
Tests end-to-end conversion of sample data files
"""

import unittest
import sys
import subprocess
from pathlib import Path
import tempfile
import shutil

class TestNotesConverterIntegration(unittest.TestCase):
    """Test full conversion workflow with sample data"""

    def setUp(self):
        """Set up test directories and sample data"""
        self.test_data = Path(__file__).parent.parent / 'testData' / 'notes'
        self.converter_script = Path(__file__).parent.parent / 'aiScripts' / 'notesToMd' / 'notes_to_md_converter.py'

        # Create temporary workspace
        self.temp_dir = Path(tempfile.mkdtemp())
        self.raw_dir = self.temp_dir / 'notes' / 'raw'
        self.ai_dir = self.temp_dir / 'notes' / 'ai'
        self.processed_dir = self.temp_dir / 'notes' / 'processed'

        # Create directories
        self.raw_dir.mkdir(parents=True)
        self.ai_dir.mkdir(parents=True)
        self.processed_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary directories"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_convert_plain_text_file(self):
        """Test conversion of plain text note"""
        # Copy sample text file to raw directory
        sample = self.test_data / 'meeting-notes-2025-12-01.txt'
        if not sample.exists():
            self.skipTest("Sample text file not found")

        test_file = self.raw_dir / 'test_note.txt'
        shutil.copy(sample, test_file)

        # Run converter
        result = subprocess.run(
            [sys.executable, str(self.converter_script)],
            cwd=self.temp_dir,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Converter failed: {result.stderr}")

        # Check output
        output_file = self.ai_dir / 'test_note.md'
        self.assertTrue(output_file.exists(), "Output markdown file not created")

        # Check processed directory
        processed_file = self.processed_dir / 'test_note.txt'
        self.assertTrue(processed_file.exists(), "Source file not moved to processed")
        self.assertFalse(test_file.exists(), "Source file not removed from raw")

    def test_convert_markdown_file(self):
        """Test conversion of markdown note"""
        sample = self.test_data / 'technical-architecture.md'
        if not sample.exists():
            self.skipTest("Sample markdown file not found")

        test_file = self.raw_dir / 'test_note.md'
        shutil.copy(sample, test_file)

        # Run converter
        result = subprocess.run(
            [sys.executable, str(self.converter_script)],
            cwd=self.temp_dir,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Converter failed: {result.stderr}")

        # Check output
        output_file = self.ai_dir / 'test_note.md'
        self.assertTrue(output_file.exists(), "Output markdown file not created")

    def test_convert_html_file(self):
        """Test conversion of Apple Notes HTML"""
        sample = self.test_data / 'sample_apple_notes.html'
        if not sample.exists():
            self.skipTest("Sample HTML file not found")

        # Check if html2text is available
        try:
            import html2text
        except ImportError:
            self.skipTest("html2text not installed")

        test_file = self.raw_dir / 'test_note.html'
        shutil.copy(sample, test_file)

        # Run converter
        result = subprocess.run(
            [sys.executable, str(self.converter_script)],
            cwd=self.temp_dir,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Converter failed: {result.stderr}")

        # Check output
        output_file = self.ai_dir / 'test_note.md'
        self.assertTrue(output_file.exists(), "Output markdown file not created")

        # Verify markdown content has headings
        content = output_file.read_text(encoding='utf-8')
        self.assertIn('# ', content, "Should have H1 headings")

    def test_convert_multiple_files(self):
        """Test conversion of multiple files at once"""
        # Copy multiple sample files
        samples = [
            ('meeting-notes-2025-12-01.txt', 'note1.txt'),
            ('status-update-2025-12-08.txt', 'note2.txt'),
        ]

        copied_count = 0
        for source_name, dest_name in samples:
            source = self.test_data / source_name
            if source.exists():
                dest = self.raw_dir / dest_name
                shutil.copy(source, dest)
                copied_count += 1

        if copied_count == 0:
            self.skipTest("No sample files found")

        # Run converter
        result = subprocess.run(
            [sys.executable, str(self.converter_script)],
            cwd=self.temp_dir,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Converter failed: {result.stderr}")

        # Check that multiple files were converted
        ai_files = list(self.ai_dir.glob('*.md'))
        self.assertGreaterEqual(len(ai_files), copied_count, "Not all files converted")

    def test_empty_raw_directory(self):
        """Test converter handles empty raw directory gracefully"""
        # Run converter with no files
        result = subprocess.run(
            [sys.executable, str(self.converter_script)],
            cwd=self.temp_dir,
            capture_output=True,
            text=True
        )

        # Should succeed with no errors
        self.assertEqual(result.returncode, 0, f"Converter failed on empty dir: {result.stderr}")

    def test_converter_creates_directories(self):
        """Test converter creates required directories if missing"""
        # Remove directories
        shutil.rmtree(self.temp_dir / 'notes')

        # Copy a test file to temporary location
        sample = self.test_data / 'meeting-notes-2025-12-01.txt'
        if not sample.exists():
            self.skipTest("Sample text file not found")

        # Create only raw directory with file
        self.raw_dir.mkdir(parents=True)
        test_file = self.raw_dir / 'test.txt'
        shutil.copy(sample, test_file)

        # Run converter - should create missing directories
        result = subprocess.run(
            [sys.executable, str(self.converter_script)],
            cwd=self.temp_dir,
            capture_output=True,
            text=True
        )

        self.assertEqual(result.returncode, 0, f"Converter failed: {result.stderr}")

        # Verify directories were created
        self.assertTrue(self.ai_dir.exists(), "ai/ directory not created")
        self.assertTrue(self.processed_dir.exists(), "processed/ directory not created")


def run_tests():
    """Run all integration tests and return exit code"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestNotesConverterIntegration)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
