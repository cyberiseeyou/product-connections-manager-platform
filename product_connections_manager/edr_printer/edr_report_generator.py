"""
EDR (Event Detail Report) Generator
==================================

This module provides functionality to generate Event Detail Reports from Walmart's Retail Link
Event Management System. It combines the authentication flow from testing_api_clean.py with
the EDR report generation capabilities derived from the provided cURL commands and frontend code.

Dependencies:
- requests: HTTP client library
- json: JSON handling
- datetime: Date/time utilities
- typing: Type hints

Usage:
    from edr_report_generator import EDRReportGenerator
    
    generator = EDRReportGenerator()
    generator.authenticate()  # Interactive authentication
    report_data = generator.get_edr_report(event_id="606034")
    html_report = generator.generate_html_report(report_data)
"""

import requests
import json
import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
import urllib.parse
import tempfile
import os
import subprocess
import platform


class EDRReportGenerator:
    """
    Event Detail Report Generator for Walmart Retail Link Event Management System.
    
    This class handles:
    1. Multi-factor authentication with Retail Link
    2. Event browsing and filtering
    3. EDR report data retrieval
    4. HTML report generation with print styling
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://retaillink2.wal-mart.com/EventManagement"
        self.auth_token = None
        self.user_data = None
        
        # Store credentials (in production, use environment variables)
        self.username = "mat.conder@productconnections.com"
        self.password = "Crossmark812Th$"
        self.mfa_credential_id = "18122365202"
        
        # Event report table headers from the JavaScript component
        self.report_headers = [
            "Item Number", "Primary Item Number", "Description", "Vendor", "Category"
        ]
        
        # Default store number for filtering (from cURL command)
        self.default_store_number = "8135"

    def _get_initial_cookies(self) -> Dict[str, str]:
        """Return initial cookies required for authentication."""
        return {
            'vtc': 'Q0JqQVX0STHy6sao9qdhNw',
            '_pxvid': '3c803a96-548a-11f0-84bf-e045250e632c',
            '_ga': 'GA1.2.103605184.1751648140',
            'QuantumMetricUserID': '23bc666aa80d92de6f4ffa5b79ff9fdc',
            'pxcts': 'd0d1b4d9-65f2-11f0-a59e-62912b00fffc',
            'rl_access_attempt': '0',
            'rlLoginInfo': '',
            'bstc': 'ZpNiPcM5OgU516Fy1nOhHw',
            'rl_show_login_form': 'N',
            'TS0111a950': '0164c7ecbba28bf006381fcf7bc3c3fbc81a9b73705f5cedd649131a664e0cc5179472f6c66a7cee46d5fc6556faef1eb07fb3b8db',
            'TS01b1e5a6': '0164c7ecbba28bf006381fcf7bc3c3fbc81a9b73705f5cedd649131a664e0cc5179472f6c66a7cee46d5fc6556faef1eb07fb3b8db',
            'mp_c586ded18141faef3e556292ef2810bc_mixpanel': '%7B%22distinct_id%22%3A%20%22d2fr4w2%20%20%20%20%20%22%2C%22%24device_id%22%3A%20%221981deb804c5f0-08ebcf61e7361f-26011151-e12d0-1981deb804d22c4%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fretaillink.login.wal-mart.com%2F%22%2C%22%24initial_referring_domain%22%3A%20%22retaillink.login.wal-mart.com%22%2C%22%24user_id%22%3A%20%22d2fr4w2%20%20%20%20%20%22%7D',
            'TS04fe286f027': '08a6069d6cab2000cf0b847458906d222e70afa03939fa0de76da5c00884f260a79443300cc5407408d2c3bf9e113000b642cbc898d0534c0c86a20a3d11bab7101afcd84708efbc3e17c493bcf63e44a30e69658f98e8ce282590fbc1283275',
            '_px3': '85d2f0646ea75d99a2faac1898a7785dc1c8c7807e2612e865c5b74b4059d5fb:UHj6hAC9RHoxLnDq2rdjE+HkchqIMD2wKeYTOfHkRyo03uaqeN4xA4DX8dbN5RrJrX+uLLB/HTtX12k0ymeoSg==:1000:9TQQXsEtZxJ8rnnXulfuBg/dxB30NwnoogsLoiaQFk/xQECXPbbFYCno02+QFD40nnBos0iUVfyD2CpgeCV+cIFLDpCggGG0LVI2Q5S4hDYjVHb0fhh7UQ2cqGLr55bijg0Ix75CQdsdWi+gc34m88u66pDWGpB13rAKmim6yJo7/mxA32DYqKWBKbTwG/HvVDaGQCGDa+Iog+lfBNePx/WdAInb6LQ00IZGqYrdrE0='
        }

    def _get_standard_headers(self, content_type: Optional[str] = None, referer: Optional[str] = None) -> Dict[str, str]:
        """Return standard headers for API requests."""
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        }
        
        if content_type:
            headers['content-type'] = content_type
            
        if referer:
            headers['referer'] = referer
            
        if self.auth_token:
            headers['authorization'] = f'Bearer {self.auth_token}'
            
        return headers

    def step1_submit_password(self) -> bool:
        """Step 1: Submit username and password."""
        login_url = "https://retaillink.login.wal-mart.com/api/login"
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://retaillink.login.wal-mart.com',
            'priority': 'u=1, i',
            'referer': 'https://retaillink.login.wal-mart.com/login',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }
        
        # Set initial cookies
        for name, value in self._get_initial_cookies().items():
            self.session.cookies.set(name, value)
        
        payload = {"username": self.username, "password": self.password, "language": "en"}
        
        print("➡️ Step 1: Submitting username and password...")
        try:
            response = self.session.post(login_url, headers=headers, json=payload)
            response.raise_for_status()
            print("✅ Password accepted. MFA required.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Step 1 failed: {e}")
            return False

    def step2_request_mfa_code(self) -> bool:
        """Step 2: Request MFA code to be sent to user's device."""
        send_code_url = "https://retaillink.login.wal-mart.com/api/mfa/sendCode"
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://retaillink.login.wal-mart.com',
            'referer': 'https://retaillink.login.wal-mart.com/login',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }
        payload = {"type": "SMS_OTP", "credid": self.mfa_credential_id}

        print("➡️ Step 2: Requesting MFA code...")
        try:
            response = self.session.post(send_code_url, headers=headers, json=payload)
            response.raise_for_status()
            print("✅ MFA code sent successfully. Check your device.")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Step 2 failed: {e}")
            return False

    def step3_validate_mfa_code(self, code: str) -> bool:
        """Step 3: Validate the MFA code entered by user."""
        validate_url = "https://retaillink.login.wal-mart.com/api/mfa/validateCode"
        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://retaillink.login.wal-mart.com',
            'referer': 'https://retaillink.login.wal-mart.com/login',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }
        payload = {
            "type": "SMS_OTP",
            "credid": self.mfa_credential_id,
            "code": code,
            "failureCount": 0
        }

        print("➡️ Step 3: Validating MFA code...")
        try:
            response = self.session.post(validate_url, headers=headers, json=payload)
            response.raise_for_status()
            print("✅ MFA authentication complete!")
            return True
        except requests.exceptions.RequestException as e:
            print(f"❌ Step 3 failed. The code may have been incorrect.")
            return False

    def step4_register_page_access(self) -> bool:
        """Step 4: Register page access to Event Management System."""
        url = "https://retaillink2.wal-mart.com/rl_portal_services/api/Site/InsertRlPageDetails"
        params = {
            'pageId': '6',
            'pageSubId': 'w6040',
            'pageSubDesc': 'Event Management System'
        }
        
        headers = self._get_standard_headers(referer='https://retaillink2.wal-mart.com/rl_portal/')
        headers['priority'] = 'u=1, i'
        
        print("➡️ Step 4: Registering page access...")
        try:
            response = self.session.get(url, headers=headers, params=params)
            if response.status_code == 200:
                print("✅ Page access registered")
                return True
            else:
                print(f"⚠️ Page registration status: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Page registration failed: {e}")
            return False

    def step5_navigate_to_event_management(self) -> bool:
        """Step 5: Navigate to Event Management system."""
        # Navigate to portal first
        portal_url = "https://retaillink2.wal-mart.com/rl_portal/"
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9',
            'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-site',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        }
        
        print("➡️ Step 5: Navigating to Event Management...")
        try:
            # First portal
            response = self.session.get(portal_url, headers=headers)
            if response.status_code != 200:
                print(f"❌ Portal access failed: {response.status_code}")
                return False
                
            # Then Event Management
            event_mgmt_url = f"{self.base_url}/"
            response = self.session.get(event_mgmt_url, headers=headers)
            if response.status_code == 200:
                print("✅ Event Management navigation successful")
                return True
            else:
                print(f"❌ Event Management access failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Navigation failed: {e}")
            return False

    def step6_authenticate_event_management(self) -> bool:
        """Step 6: Authenticate with Event Management API and extract auth token."""
        auth_url = f"{self.base_url}/api/authenticate"
        headers = self._get_standard_headers(referer=f"{self.base_url}/")
        
        print("➡️ Step 6: Authenticating with Event Management API...")
        try:
            response = self.session.get(auth_url, headers=headers)
            if response.status_code == 200:
                try:
                    auth_data = response.json()
                    print("✅ Event Management authentication successful!")
                    
                    # Extract auth token from cookies (based on cURL command)
                    for cookie in self.session.cookies:
                        if cookie.name == 'auth-token' and cookie.value:
                            # Parse the URL-encoded cookie value
                            cookie_data = urllib.parse.unquote(cookie.value)
                            try:
                                token_data = json.loads(cookie_data)
                                self.auth_token = token_data.get('token')
                                print(f"🔑 Auth token extracted: {self.auth_token[:50]}...")
                                return True
                            except json.JSONDecodeError:
                                print("⚠️ Could not parse auth-token cookie")
                    
                    print("⚠️ auth-token cookie not found")
                    return False
                    
                except json.JSONDecodeError:
                    print("⚠️ Authentication response not JSON but status OK")
                    return True
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Authentication API call failed: {e}")
            return False

    def authenticate(self) -> bool:
        """
        Complete authentication flow.
        Returns True if successful, False otherwise.
        """
        print("🔐 Starting Retail Link authentication...")
        
        # Step 1: Submit password
        if not self.step1_submit_password():
            return False

        # Step 2: Request MFA code
        if not self.step2_request_mfa_code():
            return False

        # Step 3: Get MFA code from user and validate
        mfa_code = input("📱 Please enter the MFA code you received: ").strip()
        if not self.step3_validate_mfa_code(mfa_code):
            return False
        
        # Step 4: Register page access
        if not self.step4_register_page_access():
            print("⚠️ Page registration failed, continuing...")
        
        # Step 5: Navigate to Event Management
        if not self.step5_navigate_to_event_management():
            print("⚠️ Navigation failed, continuing...")
        
        # Step 6: Authenticate and get token
        if not self.step6_authenticate_event_management():
            print("❌ Could not obtain auth token")
            return False
        
        print("✅ Full authentication completed successfully!")
        return True

    def browse_events(self, start_date: Optional[str] = None, end_date: Optional[str] = None, 
                     store_number: Optional[str] = None, event_types: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Browse events using the API endpoint from cURL command 3.
        
        Args:
            start_date: Start date in YYYY-MM-DD format (defaults to current month)
            end_date: End date in YYYY-MM-DD format (defaults to current month)
            store_number: Store number (defaults to 8135)
            event_types: List of event type IDs (defaults to all types)
            
        Returns:
            Dictionary containing event browse results
        """
        if not self.auth_token:
            raise ValueError("Must authenticate first before browsing events")
        
        # Set defaults based on cURL command
        if not start_date or not end_date:
            now = datetime.datetime.now()
            start_date = f"{now.year}-{now.month:02d}-01"
            end_date = f"{now.year}-{now.month:02d}-{now.day:02d}"
        
        if not store_number:
            store_number = self.default_store_number
        
        if not event_types:
            # All event types from cURL command
            event_types = [1,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
        
        url = f"{self.base_url}/api/browse-event/browse-data"
        headers = self._get_standard_headers(
            content_type='application/json',
            referer=f"{self.base_url}/browse-event"
        )
        headers['origin'] = 'https://retaillink2.wal-mart.com'
        headers['priority'] = 'u=1, i'
        
        payload = {
            "itemNbr": None,
            "vendorNbr": None,
            "startDate": start_date,
            "endDate": end_date,
            "billType": None,
            "eventType": event_types,
            "userId": None,
            "primItem": None,
            "storeNbr": store_number,
            "deptNbr": None
        }
        
        print(f"🔍 Browsing events from {start_date} to {end_date} for store {store_number}...")
        try:
            response = self.session.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            events_data = response.json()
            print(f"✅ Found {len(events_data)} events")
            return events_data
        except requests.exceptions.RequestException as e:
            print(f"❌ Event browsing failed: {e}")
            return {}

    def get_edr_report(self, event_id: str) -> Dict[str, Any]:
        """
        Get EDR report data for a specific event ID.
        
        Args:
            event_id: The event ID to retrieve the report for
            
        Returns:
            Dictionary containing EDR report data
        """
        if not self.auth_token:
            raise ValueError("Must authenticate first before getting EDR report")
        
        url = f"{self.base_url}/api/edrReport?id={event_id}"
        headers = self._get_standard_headers(referer=f"{self.base_url}/browse-event")
        
        print(f"📄 Retrieving EDR report for event {event_id}...")
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            
            report_data = response.json()
            print(f"✅ EDR report retrieved successfully")
            return report_data
        except requests.exceptions.RequestException as e:
            print(f"❌ EDR report retrieval failed: {e}")
            return {}

    def get_event_detail_report_page(self) -> str:
        """
        Get the event detail report page HTML (from cURL command 1).
        
        Returns:
            HTML content of the event detail report page
        """
        url = f"{self.base_url}/event-detail-report?_rsc=h0aj8"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Referer': f"{self.base_url}/create-event"
        }
        
        print("📋 Retrieving event detail report page...")
        try:
            response = self.session.get(url, headers=headers)
            response.raise_for_status()
            print("✅ Event detail report page retrieved")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"❌ Event detail report page retrieval failed: {e}")
            return ""

    def generate_html_report(self, edr_data: Dict[str, Any]) -> str:
        """
        Generate HTML report based on the React component structure and CSS styling.
        
        Args:
            edr_data: EDR report data from get_edr_report()
            
        Returns:
            Complete HTML report ready for printing
        """
        # Get current date and time for the report header
        now = datetime.datetime.now()
        report_date = now.strftime("%Y-%m-%d")
        report_time = now.strftime("%H:%M:%S")
        
        # Extract event information (adjust based on actual API response structure)
        event_number = edr_data.get('demoId', 'N/A') if edr_data else 'N/A'
        event_type = edr_data.get('demoClassCode', 'N/A') if edr_data else 'N/A'
        event_status = edr_data.get('demoStatusCode', 'N/A') if edr_data else 'N/A'
        event_date = edr_data.get('demoDate', 'N/A') if edr_data else 'N/A'
        event_name = edr_data.get('demoName', 'N/A') if edr_data else 'N/A'
        event_locked = edr_data.get('demoLockInd', 'N/A') if edr_data else 'N/A'
        
        # Instructions
        instructions = edr_data.get('demoInstructions', {}) if edr_data else {}
        event_prep = instructions.get('demoPrepnTxt', 'N/A') if instructions else 'N/A'
        event_portion = instructions.get('demoPortnTxt', 'N/A') if instructions else 'N/A'
        
        # Item details
        item_details = edr_data.get('itemDetails', []) if edr_data else []
        
        # Generate table rows for items
        item_rows = ""
        for item in item_details:
            item_rows += f"""
                <tr class="edr-wrapper">
                    <td class="report-table-content">{item.get('itemNbr', '')}</td>
                    <td class="report-table-content">{item.get('gtin', '')}</td>
                    <td class="report-table-content">{item.get('itemDesc', '')}</td>
                    <td class="report-table-content">{item.get('vendorNbr', '')}</td>
                    <td class="report-table-content">{item.get('deptNbr', '')}</td>
                </tr>
            """

        # Complete HTML template based on the React component and CSS
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Event Management System - EDR Report</title>
    <style>
        /* CSS from the provided files combined with print optimization */
        body {{ 
            font-family: Arial, sans-serif; 
            padding: 20px; 
            margin: 0;
        }}
        
        .detail-header {{ 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            font-weight: 700;
            font-size: 24px;
            margin-bottom: 20px;
        }}
        
        .elememnt-padding {{ 
            padding: 10px 0; 
        }}
        
        .font-weight-bold {{ 
            font-size: 18px; 
            margin-top: 10px; 
            margin-bottom: 10px; 
            font-weight: bold;
        }}
        
        .space-underlined {{ 
            display: inline-block; 
            width: calc(80% - 230px); 
            border-bottom: 1px solid black;
            margin-left: 10px;
        }}
        
        .instruction-heading {{ 
            margin-top: 10px; 
            margin-bottom: 10px; 
            font-size: 18px; 
            font-weight: 500; 
        }}
        
        .report-footer div {{ 
            padding: 2px 0; 
        }}
        
        .report-first {{ 
            margin-left: 20%; 
        }}
        
        .help-text {{ 
            font-size: 14px; 
            line-height: 1.2; 
        }}
        
        .demo-text {{ 
            margin-left: 12px; 
            font-weight: 700; 
        }}
        
        .col-40 {{ 
            flex: 0 0 40%; 
            max-width: 40%; 
        }}
        
        .report-table-content {{ 
            text-align: center; 
        }}
        
        .row {{ 
            display: flex; 
            padding: 5px; 
            width: 100%; 
        }}
        
        .col {{ 
            flex: 1; 
            display: block; 
            padding: 5px; 
            width: 100%; 
        }}
        
        .col-25 {{ 
            flex: 0 0 25%; 
            max-width: 25%; 
        }}
        
        .input-label {{ 
            font-weight: normal; 
        }}
        
        td {{ 
            padding: 8px; 
            border-top: solid 1px #ccc; 
            font-family: arial; 
            font-size: 12px; 
            text-align: left; 
            font-weight: 400; 
            color: grey; 
            line-height: 18px; 
        }}
        
        table {{ 
            width: 100%; 
            border-collapse: collapse; 
            text-align: center; 
            font-size: 94%; 
            outline: #ccc solid 1px; 
            table-layout: fixed; 
            margin-bottom: 10px; 
        }}
        
        th {{ 
            padding: 5px; 
            background: #e2e1e1; 
            font-size: 14px; 
            font-weight: 400; 
            color: grey; 
        }}
        
        .demo-table-header {{ 
            background: #e2e1e1; 
        }}
        
        hr {{ 
            border: 1px solid #ccc; 
            margin: 10px 0; 
        }}
        
        @media print {{
            body {{ 
                padding: 10px; 
            }}
            .print-button {{ 
                display: none; 
            }}
        }}
    </style>
</head>
<body>
    <div id="reportDdr_pdf">
        <div class="detail-header">EVENT DETAIL REPORT</div>
        
        <div class="elememnt-padding font-weight-bold">
            <span>RUN ON </span>
            <span>{report_date}</span>
            <span> AT </span>
            <span>{report_time}</span>
        </div>
        
        <hr>
        
        <div class="elememnt-padding help-text">
            <div>
                <span class="report-first">IMPORTANT!!!</span> 
                This report should be printed each morning prior to completing each event.<br>
                1. The Event Details Report should be kept in the event prep area for each demonstrator to review instructions and item status.<br>
                2. The Event Co-ordinator should use this sheet when visiting the event area. Comments should be written to enter into the system at a later time.<br>
                3. Remember to scan items for product charge using the Club Use function on the handheld device.<br>
                Retention: This report should be kept in a monthly folder with the most recent being put in the front. The previous 6 months need to be kept accessible in the event prep area. Reports older than 6 months should be boxed and stored. Discard any report over 18 months old.
            </div>
        </div>
        
        <hr>
        
        <div id="demo_div">
            <div class="row responsive-md">
                <div class="col col-25">
                    <span class="input-label" title="Event Number">
                        Event Number <span class="demo-text">{event_number}</span>
                    </span>
                </div>
                <div class="col col-25">
                    <span class="input-label" title="Event Type">
                        Event Type <span class="demo-text">{event_type}</span>
                    </span>
                </div>
                <div class="col col-40">
                    <span class="input-label" title="Event Locked">
                        Event Locked <span class="demo-text">{event_locked}</span>
                    </span>
                </div>
            </div>
            
            <div class="row responsive-md">
                <div class="col col-25">
                    <span class="input-label" title="Event Status">
                        Event Status <span class="demo-text">{event_status}</span>
                    </span>
                </div>
                <div class="col col-25">
                    <span class="input-label" title="Event Date">
                        Event Date <span class="demo-text">{event_date}</span>
                    </span>
                </div>
                <div class="col col-40">
                    <span class="input-label" title="Event Name">
                        Event Name <span class="demo-text" title="{event_name}">{event_name}</span>
                    </span>
                </div>
            </div>
        </div>
        
        <div id="demo_pdf">
            <table id="new_event">
                <thead>
                    <tr class="demo-table-header">
                        <th>Item Number</th>
                        <th>Primary Item Number</th>
                        <th>Description</th>
                        <th>Vendor</th>
                        <th>Category</th>
                    </tr>
                </thead>
                <tbody>
                    {item_rows}
                </tbody>
            </table>
        </div>
        
        <h4 class="instruction-heading">Instructions:</h4>
        
        <div>
            <span class="input-label" title="Event Preparation">
                Event Preparation: <span class="demo-text">{event_prep}</span>
            </span>
            <div>
                <span class="input-label" title="Event Portion">
                    Event Portion: <span class="demo-text">{event_portion}</span>
                </span>
            </div>
        </div>
        
        <div class="report-footer">
            <div>
                <span>Club Associate Printed Name:</span>
                <span class="space-underlined"></span>
            </div>
            <div>
                <span>Club Associate Signature:</span>
                <span class="space-underlined"></span>
            </div>
            <div>
                <span>Club Associate Title:</span>
                <span class="space-underlined"></span>
            </div>
            <div>
                <span>Date:</span>
                <span class="space-underlined"></span>
            </div>
            <div>
                <span>Tastes & Tips Rep Signature:</span>
                <span class="space-underlined"></span>
            </div>
        </div>
        
        <div class="print-button" style="margin-top: 20px; text-align: right;">
            <button onclick="window.print()" style="padding: 10px 20px; background: #1976d2; color: white; border: none; border-radius: 4px; cursor: pointer;">
                🖨️ Print Report
            </button>
        </div>
    </div>
</body>
</html>
        """
        
        return html_content.strip()

    def save_html_report(self, html_content: str, filename: Optional[str] = None) -> str:
        """
        Save HTML report to file.
        
        Args:
            html_content: HTML content to save
            filename: Optional filename (defaults to timestamp-based name)
            
        Returns:
            Path to saved file
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"edr_report_{timestamp}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 Report saved to: {filename}")
        return filename

    def print_html_report(self, html_content: str, temp_filename: Optional[str] = None) -> bool:
        """
        Print HTML report directly to the default printer without user interaction.
        
        Args:
            html_content: HTML content to print
            temp_filename: Optional temporary filename (auto-generated if not provided)
            
        Returns:
            True if print job was sent successfully, False otherwise
        """
        try:
            # Create temporary file if needed
            if not temp_filename:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                temp_filename = f"temp_edr_report_{timestamp}.html"
            
            # Save HTML to temporary file
            temp_path = os.path.join(tempfile.gettempdir(), temp_filename)
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"🖨️ Printing report to default printer...")
            print(f"📁 Temporary file: {temp_path}")
            
            # Platform-specific printing
            system = platform.system().lower()
            
            if system == "windows":
                # Try multiple Windows printing methods
                result = (self._print_on_windows_simple(temp_path) or 
                         self._print_on_windows_advanced(temp_path) or
                         self._print_on_windows_fallback(temp_path))
            elif system == "darwin":  # macOS
                result = self._print_on_macos(temp_path)
            elif system == "linux":
                result = self._print_on_linux(temp_path)
            else:
                print(f"❌ Unsupported operating system: {system}")
                return False
            
            if result:
                print("✅ Print job sent successfully to default printer")
                
                # Clean up temporary file after a longer delay to ensure printing completes
                try:
                    import time
                    print("⏳ Waiting for print job to complete...")
                    time.sleep(5)  # Give printer more time to read the file
                    os.remove(temp_path)
                    print("🗑️ Temporary file cleaned up")
                except OSError as e:
                    print(f"⚠️ Could not remove temporary file: {temp_path} - {e}")
                
                return True
            else:
                print("❌ Failed to send print job")
                print(f"📁 Report file remains at: {temp_path}")
                print("🗑️ Cleaning up temporary file...")
                try:
                    os.remove(temp_path)
                    print("✅ Temporary file cleaned up")
                except OSError:
                    pass
                return False
                
        except Exception as e:
            print(f"❌ Print operation failed: {e}")
            return False

    def _print_on_windows_simple(self, file_path: str) -> bool:
        """Simple Windows printing using start command with /wait to prevent popups."""
        try:
            print("🖨️ Method 1: Using Windows start command with print verb...")
            abs_path = os.path.abspath(file_path)
            
            # Use /wait to prevent browser from staying open, /min to minimize
            result = subprocess.run([
                "cmd", "/c", "start", "/wait", "/min", "", "/print", abs_path
            ], capture_output=True, text=True, timeout=15)
            
            success = result.returncode == 0
            if success:
                print("✅ Print command successful")
            else:
                print(f"⚠️ Print command failed with code: {result.returncode}")
                
            return success
            
        except subprocess.TimeoutExpired:
            print("⚠️ Print command timed out")
            return False
        except Exception as e:
            print(f"⚠️ Simple print method failed: {e}")
            return False

    def _print_on_windows_advanced(self, file_path: str) -> bool:
        """Advanced Windows printing using PowerShell with better control."""
        try:
            print("🖨️ Method 2: Using PowerShell with hidden window...")
            abs_path = os.path.abspath(file_path)
            
            # Use PowerShell with WindowStyle Hidden to prevent popup
            ps_cmd = f'Start-Process -FilePath "{abs_path}" -Verb Print -WindowStyle Hidden -Wait'
            
            result = subprocess.run([
                "powershell.exe", "-WindowStyle", "Hidden", "-Command", ps_cmd
            ], capture_output=True, text=True, timeout=15)
            
            success = result.returncode == 0
            if success:
                print("✅ PowerShell print command successful")
            else:
                print(f"⚠️ PowerShell print failed with code: {result.returncode}")
                
            return success
            
        except subprocess.TimeoutExpired:
            print("⚠️ PowerShell print command timed out")
            return False
        except Exception as e:
            print(f"⚠️ Advanced print method failed: {e}")
            return False

    def _print_on_windows_fallback(self, file_path: str) -> bool:
        """Fallback Windows printing - use print command directly."""
        try:
            print("🖨️ Method 3: Using Windows print command...")
            abs_path = os.path.abspath(file_path)
            
            # Try using the print command directly
            result = subprocess.run([
                "print", abs_path
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print("✅ Direct print command successful")
                return True
            else:
                print(f"⚠️ Direct print failed with code: {result.returncode}")
                print("❌ All automatic printing methods failed")
                print(f"📁 Report saved at: {abs_path}")
                print("💡 You can manually print this file if needed")
                return False
                
        except Exception as e:
            print(f"⚠️ Fallback print method failed: {e}")
            print("❌ All automatic printing methods failed")
            print(f"📁 Report saved at: {file_path}")
            return False

    def _print_on_macos(self, file_path: str) -> bool:
        """Print HTML file on macOS using lp or open command."""
        try:
            # Method 1: Try using lp with HTML file directly
            result = subprocess.run([
                "lp", "-d", "default", file_path
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                return True
            
            # Method 2: Use open command to print via default browser
            result = subprocess.run([
                "open", "-a", "Safari", file_path
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Send print command via AppleScript
                applescript = '''
                tell application "Safari"
                    delay 2
                    tell application "System Events"
                        keystroke "p" using command down
                        delay 1
                        keystroke return
                    end tell
                end tell
                '''
                
                subprocess.run([
                    "osascript", "-e", applescript
                ], timeout=10)
                return True
            
            return False
            
        except subprocess.TimeoutExpired:
            print("⚠️ Print operation timed out")
            return False
        except Exception as e:
            print(f"⚠️ macOS print method failed: {e}")
            return False

    def _print_on_linux(self, file_path: str) -> bool:
        """Print HTML file on Linux using lp command."""
        try:
            # Method 1: Try using lp command with default printer
            result = subprocess.run([
                "lp", file_path
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                return True
            
            # Method 2: Try using lpr command
            result = subprocess.run([
                "lpr", file_path
            ], capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                return True
            
            # Method 3: Use xdg-open and attempt to print via default browser
            result = subprocess.run([
                "xdg-open", file_path
            ], capture_output=True, text=True, timeout=10)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("⚠️ Print operation timed out")
            return False
        except Exception as e:
            print(f"⚠️ Linux print method failed: {e}")
            return False

    def generate_and_print_edr_report(self, event_id: str, save_copy: bool = True) -> bool:
        """
        Complete workflow: Get EDR data, generate HTML report, and print automatically.
        
        Args:
            event_id: The event ID to generate and print report for
            save_copy: Whether to save a permanent copy of the report (default: True)
            
        Returns:
            True if the entire process was successful, False otherwise
        """
        if not self.auth_token:
            print("❌ Must authenticate first before generating reports")
            return False
        
        print(f"📋 Starting EDR report generation and printing for event {event_id}...")
        
        # Step 1: Get EDR data
        print("📄 Retrieving EDR data...")
        edr_data = self.get_edr_report(event_id)
        if not edr_data:
            print("❌ Failed to retrieve EDR data")
            return False
        
        # Step 2: Generate HTML report
        print("🔧 Generating HTML report...")
        html_report = self.generate_html_report(edr_data)
        if not html_report:
            print("❌ Failed to generate HTML report")
            return False
        
        # Step 3: Save permanent copy if requested
        saved_file = None
        if save_copy:
            print("💾 Saving permanent copy...")
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            saved_file = self.save_html_report(
                html_report, 
                f"edr_report_{event_id}_{timestamp}.html"
            )
        
        # Step 4: Print the report
        print("🖨️ Sending to printer...")
        print_success = self.print_html_report(html_report)
        
        if print_success:
            print("✅ EDR report generated and printed successfully!")
            if saved_file:
                print(f"📁 Permanent copy saved as: {saved_file}")
            return True
        else:
            print("❌ Report generated but printing failed")
            if saved_file:
                print(f"📁 Report still saved as: {saved_file}")
            return False


# Example usage and testing
if __name__ == "__main__":
    # Automated usage - no user interaction
    generator = EDRReportGenerator()
    
    print("🤖 Running in automated mode - no user interaction")
    print("⚠️ Note: MFA authentication will fail in automated mode")
    print("📋 This script is designed for use after manual authentication")
    
    # For automated usage, assume authentication is already handled
    # or use this for testing the report generation parts only
    
    # Example of automated report generation (would need pre-authenticated session)
    # event_id = "606034"  # Default event ID for testing
    # 
    # if generator.auth_token:  # Only if already authenticated
    #     print(f"🖨️ Generating and printing EDR report for event {event_id}...")
    #     success = generator.generate_and_print_edr_report(event_id, save_copy=True)
    #     if success:
    #         print("✅ EDR report generated, saved, and sent to printer!")
    #     else:
    #         print("❌ Failed to complete the automated process")
    # else:
    #     print("❌ No authentication token available for automated operation")
    
    print("� For automated usage, integrate this class into your workflow after authentication")
