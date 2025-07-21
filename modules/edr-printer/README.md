# EDR Printer Module

**Status**: ✅ Production Ready  
**Version**: 1.0.0  
**Last Updated**: July 21, 2025

A fully automated Event Detail Report (EDR) generation and printing system for Walmart's Retail Link Event Management System. This module minimizes user interaction to a single MFA authentication step, then automatically processes multiple events and prints reports.

## Features

- **🔐 One-Time Authentication**: Only requires MFA code entry once per session
- **📦 Batch Processing**: Process multiple events automatically with a single command
- **🖨️ Silent Printing**: Prints directly to default printer without browser popups
- **🗑️ Automatic Cleanup**: Removes temporary files after processing
- **⚡ Command Line Interface**: Easy to use from command line or scripts
- **🔄 Session Management**: Reuses authentication token for multiple reports
- **🛡️ Error Handling**: Comprehensive error reporting and recovery

## Quick Start

1. **Navigate to the module**:
   ```bash
   cd modules/edr-printer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure credentials** (edit `edr_report_generator.py`):
   ```python
   self.username = "your.email@company.com"
   self.password = "your_password"
   self.mfa_credential_id = "your_mfa_id"
   ```

4. **Run with default events**:
   ```bash
   python automated_edr_printer.py
   ```

5. **Run with specific events**:
   ```bash
   python automated_edr_printer.py 606034 606035 606036
   ```

## System Requirements

- **Operating System**: Windows (tested on Windows 10/11)
- **Python**: 3.7 or higher
- **Printer**: Default printer configured in Windows
- **Network**: Access to Walmart Retail Link (retaillink2.wal-mart.com)

## Usage Examples

### Command Line Usage

```bash
# Process default events (configured in the script)
python automated_edr_printer.py

# Process specific events
python automated_edr_printer.py 606034 606035 606036

# Process single event
python automated_edr_printer.py 606034
```

### Programmatic Usage

```python
from automated_edr_printer import AutomatedEDRPrinter

# Create printer instance
printer = AutomatedEDRPrinter()

# Process events with authentication
success = printer.run_automated_batch(['606034', '606035'])

# Or set custom default events
printer.DEFAULT_EVENT_IDS = ['606034', '606035', '606036']
success = printer.run_automated_batch()
```

### Integration with Platform

```python
# Platform integration example
from modules.edr_printer.automated_edr_printer import AutomatedEDRPrinter
from shared.authentication import get_platform_auth

# Use platform authentication
printer = AutomatedEDRPrinter()
token = get_platform_auth("retail_link")
printer.set_authentication_manually(token)

# Process events
results = printer.process_event_list(['606034', '606035'])
```

## Configuration

### Default Event IDs
Edit the `DEFAULT_EVENT_IDS` list in `automated_edr_printer.py`:

```python
self.DEFAULT_EVENT_IDS = [
    "606034",  # Your event ID here
    "606035",  # Add more as needed
    "606036",
]
```

### Authentication Credentials
Update credentials in `edr_report_generator.py`:

```python
self.username = "your.email@company.com"
self.password = "your_password"
self.mfa_credential_id = "your_mfa_id"
```

## How It Works

### Authentication Flow
1. **Username/Password**: Submitted automatically using stored credentials
2. **MFA Request**: System requests MFA code to be sent to your device
3. **MFA Validation**: User enters code once, system validates and stores token
4. **Token Reuse**: All subsequent API calls use the stored authentication token

### Report Generation Process
1. **Event Data Retrieval**: Fetch EDR data from Retail Link API
2. **HTML Generation**: Create formatted HTML report with CSS styling
3. **Printing**: Send report directly to default printer using Windows print commands
4. **File Management**: Clean up temporary files automatically

### Printing Methods
The system uses multiple printing methods with automatic fallback:
1. **Windows Print Command**: Direct `print` command (most reliable)
2. **PowerShell**: Hidden window PowerShell execution with `/wait` and `/min` flags
3. **Direct Print**: Windows `print` command fallback
4. **Error Handling**: Graceful failure with file preservation

## File Structure

```
modules/edr-printer/
├── automated_edr_printer.py    # Main automation script
├── edr_report_generator.py     # Core EDR generation and printing
├── edr_session_manager.py      # Session and configuration management
├── requirements.txt            # Module-specific dependencies
├── README.md                   # This file
├── config.json                 # Module configuration
├── tests/                      # Module test suite
│   ├── test_automated_printer.py
│   ├── test_edr_generator.py
│   └── test_session_manager.py
└── examples/                   # Usage examples
    ├── basic_usage.py
    ├── batch_processing.py
    └── platform_integration.py
