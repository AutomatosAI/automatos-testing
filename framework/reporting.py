
"""
Test Reporting System for Automotas AI Testing Framework
========================================================

Generates comprehensive test reports in multiple formats.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import asdict

from .config import test_config

class TestReporter:
    """Generates test reports in various formats"""
    
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    async def generate_report(self, summary: Dict[str, Any], 
                            detailed_results: Dict[str, Any]):
        """Generate reports in configured formats"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Always generate JSON report
        await self._generate_json_report(summary, detailed_results, timestamp)
        
        # Generate HTML report if configured
        if test_config.report_format == "html":
            await self._generate_html_report(summary, detailed_results, timestamp)
            
        # Generate JUnit XML for CI/CD
        await self._generate_junit_xml(summary, detailed_results, timestamp)
        
    async def _generate_json_report(self, summary: Dict[str, Any], 
                                   detailed_results: Dict[str, Any], 
                                   timestamp: str):
        """Generate JSON report"""
        report_data = {
            "summary": summary,
            "detailed_results": detailed_results,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "framework_version": "1.0.0",
                "environment": test_config.environment.value
            }
        }
        
        json_file = self.output_dir / f"test_report_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
            
        print(f"📊 JSON report generated: {json_file}")
        
    async def _generate_html_report(self, summary: Dict[str, Any], 
                                   detailed_results: Dict[str, Any], 
                                   timestamp: str):
        """Generate HTML report"""
        html_content = self._create_html_template(summary, detailed_results)
        
        html_file = self.output_dir / f"test_report_{timestamp}.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
            
        print(f"📊 HTML report generated: {html_file}")
        
    async def _generate_junit_xml(self, summary: Dict[str, Any], 
                                 detailed_results: Dict[str, Any], 
                                 timestamp: str):
        """Generate JUnit XML for CI/CD integration"""
        xml_content = self._create_junit_xml(summary, detailed_results)
        
        xml_file = self.output_dir / f"junit_results_{timestamp}.xml"
        with open(xml_file, 'w') as f:
            f.write(xml_content)
            
        print(f"📊 JUnit XML generated: {xml_file}")
        
    def _create_html_template(self, summary: Dict[str, Any], 
                             detailed_results: Dict[str, Any]) -> str:
        """Create HTML report template"""
        status_color = "#28a745" if summary["status"] == "passed" else "#dc3545"
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automotas AI Test Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; border-bottom: 2px solid #e9ecef; padding-bottom: 20px; }}
        .status-badge {{ padding: 10px 20px; border-radius: 25px; color: white; font-weight: bold; background-color: {status_color}; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .metric-card {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border-left: 4px solid #007bff; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
        .metric-label {{ color: #6c757d; margin-top: 5px; }}
        .test-suite {{ margin: 20px 0; border: 1px solid #dee2e6; border-radius: 8px; }}
        .suite-header {{ background: #f8f9fa; padding: 15px; border-bottom: 1px solid #dee2e6; }}
        .suite-name {{ font-weight: bold; font-size: 1.1em; }}
        .test-list {{ padding: 0; }}
        .test-item {{ padding: 10px 15px; border-bottom: 1px solid #f1f3f4; display: flex; justify-content: between; align-items: center; }}
        .test-item:last-child {{ border-bottom: none; }}
        .test-passed {{ color: #28a745; }}
        .test-failed {{ color: #dc3545; }}
        .test-skipped {{ color: #ffc107; }}
        .duration {{ color: #6c757d; font-size: 0.9em; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Automotas AI Test Report</h1>
            <div class="status-badge">{summary["status"].upper()}</div>
            <p>Generated on {summary["timestamp"]}</p>
            <p>Environment: <strong>{summary["environment"]}</strong></p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-value">{summary["total_tests"]}</div>
                <div class="metric-label">Total Tests</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #28a745;">{summary["passed"]}</div>
                <div class="metric-label">Passed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #dc3545;">{summary["failed"]}</div>
                <div class="metric-label">Failed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value" style="color: #ffc107;">{summary["skipped"]}</div>
                <div class="metric-label">Skipped</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary["success_rate"]:.1f}%</div>
                <div class="metric-label">Success Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary["duration"]:.1f}s</div>
                <div class="metric-label">Duration</div>
            </div>
        </div>
        
        <h2>Test Suite Details</h2>
        """
        
        # Add test suite details
        for suite_name, suite_data in detailed_results.items():
            html += f"""
        <div class="test-suite">
            <div class="suite-header">
                <div class="suite-name">{suite_name}</div>
                <div>
                    <span class="test-passed">✅ {suite_data.get('passed', 0)}</span>
                    <span class="test-failed">❌ {suite_data.get('failed', 0)}</span>
                    <span class="test-skipped">⏭️ {suite_data.get('skipped', 0)}</span>
                    <span class="duration">({suite_data.get('total_duration', 0):.2f}s)</span>
                </div>
            </div>
            <div class="test-list">
            """
            
            for result in suite_data.get('results', []):
                status_class = f"test-{result['status']}"
                status_icon = "✅" if result['status'] == 'passed' else "❌" if result['status'] == 'failed' else "⏭️"
                
                html += f"""
                <div class="test-item">
                    <span class="{status_class}">
                        {status_icon} {result['name']}
                    </span>
                    <span class="duration">{result['duration']:.2f}s</span>
                </div>
                """
                
            html += """
            </div>
        </div>
            """
        
        html += """
    </div>
</body>
</html>
        """
        
        return html
        
    def _create_junit_xml(self, summary: Dict[str, Any], 
                         detailed_results: Dict[str, Any]) -> str:
        """Create JUnit XML format"""
        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<testsuites name="Automotas AI Tests" 
           tests="{summary['total_tests']}" 
           failures="{summary['failed']}" 
           skipped="{summary['skipped']}" 
           time="{summary['duration']:.3f}">
'''
        
        for suite_name, suite_data in detailed_results.items():
            xml += f'''  <testsuite name="{suite_name}" 
              tests="{suite_data.get('total_tests', 0)}" 
              failures="{suite_data.get('failed', 0)}" 
              skipped="{suite_data.get('skipped', 0)}" 
              time="{suite_data.get('total_duration', 0):.3f}">
'''
            
            for result in suite_data.get('results', []):
                xml += f'''    <testcase name="{result['name']}" 
               time="{result['duration']:.3f}">
'''
                if result['status'] == 'failed':
                    xml += f'''      <failure message="{result.get('error', '')}">{result.get('error', '')}</failure>
'''
                elif result['status'] == 'skipped':
                    xml += f'''      <skipped message="Test skipped"/>
'''
                    
                xml += '''    </testcase>
'''
                
            xml += '''  </testsuite>
'''
            
        xml += '''</testsuites>'''
        
        return xml
