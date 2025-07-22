#!/usr/bin/env python3
"""
Setup script for Product Connections Manager - Enhanced EDR Printer
"""

from setuptools import setup, find_packages
import os

# Read the README file for the long description
def read(fname):
    """Read file contents"""
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

# Read requirements.txt
def read_requirements(filename):
    """Read requirements from file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="product-connections-manager",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Enhanced EDR (Event Data Recorder) printer with PDF consolidation and professional formatting",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url="https://github.com/cyberiseeyou/product-connections-manager-platform",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'pdf': [
            'reportlab>=3.6.0',
            'PyPDF2>=3.0.0',
        ],
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'edr-printer=product_connections_manager.edr_printer.enhanced_edr_printer:main',
            'edr-automated=product_connections_manager.edr_printer.automated_edr_printer:main',
        ],
    },
    include_package_data=True,
    package_data={
        'product_connections_manager': ['*.txt', '*.md'],
    },
    keywords="edr, printer, pdf, automation, reports",
    project_urls={
        "Bug Reports": "https://github.com/cyberiseeyou/product-connections-manager-platform/issues",
        "Source": "https://github.com/cyberiseeyou/product-connections-manager-platform",
    },
)