```

## API Reference

### AutomatedEDRPrinter Class

#### Methods

**`__init__()`**
- Initializes the printer with default configuration

**`authenticate_once() -> bool`**
- Performs one-time authentication for the session
- Returns: True if successful, False otherwise

**`set_authentication_manually(auth_token: str) -> None`**
- Sets authentication token manually
- Args: `auth_token` - Pre-obtained authentication token

**`process_event_list(event_ids: List[str], save_copies: bool, print_reports: bool) -> dict`**
- Processes a list of event IDs automatically
- Args: 
  - `event_ids` - List of event IDs to process
  - `save_copies` - Whether to save permanent copies
  - `print_reports` - Whether to send to printer
- Returns: Dictionary with processing results

**`run_automated_batch(event_ids: List[str], authenticate: bool) -> bool`**
- Runs complete automated batch job
- Args:
  - `event_ids` - List of event IDs to process
  - `authenticate` - Whether to perform authentication
- Returns: True if all events processed successfully

## Error Handling

### Common Errors

#### Authentication Issues
- **Invalid MFA Code**: Ensure you're entering the latest code from your device
- **Token Expiration**: Restart the script to re-authenticate
- **Network Issues**: Check VPN connection to Walmart Retail Link

#### Printing Issues
- **No Default Printer**: Configure a default printer in Windows
- **Print Queue**: Check Windows print queue for stuck jobs
- **File Permissions**: Ensure write access to temp directory

#### Event Processing Errors
- **Invalid Event ID**: Verify event ID exists in the system
- **Network Timeout**: Check internet connectivity
- **API Rate Limiting**: Wait before retrying requests

## Testing

Run the module tests:

```bash
cd modules/edr-printer
python -m pytest tests/
```

Run specific test categories:

```bash
# Test authentication
python -m pytest tests/test_automated_printer.py -k "test_auth"

# Test printing functionality
python -m pytest tests/test_edr_generator.py -k "test_print"

# Test session management
python -m pytest tests/test_session_manager.py
```

## Automation & Scheduling

### Windows Task Scheduler
Create a daily automated task:

```batch
schtasks /create /tn "EDR Daily Reports" /tr "python C:\path\to\platform\modules\edr-printer\automated_edr_printer.py" /sc daily /st 08:00
```

### Platform Integration
Use with the platform's scheduling system:

```python
from shared.scheduler import PlatformScheduler
from modules.edr_printer.automated_edr_printer import AutomatedEDRPrinter

scheduler = PlatformScheduler()
printer = AutomatedEDRPrinter()

# Schedule daily EDR processing
scheduler.schedule_daily(
    name="EDR Reports",
    time="08:00",
    function=printer.run_automated_batch,
    args=[['606034', '606035', '606036']]
)
```

## Dependencies

- **requests**: HTTP client for API communication
- **datetime**: Date/time handling (built-in)
- **tempfile**: Temporary file management (built-in)
- **subprocess**: System command execution (built-in)
- **platform**: OS detection for printing (built-in)
- **json**: JSON data handling (built-in)
- **urllib**: URL handling (built-in)
- **typing**: Type hints (built-in)

## Contributing to the Module

1. Follow the platform contributing guidelines
2. Add comprehensive tests for new features
3. Update this README for any changes
4. Ensure compatibility with other platform modules
5. Test integration with shared platform components

## Security Considerations

- **Credentials**: Use platform's secure credential storage
- **MFA**: Required for each session (cannot be bypassed)
- **Network**: Uses HTTPS for all API communications
- **Files**: Temporary files are automatically cleaned up
- **Tokens**: Authentication tokens are stored securely in memory

## Performance

- **Authentication**: ~10-15 seconds for initial setup
- **Report Generation**: ~2-3 seconds per event
- **Printing**: ~5-10 seconds per report (including cleanup)
- **Memory Usage**: ~50-100MB during operation
- **Disk Usage**: Minimal (temporary files are cleaned up)

## Changelog

### Version 1.0.0 (July 21, 2025)
- Initial release as part of Product Connections Manager Platform
- One-time MFA authentication with session token reuse
- Batch event processing capability
- Silent printing without browser popups
- Automatic file cleanup and error handling
- Command line interface and programmatic API
- Integration with platform authentication system
- Comprehensive test suite and documentation

---

**Module Maintainer**: CyberISeeYou  
**Platform**: Product Connections Manager Platform  
**Repository**: [GitHub](https://github.com/cyberiseeyou/product-connections-manager-platform)

For platform-wide issues, see the [main platform documentation](../../README.md).