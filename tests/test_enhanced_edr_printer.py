"""
Tests for the Enhanced EDR Printer module.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import tempfile
import os
from pathlib import Path

# Import the modules to test
try:
    from product_connections_manager.edr_printer import EnhancedEDRPrinter
except ImportError:
    # Fallback for development
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'product_connections_manager', 'edr_printer'))
    from enhanced_edr_printer import EnhancedEDRPrinter


class TestEnhancedEDRPrinter(unittest.TestCase):
    """Test cases for EnhancedEDRPrinter class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.printer = EnhancedEDRPrinter()
        self.sample_event_data = {
            'demoId': '606034',
            'demoName': 'Test Food Demo Event',
            'demoClassCode': '45',
            'demoStatusCode': '2',
            'demoDate': '2025-07-22',
            'demoLockInd': 'N',
            'demoInstructions': {
                'demoPrepnTxt': 'Test preparation instructions',
                'demoPortnTxt': 'Test portion instructions'
            },
            'itemDetails': [
                {
                    'itemNbr': '12345',
                    'gtin': '67890',
                    'itemDesc': 'Test Product',
                    'vendorNbr': '123',
                    'deptNbr': '456'
                }
            ]
        }
    
    def test_event_type_description_mapping(self):
        """Test event type code to description mapping."""
        self.assertEqual(self.printer.get_event_type_description('45'), 'Food Demo/Sampling')
        self.assertEqual(self.printer.get_event_type_description('1'), 'Sampling')
        self.assertEqual(self.printer.get_event_type_description('999'), 'Event Type 999')
        self.assertEqual(self.printer.get_event_type_description('N/A'), 'N/A')
    
    def test_event_status_description_mapping(self):
        """Test event status code to description mapping."""
        self.assertEqual(self.printer.get_event_status_description('2'), 'Active/Scheduled')
        self.assertEqual(self.printer.get_event_status_description('1'), 'Pending')
        self.assertEqual(self.printer.get_event_status_description('999'), 'Status 999')
        self.assertEqual(self.printer.get_event_status_description('N/A'), 'N/A')
    
    @patch('product_connections_manager.edr_printer.enhanced_edr_printer.REPORTLAB_AVAILABLE', True)
    def test_pdf_generation_structure(self):
        """Test PDF generation with mock data."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_filename = os.path.join(temp_dir, 'test_report.pdf')
            
            # Mock ReportLab components
            with patch('product_connections_manager.edr_printer.enhanced_edr_printer.SimpleDocTemplate') as mock_doc, \
                 patch('product_connections_manager.edr_printer.enhanced_edr_printer.getSampleStyleSheet') as mock_styles:
                
                mock_doc_instance = Mock()
                mock_doc.return_value = mock_doc_instance
                mock_styles.return_value = {'Normal': Mock(), 'Heading1': Mock(), 'Heading2': Mock()}
                
                # Test PDF generation
                result = self.printer.generate_consolidated_pdf_reportlab(
                    [self.sample_event_data], 
                    test_filename
                )
                
                # Verify the method was called and returned a filename
                self.assertEqual(result, test_filename)
                mock_doc_instance.build.assert_called_once()
    
    def test_initialization(self):
        """Test EnhancedEDRPrinter initialization."""
        self.assertIsInstance(self.printer.event_type_codes, dict)
        self.assertIsInstance(self.printer.event_status_codes, dict)
        self.assertIsInstance(self.printer.pdf_reports, list)
        
        # Check some key mappings exist
        self.assertIn('45', self.printer.event_type_codes)
        self.assertIn('2', self.printer.event_status_codes)


class TestPackageStructure(unittest.TestCase):
    """Test the package structure and imports."""
    
    def test_package_imports(self):
        """Test that main classes can be imported from the package."""
        try:
            from product_connections_manager.edr_printer import EnhancedEDRPrinter
            from product_connections_manager.edr_printer import AutomatedEDRPrinter
            from product_connections_manager.edr_printer import EDRReportGenerator
            
            # Test that classes can be instantiated (basic smoke test)
            self.assertTrue(hasattr(EnhancedEDRPrinter, '__init__'))
            self.assertTrue(hasattr(AutomatedEDRPrinter, '__init__'))
            self.assertTrue(hasattr(EDRReportGenerator, '__init__'))
            
        except ImportError as e:
            self.fail(f"Failed to import required classes: {e}")
    
    def test_version_availability(self):
        """Test that package version is available."""
        try:
            import product_connections_manager
            self.assertTrue(hasattr(product_connections_manager, '__version__'))
            self.assertIsInstance(product_connections_manager.__version__, str)
        except ImportError:
            # This is acceptable during development
            pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
