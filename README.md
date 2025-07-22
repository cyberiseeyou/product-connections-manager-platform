# Product Connections Manager - Enhanced EDR Printer

A comprehensive platform for managing Product Connections operations, including automated EDR printing, event management, and retail link integrations.

## Features

- **Enhanced PDF Generation**: Professional-grade PDF reports with custom formatting
- **PDF Consolidation**: Merge multiple reports into single documents  
- **Signature Fields**: Automated signature blocks with date/time stamps
- **Event Code Translation**: Human-readable event descriptions
- **Batch Processing**: Automated processing of multiple events
- **Console Scripts**: Command-line tools for easy usage

## Installation

```bash
pip install product-connections-manager
```

For PDF features:
```bash
pip install "product-connections-manager[pdf]"
```

## Quick Start

```python
from product_connections_manager import EnhancedEDRPrinter

# Initialize the printer
printer = EnhancedEDRPrinter()

# Process events with PDF consolidation
printer.process_multiple_events(['12345', '67890'])
```

## Command Line Usage

```bash
# Enhanced printing
edr-printer --events 12345,67890 --output consolidated_report.pdf

# Automated batch processing
edr-automated --batch-size 10
```

## License

MIT License