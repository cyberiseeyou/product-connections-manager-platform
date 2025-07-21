# Enhanced EDR Printer Module 🖨️

## Overview

The Enhanced EDR Printer is a professional Python automation tool designed for Walmart's Product Connections team. It automates the retrieval and processing of Event Detail Reports (EDRs) from Walmart's Retail Link portal, with advanced PDF consolidation and custom formatting features.

## ✨ Key Features

### 🎯 **Enhanced PDF Generation**
- **Consolidated PDF Reports**: Combines multiple EDR reports into a single, professionally formatted PDF
- **Professional Cover Page**: Includes event summary table with event IDs, names, types, and statuses
- **Optimized Layout**: Custom column widths to properly display long event names
- **Individual Report Pages**: Each EDR gets its own dedicated page for clarity

### 📋 **Custom Report Formatting**
- **"MUST BE SIGNED AND DATED" Header**: Clear, bold directive for compliance
- **Custom Signature Fields**:
  - Event Specialist Printed Name
  - Event Specialist Signature
  - Date Performed
  - Supervisor Signature
- **Event Code Translation**: Converts numeric codes to human-readable descriptions
  - Event Type 45 → "Food Demo/Sampling"
  - Event Status 2 → "Active/Scheduled"

### 🔧 **Technical Improvements**
- **Dual PDF Libraries**: Support for both ReportLab and WeasyPrint
- **Enhanced Error Handling**: Comprehensive error reporting and recovery
- **Cross-Platform Printing**: Windows, macOS, and Linux support
- **Automatic File Management**: Opens generated PDFs automatically

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Basic Usage
```python
from enhanced_edr_printer import EnhancedEDRPrinter

# Initialize the printer
printer = EnhancedEDRPrinter()

# Process events and generate consolidated PDF
success = printer.run_enhanced_batch(
    event_ids=['606034', '606035'],  # Your event IDs
    authenticate=True,               # Perform one-time auth
    create_pdf=True,                # Generate PDF
    auto_print=True,                # Attempt printing
    open_pdf=True                   # Open PDF viewer
)
```

### Command Line Usage
```bash
# Use default event ID
python enhanced_edr_printer.py

# Specify custom event IDs
python enhanced_edr_printer.py 606034 606035 606036
```

## 📄 Sample Output

The enhanced EDR printer generates:

### Cover Page
```
CONSOLIDATED EVENT DETAILS REPORT
Generated on 2025-07-21 at 07:55:19
Total Events: 1

┌─────────┬────────────────────────────────┬─────────────────────┬──────────────────┐
│Event ID │Event Name                      │Event Type           │Status            │
├─────────┼────────────────────────────────┼─────────────────────┼──────────────────┤
│606034   │Kellogg's Cereal Demo Event...  │Food Demo/Sampling   │Active/Scheduled  │
└─────────┴────────────────────────────────┴─────────────────────┴──────────────────┘
```

### Individual Report Format
```
EVENT DETAIL REPORT

IMPORTANT!!! This report should be printed each morning prior to completing each event.
[Additional compliance and retention instructions...]

┌──────────────┬─────────────────────┬─────────────────────────────────┐
│Event Number  │Event Type           │Event Locked                     │
├──────────────┼─────────────────────┼─────────────────────────────────┤
│606034        │Food Demo/Sampling   │No                               │
└──────────────┴─────────────────────┴─────────────────────────────────┘

┌──────────────┬─────────────────────┬─────────────────────────────────┐
│Event Status  │Event Date           │Event Name                       │
├──────────────┼─────────────────────┼─────────────────────────────────┤
│Active/Sched  │2025-07-22          │Kellogg's Morning Cereal Demo    │
└──────────────┴─────────────────────┴─────────────────────────────────┘

MUST BE SIGNED AND DATED

Event Specialist Printed Name: ________________________________
Event Specialist Signature:    ________________________________
Date Performed:                ________________________________
Supervisor Signature:          ________________________________
```

## 🔧 Configuration

### Event Type Codes
The system automatically translates these numeric codes:
- `1`: Sampling
- `2`: Demo/Sampling
- `3`: Cooking Demo
- `45`: Food Demo/Sampling (common)
- `46`: Beverage Demo
- And many more...

### Event Status Codes  
- `1`: Pending
- `2`: Active/Scheduled (common)
- `3`: In Progress
- `4`: Completed
- `5`: Cancelled
- And many more...

## 📦 Dependencies

### Required
- `requests>=2.28.0` - HTTP client for API communication
- `reportlab>=4.0.0` - Professional PDF generation

### Optional
- `weasyprint>=61.0` - Alternative PDF converter
- `typing-extensions>=4.5.0` - Enhanced type hints

## 🛠️ Advanced Features

### PDF Generation Methods
1. **ReportLab** (Primary): Professional-grade PDF generation with precise control
2. **WeasyPrint** (Fallback): HTML-to-PDF conversion for alternative rendering

### Error Handling
- Graceful degradation when PDF libraries aren't available
- Comprehensive logging of authentication and processing steps
- Automatic retry mechanisms for network requests

### Cross-Platform Support
- **Windows**: PowerShell and cmd printing methods
- **macOS**: Native `lp` command integration  
- **Linux**: Standard `lp` command support

## 🎨 Customization

### Column Width Optimization
Event name columns are automatically sized for better readability:
- Event Number: 1.3" (compact)
- Event Status: 1.3" (compact) 
- Event Name: 3.2" (expanded for full names)

### Signature Field Customization
Easily modify signature requirements in the `signature_data` array:
```python
signature_data = [
    ['Event Specialist Printed Name:', '________________________________'],
    ['Event Specialist Signature:', '________________________________'],
    ['Date Performed:', '________________________________'],
    ['Supervisor Signature:', '________________________________']
]
```

## 🔍 Troubleshooting

### Common Issues
1. **PDF Generation Fails**: Install ReportLab with `pip install reportlab>=4.0.0`
2. **Print Commands Fail**: PDFs are automatically opened for manual printing
3. **Authentication Issues**: Ensure MFA code is entered when prompted

### Debug Mode
Enable detailed logging by modifying the print statements or adding logging configuration.

## 📈 Performance

- **One-Time Authentication**: MFA required only once per session
- **Batch Processing**: Multiple events processed in sequence
- **Memory Efficient**: Reports processed individually to minimize RAM usage
- **Fast PDF Generation**: ReportLab optimized for speed and quality

## 🤝 Contributing

When extending the Enhanced EDR Printer:
1. Maintain the signature field formatting
2. Preserve the cover page functionality
3. Keep event code mappings updated
4. Test across different event types

## 📄 License

This module is part of the Product Connections Manager Platform and follows the same MIT license terms.

---

## 🏆 Success Metrics

The Enhanced EDR Printer has successfully addressed:
- ✅ Unreliable HTML printing through PDF consolidation
- ✅ Manual signature field requirements through custom formatting  
- ✅ Event name truncation through optimized column widths
- ✅ Code readability through human-friendly event descriptions
- ✅ Compliance requirements through "MUST BE SIGNED AND DATED" headers

**Ready for production use in Walmart Product Connections operations!** 🎉