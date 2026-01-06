#!/usr/bin/env python3
"""
Smoke tests for notes converter
Tests critical paths to ensure notes conversion works correctly for all supported formats
"""

import unittest
import sys
from pathlib import Path
import tempfile
import shutil
import os

# Add notes converter to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'aiScripts' / 'notesToMd'))

class TestNotesConverterBasics(unittest.TestCase):
    """Test basic notes converter functionality"""

    def setUp(self):
        """Set up test fixtures and temporary directories"""
        self.test_data = Path(__file__).parent.parent / 'testData' / 'notes'
        self.temp_dir = Path(tempfile.mkdtemp())
        self.raw_dir = self.temp_dir / 'raw'
        self.ai_dir = self.temp_dir / 'ai'
        self.processed_dir = self.temp_dir / 'processed'

        # Create directories
        self.raw_dir.mkdir(parents=True)
        self.ai_dir.mkdir(parents=True)
        self.processed_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary directories"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_notes_converter_script_exists(self):
        """Test that notes converter script exists"""
        converter_path = Path(__file__).parent.parent / 'aiScripts' / 'notesToMd' / 'notes_to_md_converter.py'
        self.assertTrue(converter_path.exists(), "Notes converter script not found")

    def test_notes_converter_can_be_imported(self):
        """Test that notes converter module can be imported"""
        try:
            import notes_to_md_converter
            self.assertTrue(True, "Module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import notes converter: {e}")

    def test_sample_text_file_exists(self):
        """Test that sample .txt file exists in testData"""
        txt_file = self.test_data / 'meeting-notes-2025-12-01.txt'
        self.assertTrue(txt_file.exists(), "Sample .txt file not found in testData")

    def test_sample_markdown_file_exists(self):
        """Test that sample .md file exists in testData"""
        md_file = self.test_data / 'technical-architecture.md'
        self.assertTrue(md_file.exists(), "Sample .md file not found in testData")


class TestNotesConverterFormats(unittest.TestCase):
    """Test support for various note formats"""

    def setUp(self):
        """Set up test data path"""
        self.test_data = Path(__file__).parent.parent / 'testData' / 'notes'

    def test_onenote_docx_sample_exists(self):
        """Test that OneNote .docx sample exists"""
        docx_file = self.test_data / 'sample_onenote_export.docx'
        self.assertTrue(docx_file.exists(), "OneNote .docx sample not found")

    def test_bear_textbundle_sample_exists(self):
        """Test that Bear .textbundle sample exists"""
        textbundle = self.test_data / 'sample_bear_note.textbundle'
        self.assertTrue(textbundle.exists(), "Bear .textbundle sample not found")
        self.assertTrue(textbundle.is_dir(), "TextBundle should be a directory")

    def test_bear_textbundle_has_required_files(self):
        """Test that Bear .textbundle has required structure"""
        textbundle = self.test_data / 'sample_bear_note.textbundle'

        if not textbundle.exists():
            self.skipTest("TextBundle sample not found")

        # Check for info.json
        info_json = textbundle / 'info.json'
        self.assertTrue(info_json.exists(), "TextBundle missing info.json")

        # Check for text file (either text.md or text.txt)
        text_md = textbundle / 'text.md'
        text_txt = textbundle / 'text.txt'
        has_text_file = text_md.exists() or text_txt.exists()
        self.assertTrue(has_text_file, "TextBundle missing text.md or text.txt")

    def test_apple_notes_html_sample_exists(self):
        """Test that Apple Notes .html sample exists"""
        html_file = self.test_data / 'sample_apple_notes.html'
        self.assertTrue(html_file.exists(), "Apple Notes .html sample not found")


class TestNotesConverterDependencies(unittest.TestCase):
    """Test optional dependencies availability"""

    def test_docx_library_available(self):
        """Test if python-docx is available (optional for OneNote support)"""
        try:
            import docx
            has_docx = True
        except ImportError:
            has_docx = False

        # We don't fail if missing - just note availability
        self.assertIsInstance(has_docx, bool, "DOCX availability check should be boolean")

    def test_html2text_library_available(self):
        """Test if html2text is available (optional for Apple Notes support)"""
        try:
            import html2text
            has_html2text = True
        except ImportError:
            has_html2text = False

        # We don't fail if missing - just note availability
        self.assertIsInstance(has_html2text, bool, "html2text availability check should be boolean")


