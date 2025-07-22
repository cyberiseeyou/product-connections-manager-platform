# Tests for Product Connections Manager Platform

This directory contains unit tests and integration tests for the platform.

## Running Tests

```bash
# Install with dev dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run tests with coverage
pytest --cov=product_connections_manager

# Run specific test file
pytest tests/test_edr_printer.py -v
```

## Test Structure

- `test_edr_report_generator.py` - Tests for core EDR functionality
- `test_automated_edr_printer.py` - Tests for automated batch processing
- `test_enhanced_edr_printer.py` - Tests for PDF generation and formatting
- `conftest.py` - Shared test fixtures and configuration
