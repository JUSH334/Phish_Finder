import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk, Text, Button, Label
from phishing_detector import classify_email, phishing_detector, root, email_entry, result_label

class TestPhishingDetector(unittest.TestCase):

    @patch("phishing_detector.pipeline")
    def test_pipeline_loading(self, mock_pipeline):
        """Test if the phishing detection pipeline is loaded correctly."""
        mock_pipeline.return_value = MagicMock()
        phishing_detector = pipeline("text-classification", model=MagicMock(), tokenizer=MagicMock(), device=-1)
        self.assertIsNotNone(phishing_detector)

    @patch("phishing_detector.phishing_detector")
    def test_classify_email_phishing(self, mock_detector):
        """Test the classify_email function for a phishing email."""
        # Mock the model output
        mock_detector.return_value = [{"label": "LABEL_1", "score": 0.95}]

        # Simulate input and button press
        email_entry.insert("1.0", "This is a phishing email!")
        classify_email()

        # Check the result label
        expected_text = "Classification: Phishing (Confidence: 95.0%)"
        self.assertEqual(result_label.cget("text"), expected_text)

    @patch("phishing_detector.phishing_detector")
    def test_classify_email_legitimate(self, mock_detector):
        """Test the classify_email function for a legitimate email."""
        # Mock the model output
        mock_detector.return_value = [{"label": "LABEL_0", "score": 0.87}]

        # Simulate input and button press
        email_entry.delete("1.0", "end")
        email_entry.insert("1.0", "This is a legitimate email.")
        classify_email()

        # Check the result label
        expected_text = "Classification: Legitimate (Confidence: 87.0%)"
        self.assertEqual(result_label.cget("text"), expected_text)

    def test_empty_input(self):
        """Test the classify_email function for empty input."""
        with patch("tkinter.messagebox.showwarning") as mock_warning:
            # Simulate empty input and button press
            email_entry.delete("1.0", "end")
            classify_email()

            # Check if warning was called
            mock_warning.assert_called_once_with("Input Error", "Please enter email text to classify.")

    def test_gui_components(self):
        """Test if GUI components are created correctly."""
        self.assertIsInstance(root, Tk)
        self.assertIsInstance(email_entry, Text)
        self.assertIsInstance(result_label, Label)

if __name__ == "__main__":
    unittest.main()

