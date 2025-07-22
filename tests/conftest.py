"""
Test configuration and shared fixtures for Product Connections Manager Platform tests.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)

@pytest.fixture
def mock_requests():
    """Mock the requests library for API testing."""
    with patch('requests.Session') as mock_session:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'success': True}
        mock_response.text = '<html>Mock response</html>'
        mock_session.return_value.get.return_value = mock_response
        mock_session.return_value.post.return_value = mock_response
        yield mock_session

@pytest.fixture
def sample_edr_data():
    """Sample EDR data for testing."""
    return {
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

@pytest.fixture
def mock_authentication():
    """Mock successful authentication."""
    with patch('product_connections_manager.edr_printer.edr_report_generator.EDRReportGenerator.authenticate') as mock_auth:
        mock_auth.return_value = True
        yield mock_auth