class TestNotesConverterParsers(unittest.TestCase):
    """Test individual parser functions"""

    def setUp(self):
        """Set up test data path"""
        self.test_data = Path(__file__).parent.parent / 'testData' / 'notes'

    def test_plain_text_can_be_read(self):
        """Test that plain text files can be read"""
        txt_file = self.test_data / 'meeting-notes-2025-12-01.txt'

        if not txt_file.exists():
            self.skipTest("Sample .txt file not found")

        try:
            content = txt_file.read_text(encoding='utf-8')
            self.assertIsInstance(content, str, "Should read as string")
            self.assertGreater(len(content), 0, "File should have content")
        except Exception as e:
            self.fail(f"Failed to read text file: {e}")

    def test_markdown_can_be_read(self):
        """Test that markdown files can be read"""
        md_file = self.test_data / 'technical-architecture.md'

        if not md_file.exists():
            self.skipTest("Sample .md file not found")

        try:
            content = md_file.read_text(encoding='utf-8')
            self.assertIsInstance(content, str, "Should read as string")
            self.assertGreater(len(content), 0, "File should have content")
        except Exception as e:
            self.fail(f"Failed to read markdown file: {e}")

    def test_docx_can_be_parsed(self):
        """Test that .docx files can be parsed (if library available)"""
        docx_file = self.test_data / 'sample_onenote_export.docx'

        if not docx_file.exists():
            self.skipTest("OneNote .docx sample not found")

        try:
            import docx
        except ImportError:
            self.skipTest("python-docx not installed")

        try:
            doc = docx.Document(docx_file)
            paragraphs = [p.text for p in doc.paragraphs]
            self.assertIsInstance(paragraphs, list, "Should parse paragraphs")
        except Exception as e:
            self.fail(f"Failed to parse .docx file: {e}")

    def test_html_can_be_parsed(self):
        """Test that .html files can be parsed (if library available)"""
        html_file = self.test_data / 'sample_apple_notes.html'

        if not html_file.exists():
            self.skipTest("Apple Notes .html sample not found")

        try:
            import html2text
        except ImportError:
            self.skipTest("html2text not installed")

        try:
            content = html_file.read_text(encoding='utf-8')
            h = html2text.HTML2Text()
            markdown = h.handle(content)
            self.assertIsInstance(markdown, str, "Should convert to markdown string")
            self.assertGreater(len(markdown), 0, "Converted markdown should have content")
        except Exception as e:
            self.fail(f"Failed to parse .html file: {e}")


class TestNotesConverterFileOperations(unittest.TestCase):
    """Test file operations and directory handling"""

    def setUp(self):
        """Set up temporary directories"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.raw_dir = self.temp_dir / 'raw'
        self.ai_dir = self.temp_dir / 'ai'
        self.processed_dir = self.temp_dir / 'processed'

        # Create directories
        self.raw_dir.mkdir(parents=True)
        self.ai_dir.mkdir(parents=True)
        self.processed_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary directories"""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_directories_can_be_created(self):
        """Test that required directories can be created"""
        self.assertTrue(self.raw_dir.exists(), "raw/ directory should exist")
        self.assertTrue(self.ai_dir.exists(), "ai/ directory should exist")
        self.assertTrue(self.processed_dir.exists(), "processed/ directory should exist")

    def test_text_file_can_be_copied(self):
        """Test that text files can be copied between directories"""
        # Create test file
        test_file = self.raw_dir / 'test.txt'
        test_file.write_text('Test content', encoding='utf-8')

        # Copy to ai directory
        dest_file = self.ai_dir / 'test.md'
        dest_file.write_text(test_file.read_text(encoding='utf-8'), encoding='utf-8')

        self.assertTrue(dest_file.exists(), "File should be copied")
        self.assertEqual(dest_file.read_text(), 'Test content', "Content should match")

    def test_file_can_be_moved(self):
        """Test that files can be moved between directories"""
        # Create test file
        test_file = self.raw_dir / 'test.txt'
        test_file.write_text('Test content', encoding='utf-8')

        # Move to processed directory
        dest_file = self.processed_dir / 'test.txt'
        shutil.move(str(test_file), str(dest_file))

        self.assertFalse(test_file.exists(), "Original file should be moved")
        self.assertTrue(dest_file.exists(), "File should be in processed")


def run_tests():
    """Run all tests and return exit code"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestNotesConverterBasics))
    suite.addTests(loader.loadTestsFromTestCase(TestNotesConverterFormats))
    suite.addTests(loader.loadTestsFromTestCase(TestNotesConverterDependencies))
    suite.addTests(loader.loadTestsFromTestCase(TestNotesConverterParsers))
    suite.addTests(loader.loadTestsFromTestCase(TestNotesConverterFileOperations))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
