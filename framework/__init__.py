
"""
Automotas AI Testing Framework
=============================

A comprehensive testing framework for the Automotas AI platform providing:
- Modular test architecture
- API integration testing
- Performance and load testing  
- Security vulnerability testing
- Multi-agent system testing
- N8N workflow integration
- Automated reporting
- Continuous monitoring

Usage:
    python run_tests.py --help
"""

__version__ = "1.0.0"
__author__ = "Automotas AI Team"
__email__ = "testing@automotas.ai"

from .config import test_config, TestLevel, TestEnvironment
from .base_test import BaseTest, APITest, DatabaseTest, WorkflowTest
from .test_runner import TestRunner
from .reporting import TestReporter

__all__ = [
    "test_config",
    "TestLevel", 
    "TestEnvironment",
    "BaseTest",
    "APITest", 
    "DatabaseTest",
    "WorkflowTest",
    "TestRunner",
    "TestReporter"
]
